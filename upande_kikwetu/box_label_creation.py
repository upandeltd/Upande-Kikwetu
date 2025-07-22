import qrcode
import base64
import io
import frappe


def generate_qr(data):
    img = qrcode.make(data)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{qr_base64}"


def before_save(doc, method):
    qr_content = f"BOX: {doc.box_number} | DATE: {doc.date.strftime('%d/%m/%Y')}"
    doc.qr_code = generate_qr(qr_content)