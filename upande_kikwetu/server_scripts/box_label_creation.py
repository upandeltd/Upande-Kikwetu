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

        # Group by box_id
        boxes = defaultdict(list)
        for item in pack_list_items:
            if item.box_id:
                boxes[str(item.box_id)].append(item)

        if not boxes:
            frappe.throw("Please enter 'box_id' for at least one item before submission.")

        # Existing labels
        existing_labels = frappe.get_all(
            "Box Label",
            filters={"order_pick_list": opl_doc.name},
            fields=["box_number"]
        )
        existing_box_numbers = {str(d.box_number) for d in existing_labels}

        created_labels = []

        for box_id, items in boxes.items():
            try:
                if str(box_id) in existing_box_numbers:
                    frappe.msgprint(f"Box {box_id} already has a label. Skipping.")
                    continue

                total_stems = sum(row.custom_number_of_stems for row in items)

                new_label = frappe.new_doc("Box Label")
                new_label.customer = self.custom_customer
                new_label.box_number = int(box_id)
                new_label.order_pick_list = opl_doc.name
                new_label.pack_rate = total_stems
                new_label.date = opl_doc.date_created
                new_label.customer_purchase_order = sales_order_doc.po_no
                new_label.consignee = sales_order_doc.custom_consignee
                new_label.truck_details = sales_order_doc.custom_truck_details
                new_label.farm_pack_list_link = self.name

                for row in items:
                    new_label.append("box_item", {
                        "variety": row.item_code,
                        "uom": row.bunch_uom,
                        "qty": row.bunch_qty
                    })

                new_label.insert()
                created_labels.append(new_label.name)
                frappe.msgprint(f"Created Box Label: {new_label.name}")

                try:
                    generate_and_attach_box_qr(new_label)
                except Exception:
                    frappe.log_error(traceback.format_exc(), f"QR Generation Failed for {new_label.name}")
                    frappe.msgprint(f"QR generation failed for Box {box_id}, but label was created.")

            except Exception:
                frappe.log_error(traceback.format_exc(), f"Error processing Box {box_id}")
                frappe.throw(f"Failed while processing Box {box_id}. Check Error Log.")

        if not created_labels:
            frappe.msgprint("No new Box Labels were created.")
        else:
            frappe.msgprint(f"Created Box Labels: {', '.join(created_labels)}")

    except Exception:
        frappe.log_error(traceback.format_exc(), f"Box Label Creation Failed for {self.name}")
        frappe.throw("An unexpected error occurred during box label generation. See Error Log.")