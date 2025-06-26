# import json
# import os
# import frappe
# import qrcode
# from collections import defaultdict

# def generate_box_labels_with_qr(self, method):
#     try:
#         frappe.msgprint(f"Running QR label generation for {self.name}")

#         if self.docstatus != 1:
#             frappe.msgprint("Document not submitted.")
#             return

#         if not self.pack_list_item:
#             frappe.msgprint("No pack list items found.")
#             return

#         sales_order_id = self.custom_sales_order
#         pack_list_items = self.pack_list_item
#         farm_warehouse = pack_list_items[0].source_warehouse
#         farm = farm_warehouse.split()[0]

#         opl = frappe.db.sql("""
#             SELECT p.name
#             FROM `tabOrder Pick List` p
#             JOIN `tabPick List Item` i ON i.parent = p.name
#             WHERE p.sales_order = %s
#             AND i.warehouse = %s
#             AND i.idx = 1
#             LIMIT 1
#         """, (sales_order_id, f"{farm} Dispatch Coldstore - KF"), as_dict=1)

#         if not opl:
#             frappe.msgprint("No matching Order Pick List found.")
#             return

#         opl_doc = frappe.get_doc("Order Pick List", opl[0].name)
#         sales_order_doc = frappe.get_doc("Sales Order", sales_order_id)

#         boxes = defaultdict(list)
#         for item in pack_list_items:
#             if item.box_id:
#                 boxes[item.box_id].append(item)

#         if not boxes:
#             frappe.msgprint("No `box_id` values set on items.")
#             return

#         existing_labels = frappe.get_all(
#             "Box Label",
#             filters={"order_pick_list": opl_doc.name},
#             fields=["box_number"]
#         )
#         existing_box_numbers = {str(d.box_number) for d in existing_labels}

#         created_labels = []

#         for box_id, items in boxes.items():
#             if str(box_id) in existing_box_numbers:
#                 frappe.msgprint(f"Box {box_id} already has a label. Skipping.")
#                 continue

#             total_stems = sum(row.custom_number_of_stems for row in items)

#             new_label = frappe.new_doc("Box Label")
#             new_label.customer = self.custom_customer
#             new_label.box_number = int(box_id)
#             new_label.order_pick_list = opl_doc.name
#             new_label.pack_rate = total_stems
#             new_label.date = opl_doc.date_created
#             new_label.customer_purchase_order = sales_order_doc.po_no
#             new_label.consignee = sales_order_doc.custom_consignee
#             new_label.truck_details = sales_order_doc.custom_truck_details
#             new_label.farm_pack_list_link = self.name

#             for row in items:
#                 new_label.append("box_item", {
#                     "variety": row.item_code,
#                     "uom": row.bunch_uom,
#                     "qty": row.bunch_qty
#                 })

#             new_label.insert()
#             frappe.msgprint(f"Created Box Label: {new_label.name}")
#             created_labels.append(new_label.name)

#             generate_and_attach_box_qr(new_label)

#         if not created_labels:
#             frappe.msgprint("No new Box Labels were created.")
#         else:
#             frappe.msgprint(f"Created Box Labels: {', '.join(created_labels)}")

#     except Exception:
#         frappe.msgprint("An error occurred during box label generation. Check Error Log.")

# def generate_and_attach_box_qr(box_doc):
#     try:
#         qr_data = {
#             "box_number": box_doc.box_number,
#             "order_pick_list": box_doc.order_pick_list,
#             "customer": box_doc.customer,
#             "po_no": box_doc.customer_purchase_order,
#             "date": str(box_doc.date),
#             "farm_pack_list": box_doc.farm_pack_list_link
#         }

#         qr_string = json.dumps(qr_data)

#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=4,
#             border=2
#         )
#         qr.add_data(qr_string)
#         qr.make(fit=True)
#         qr_img = qr.make_image(fill='black', back_color='white')

#         qr_codes_dir = frappe.utils.get_files_path("qr_codes")
#         os.makedirs(qr_codes_dir, exist_ok=True)

#         file_name = f"box_label_{box_doc.name}.png"
#         file_path = os.path.join(qr_codes_dir, file_name)
#         qr_img.save(file_path)

#         file_doc = frappe.get_doc({
#             "doctype": "File",
#             "file_url": f"/files/qr_codes/{file_name}",
#             "attached_to_doctype": "Box Label",
#             "attached_to_name": box_doc.name,
#             "is_private": 0
#         })
#         file_doc.insert(ignore_permissions=True)

#         box_doc.db_set("qr_code_image", file_doc.file_url, update_modified=False)

#     except Exception:
#         frappe.msgprint(f"Failed to generate QR Code for Box Label: {box_doc.name}")
