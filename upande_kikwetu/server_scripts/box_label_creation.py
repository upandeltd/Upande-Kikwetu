import frappe
from collections import defaultdict
import traceback
from datetime import datetime
from upande_kikwetu.utils.qr_utils import generate_and_attach_box_qr

def generate_box_labels_with_qr(self, method):
    # STEP 1: Ensure Farm Pack List is submitted
    frappe.msgprint("⚙️ 1) Checking Farm Pack List submission…")
    if self.docstatus == 0:
        frappe.msgprint("   • It’s a draft. Submitting now…")
        self.submit()
        frappe.db.commit()
        frappe.msgprint("   ✔️ Submitted.")
    if self.docstatus != 1:
        frappe.throw("Farm Pack List must be submitted before generating labels.")

    # STEP 2: Quick sanity check
    frappe.msgprint("⚙️ 2) Verifying pack_list_item…")
    if not self.pack_list_item:
        frappe.msgprint("   ⚠️ No items found. Exiting.")
        return

    # STEP 3: Load related documents
    frappe.msgprint("⚙️ 3) Fetching Order Pick List & Sales Order…")
    so_name = self.custom_sales_order
    opl = frappe.db.get_value("Order Pick List",
                              {"sales_order": so_name},
                              "name")
    if not opl:
        frappe.throw(f"No Order Pick List found for Sales Order {so_name}")
    opl_doc = frappe.get_doc("Order Pick List", opl)
    so_doc  = frappe.get_doc("Sales Order", so_name)
    frappe.msgprint(f"   ✔️ Found OPL {opl}")

    # STEP 4: Build used‐box set
    frappe.msgprint("⚙️ 4) Loading existing Box Label numbers…")
    used_nums = set(frappe.get_all("Box Label",
                                   filters={"order_pick_list": opl},
                                   pluck="box_number"))
    next_box = (max(map(int, used_nums)) + 1) if used_nums else 1
    frappe.msgprint(f"   ✔️ Next available box_number = {next_box}")

    # STEP 5: Group items into boxes
    frappe.msgprint("⚙️ 5) Grouping pack list items…")
    boxes = defaultdict(list)
    for row in self.pack_list_item:
        key = row.mix_number or f"single_{row.idx}"
        boxes[str(key)].append(row)
    frappe.msgprint(f"   ✔️ {len(boxes)} group(s) ready")

    created = []

    # STEP 6: Iterate, check existence, insert, QR
    for idx, (mix_key, items) in enumerate(boxes.items(), start=1):
        frappe.msgprint(f"⚙️ 6.{idx}) Processing group “{mix_key}” → Box #{next_box}")

        # Skip until free
        while next_box in used_nums:
            next_box += 1

        # 6.a) Existence check
        existing = frappe.db.exists("Box Label", {
            "order_pick_list": opl,
            "box_number": next_box
        })
        if existing:
            frappe.msgprint(f"   • Box #{next_box} already labeled as {existing}. Skipping.")
            used_nums.add(next_box)
            next_box += 1
            continue

        # 6.b) Create new Box Label
        total_stems = sum(r.custom_number_of_stems for r in items)
        lbl = frappe.new_doc("Box Label")
        lbl.update({
            "customer": self.custom_customer,
            "box_number": next_box,
            "order_pick_list": opl,
            "pack_rate": total_stems,
            "date": opl_doc.date_created,
            "customer_purchase_order": so_doc.po_no,
            "consignee": so_doc.custom_consignee,
            "truck_details": so_doc.custom_truck_details,
            "farm_pack_list_link": self.name
        })
        for r in items:
            lbl.append("box_item", {
                "variety": r.item_code,
                "uom":     r.bunch_uom,
                "qty":     r.bunch_qty
            })

        frappe.msgprint(f"   • Inserting Box Label for Box #{next_box}…")
        try:
            lbl.insert()
            frappe.db.commit()
            created.append(lbl.name)
            used_nums.add(next_box)
            frappe.msgprint(f"     ✔️ Created {lbl.name}")
        except Exception as e:
            frappe.db.rollback()
            frappe.msgprint(f"     ⚠️ Insert failed: {e}")
            frappe.log_error(message=traceback.format_exc(),
                             title=f"Insert Fail Box {next_box}")
            next_box += 1
            continue

        # 6.c) Always generate QR (even if it existed before)
        frappe.msgprint(f"   • Generating QR for {lbl.name}…")
        try:
            generate_and_attach_box_qr(lbl)
        except Exception as e:
            frappe.msgprint(f"     ⚠️ QR generation failed: {e}")
            frappe.log_error(message=traceback.format_exc(),
                             title=f"QR Fail Box {next_box}")

        next_box += 1

    # STEP 7: Wrap up
    if created:
        frappe.msgprint(f"🏁 Done! Labels created: {', '.join(created)}")
    else:
        frappe.msgprint("📭 No new labels were created.")
