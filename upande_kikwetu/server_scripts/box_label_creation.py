import frappe
from collections import defaultdict
import traceback
from upande_kikwetu.utils.qr_utils import generate_and_attach_box_qr

def generate_box_labels_with_qr(self, method):
    try:
        frappe.msgprint(f"Running QR label generation for {self.name}")

        if self.docstatus != 1:
            frappe.msgprint("Document not submitted.")
            return

        if not self.pack_list_item:
            frappe.msgprint("No pack list items found.")
            return

        sales_order_id = self.custom_sales_order
        pack_list_items = self.pack_list_item

        # Get Order Pick List
        opl = frappe.db.sql("""
            SELECT p.name 
            FROM `tabOrder Pick List` p
            JOIN `tabPick List Item` i ON i.parent = p.name
            WHERE p.sales_order = %s
            AND i.idx = 1
            LIMIT 1
        """, (sales_order_id,), as_dict=True)

        if not opl:
            frappe.throw("No matching Order Pick List found.")

        opl_doc = frappe.get_doc("Order Pick List", opl[0].name)
        sales_order_doc = frappe.get_doc("Sales Order", sales_order_id)

        # Get max box_number from existing Box Labels
        max_box_number = frappe.db.sql("""
            SELECT COALESCE(MAX(box_number), 0) as max_box_number
            FROM `tabBox Label`
            WHERE order_pick_list = %s
        """, (opl_doc.name,), as_dict=True)[0].max_box_number or 0

        # Group by mix_number or fallback to index
        boxes = defaultdict(list)
        for item in pack_list_items:
            mix_number = str(item.mix_number) if item.mix_number else f"single_{item.idx}"
            boxes[mix_number].append(item)

        if not boxes:
            frappe.throw("No valid items found for box label generation.")

        existing_labels = frappe.get_all(
            "Box Label",
            filters={"order_pick_list": opl_doc.name},
            fields=["box_number"]
        )
        existing_box_numbers = {str(d.box_number) for d in existing_labels}

        created_labels = []
        current_box_number = max_box_number + 1

        for mix_number, items in boxes.items():
            try:
                while str(current_box_number) in existing_box_numbers:
                    frappe.msgprint(f"Box number {current_box_number} already used. Incrementing.")
                    current_box_number += 1

                total_stems = sum(row.custom_number_of_stems for row in items)

                new_label = frappe.new_doc("Box Label")
                new_label.customer = self.custom_customer
                new_label.box_number = current_box_number
                new_label.order_pick_list = opl_doc.name
                new_label.pack_rate = total_stems
                new_label.date = opl_doc.date_created
                new_label.customer_purchase_order = sales_order_doc.po_no
                new_label.consignee = sales_order_doc.custom_consignee
                new_label.truck_details = sales_order_doc.custom_truck_details
                new_label.farm_pack_list_link = self.name
                # ⚠️ Name is NOT set manually here — let Frappe handle it

                for row in items:
                    new_label.append("box_item", {
                        "variety": row.item_code,
                        "uom": row.bunch_uom,
                        "qty": row.bunch_qty
                    })

                required_fields = ["customer", "box_number", "order_pick_list", "pack_rate"]
                missing_fields = [field for field in required_fields if not getattr(new_label, field, None)]
                if missing_fields:
                    frappe.log_error(
                        message=f"Missing fields: {missing_fields}",
                        title=f"QR Gen Missing B{current_box_number}"
                    )
                    frappe.msgprint(f"Cannot generate QR for Box {current_box_number}: Missing {missing_fields}")
                    continue

                if not new_label.box_item:
                    frappe.log_error(
                        message=f"No box items for box {current_box_number}",
                        title=f"QR Gen No Items B{current_box_number}"
                    )
                    frappe.msgprint(f"Cannot generate QR for Box {current_box_number}: No box items")
                    continue

                new_label.insert(ignore_if_duplicate=True)
                frappe.db.commit()
                created_labels.append(new_label.name)
                frappe.msgprint(f"Created Box Label: {new_label.name} (Box {current_box_number})")

                try:
                    generate_and_attach_box_qr(new_label)
                    frappe.msgprint(f"QR code generated for Box {current_box_number}")
                except Exception as qr_error:
                    frappe.log_error(
                        message=f"{traceback.format_exc()}\nBox Label Data: {new_label.as_dict()}",
                        title=f"QR Gen Fail B{current_box_number}"
                    )
                    frappe.msgprint(f"QR generation failed for Box {current_box_number}: {str(qr_error)}")

                current_box_number += 1

            except Exception as e:
                frappe.db.rollback()
                frappe.log_error(
                    message=traceback.format_exc(),
                    title=f"Box Creation Fail B{current_box_number}"
                )
                frappe.msgprint(f"Failed processing Box {current_box_number}: {str(e)}")
                current_box_number += 1

        if not created_labels:
            frappe.msgprint("No new Box Labels were created.")
        else:
            frappe.msgprint(f"Created Box Labels: {', '.join(created_labels)}")

    except Exception:
        frappe.db.rollback()
        frappe.log_error(
            message=traceback.format_exc(),
            title=f"Box Label Fail {self.name}"[:139]
        )
        frappe.throw("An unexpected error occurred during box label generation. See Error Log.")
