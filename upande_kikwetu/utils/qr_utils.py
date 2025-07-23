import frappe
import qrcode
import json
from io import BytesIO
from frappe.utils.file_manager import save_file

def generate_and_attach_box_qr(box_label_doc):
    # 1) Let the user know we’re in the QR step
    frappe.msgprint(f"   • Generating QR for Box Label {box_label_doc.name}…")

    # 2) Build the JSON payload
    qr_dict = {
        "box_number": f"BX-{box_label_doc.box_number}",
        "order_pick_list": box_label_doc.order_pick_list,
        "customer": box_label_doc.customer,
        "po_no":     box_label_doc.get("customer_purchase_order", ""),
        "date":      str(box_label_doc.date),
        "farm_pack_list": box_label_doc.farm_pack_list_link
    }
    qr_data = json.dumps(qr_dict)

    # 3) Create the image in memory
    qr_img = qrcode.make(qr_data)
    img_io = BytesIO()
    qr_img.save(img_io, format="PNG")
    img_content = img_io.getvalue()

    # 4) Save as a File doc
    file_doc = save_file(
        fname=f"{box_label_doc.name}.png",
        content=img_content,
        dt=box_label_doc.doctype,
        dn=box_label_doc.name,
        folder=None,
        is_private=0
    )

    # 5) Attach the URL via a direct DB call (avoids full .save())
    frappe.db.set_value(
        box_label_doc.doctype,
        box_label_doc.name,
        "qr_code_image",
        file_doc.file_url
    )
    # Commit just this field change
    frappe.db.commit()

    frappe.msgprint(f"   ✔️ QR attached: {file_doc.file_url}")
    return file_doc
