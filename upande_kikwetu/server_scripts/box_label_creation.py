import frappe
from collections import defaultdict
import traceback
from datetime import datetime
from upande_kikwetu.utils.qr_utils import generate_and_attach_box_qr

MAX_ERROR_TITLE_LENGTH = 140

def truncate_title(title, max_length=MAX_ERROR_TITLE_LENGTH):
    return title[:max_length]

def generate_box_labels_with_qr(self, method):
    # Step 1: Ensure the Farm Pack List is submitted
    frappe.msgprint("🔹 Step 1: Checking document status…")
    if self.docstatus == 0:
        frappe.msgprint("   • Document is draft. Submitting now…")
        self.submit()
        frappe.db.commit()
        frappe.msgprint("   ✓ Document submitted.")
    if self.docstatus != 1:
        frappe.throw("Document must be submitted before generating box labels.")

    # Step 2: Announce start of processing
    frappe.msgprint("🔹 Step 2: Beginning box-label + QR-code generation…")

    # Validate pack list items
    if not self.pack_list_item:
        frappe.msgprint("   ⚠️ No pack list items to process. Exiting.")
        return

    # Step 3: Load related Order Pick List and Sales Order
    frappe.msgprint("🔹 Step 3: Fetching Order Pick List & Sales Order…")
    so_name = self.custom_sales_order
    opl = frappe.db.get_all(
        "Order Pick List",
        filters={"sales_order": so_name},
        fields=["name"],
        limit_page_length=1
    )
    if not opl:
        frappe.throw("No Order Pick List found for this Sales Order.")
    opl_name = opl[0].name
    opl_doc = frappe.get_doc("Order Pick List", opl_name)
    so_doc  = frappe.get_doc("Sales Order", so_name)
    frappe.msgprint(f"   ✓ Found OPL {opl_name}")

    # Step 4: Build existing box number set
    frappe.msgprint("🔹 Step 4: Loading existing box numbers…")
    existing = frappe.get_all(
        "Box Label",
        filters={"order_pick_list": opl_name},
        fields=["box_number"]
    )
    used = {str(d.box_number) for d in existing}
    next_box = max([int(n) for n in used if n.isdigit()] or [0]) + 1
    frappe.msgprint(f"   ✓ Next available box number: {next_box}")

    # Step 5: Group pack list items into “boxes”
    frappe.msgprint("🔹 Step 5: Grouping items into boxes…")
    boxes = defaultdict(list)
    for row in self.pack_list_item:
        key = str(row.mix_number) if row.mix_number else f"single_{row.idx}"
        boxes[key].append(row)
    frappe.msgprint(f"   ✓ Created {len(boxes)} box group(s)")

    created = []

    # Step 6: Iterate groups and create labels + QR
    for idx, (mix_key, items) in enumerate(boxes.items(), start=1):
        frappe.msgprint(f"🔹 Step 6.{idx}: Processing box group “{mix_key}”…")

        # Skip used box_numbers
        while str(next_box) in used:
            next_box += 1

        # Skip if a label already exists for this box_number
        if frappe.db.exists("Box Label", {
            "order_pick_list": opl_name,
            "box_number": next_box
        }):
            frappe.msgprint(f"   • Box #{next_box} already has a label. Skipping.")
            next_box += 1
            continue

        # Build new Box Label
        total_stems = sum(r.custom_number_of_stems for r in items)
        label = frappe.new_doc("Box Label")
        label.update({
            "customer": self.custom_customer,
            "box_number": next_box,
            "order_pick_list": opl_name,
            "pack_rate": total_stems,
            "date": opl_doc.date_created,
            "customer_purchase_order": so_doc.po_no,
            "consignee": so_doc.custom_consignee,
            "truck_details": so_doc.custom_truck_details,
            "farm_pack_list_link": self.name
        })
        for r in items:
            label.append("box_item", {
                "variety": r.item_code,
                "uom":     r.bunch_uom,
                "qty":     r.bunch_qty
            })

        # Insert and commit
        frappe.msgprint(f"   • Creating Box Label for Box #{next_box}…")
        try:
            label.insert()
            frappe.db.commit()
            created.append(label.name)
            frappe.msgprint(f"     ✓ Label {label.name} created.")
        except Exception as e:
            frappe.db.rollback()
            frappe.log_error(
                message=traceback.format_exc(),
                title=truncate_title(f"Create Fail Box {next_box}")
            )
            frappe.msgprint(f"     ⚠️ Failed to create label for Box #{next_box}: {e}")
            next_box += 1
            continue

        # Generate QR
        frappe.msgprint(f"   • Generating QR for Box #{next_box}…")
        try:
            generate_and_attach_box_qr(label)
            frappe.msgprint(f"     🎉 QR attached for Box #{next_box}.")
        except Exception as qr_e:
            frappe.log_error(
                message=traceback.format_exc(),
                title=truncate_title(f"QR Fail Box {next_box}")
            )
            frappe.msgprint(f"     ⚠️ QR failed for Box #{next_box}: {qr_e}")

        next_box += 1

    # Step 7: Final summary
    if created:
        frappe.msgprint(f"🏁 Done! Created labels: {', '.join(created)}")
    else:
        frappe.msgprint("📭 No new labels were created.")
