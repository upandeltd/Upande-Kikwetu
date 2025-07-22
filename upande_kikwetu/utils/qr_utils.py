import frappe
import qrcode
import json
from io import BytesIO
from frappe.utils.file_manager import save_file

def generate_and_attach_box_qr(box_label_doc):
    # Try to fetch Farm Pack List to get Sales Order
    sales_order = ""
    if box_label_doc.farm_pack_list_link:
        try:
            farm_doc = frappe.get_doc("Farm Pack List", box_label_doc.farm_pack_list_link)
            sales_order = farm_doc.custom_sales_order or ""
        except Exception:
            sales_order = ""

    # Structure data as JSON
    qr_dict = {
        "box_number": f"BX-{box_label_doc.box_number}",
        "order_pick_list": box_label_doc.order_pick_list,
        "customer": box_label_doc.customer,
        "po_no": sales_order,
        "date": str(box_label_doc.date),
        "farm_pack_list": box_label_doc.farm_pack_list_link
    }

    # Convert to JSON string
    qr_data = json.dumps(qr_dict)

    # Generate QR image
    qr_img = qrcode.make(qr_data)

    # Save to memory
    img_io = BytesIO()
    qr_img.save(img_io, format='PNG')
    img_content = img_io.getvalue()

    # Save as file in ERPNext
    file_doc = save_file(
        fname=f"{box_label_doc.name}.png",
        content=img_content,
        dt=box_label_doc.doctype,
        dn=box_label_doc.name,
        folder=None,
        is_private=0
    )

    # Link image to field
    box_label_doc.qr_code_image = file_doc.file_url
    box_label_doc.save(ignore_permissions=True)

    return file_doc