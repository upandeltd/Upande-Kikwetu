import frappe
import json
from frappe.utils import getdate, today

@frappe.whitelist()
def create_sales_invoice_from_packlist_button(source_names, target_doc=None):
    # Parse inputs
    if isinstance(source_names, str):
        if not source_names:
            frappe.throw("No Consolidated Pack List selected.")
        try:
            source_names = json.loads(source_names)
        except (json.JSONDecodeError, TypeError):
            # Handle single string case (e.g., "CPL-001" instead of "[\"CPL-001\"]")
            source_names = [source_names]
    elif isinstance(source_names, (list, tuple)):
        pass  # Already a list, no need to parse
    else:
        frappe.throw(f"Invalid source_names type: {type(source_names)}. Expected a JSON string or list.")

    if not source_names:
        frappe.throw("No Consolidated Pack List selected.")

    # Initialize Sales Invoice
    sales_invoice = frappe.get_doc(target_doc) if target_doc else frappe.new_doc("Sales Invoice")
    created_so_ids = set()

    # Validate custom fields
    required_fields = ["custom_shipping_agent", "custom_destination", "custom_consignee", "custom_comment"]
    for field in required_fields:
        if not frappe.get_meta("Sales Invoice").has_field(field):
            frappe.throw(f"Custom field '{field}' not found in Sales Invoice.")

    for cpl_name in source_names:
        try:
            cpl = frappe.get_doc("Consolidated Pack List", cpl_name)
        except frappe.DoesNotExistError:
            frappe.msgprint(f"Consolidated Pack List {cpl_name} does not exist. Skipping.")
            continue

        for item in cpl.items:
            if not item.sales_order_id or item.sales_order_id in created_so_ids:
                continue

            try:
                sales_order = frappe.get_doc("Sales Order", item.sales_order_id)
            except frappe.DoesNotExistError:
                frappe.msgprint(f"Sales Order {item.sales_order_id} does not exist. Skipping.")
                continue

            created_so_ids.add(item.sales_order_id)

            # Set standard fields (first match only)
            if not sales_invoice.get("customer"):
                sales_invoice.customer = sales_order.customer
                sales_invoice.custom_shipping_agent = sales_order.custom_shipping_agent
                sales_invoice.custom_destination = sales_order.custom_delivery_point
                sales_invoice.custom_consignee = sales_order.custom_consignee
                sales_invoice.custom_comment = sales_order.custom_comment
                sales_invoice.set_warehouse = item.source_warehouse or sales_order.set_warehouse
                sales_invoice.posting_date = today()
                sales_invoice.update_stock = 1
                delivery_date = sales_order.delivery_date or sales_invoice.posting_date
                sales_invoice.due_date = getdate(delivery_date) if delivery_date else getdate(sales_invoice.posting_date)
                
                # Validate taxes consistency
                if sales_invoice.taxes_and_charges and sales_invoice.taxes_and_charges != sales_order.taxes_and_charges:
                    frappe.msgprint(f"Warning: Taxes and charges differ in Sales Order {sales_order.name}. Using first Sales Order's taxes.")
                else:
                    sales_invoice.taxes_and_charges = sales_order.taxes_and_charges
                    sales_invoice.taxes = sales_order.taxes

            # Match item and append
            so_item = next((i for i in sales_order.items if i.item_code == item.item_code), None)
            if not so_item or not item.bunch_qty or item.bunch_qty <= 0:
                continue

            sales_invoice.append("items", {
                "item_code": item.item_code,
                "qty": item.bunch_qty,
                "uom": item.bunch_uom,
                "bunch_qty": item.bunch_qty,
                "bunch_uom": item.bunch_uom,
                "custom_number_of_stems": item.custom_number_of_stems,
                "rate": so_item.rate,
                "custom_length": so_item.custom_length,
                "discount_percentage": so_item.discount_percentage
            })

    if not sales_invoice.items:
        frappe.throw("No valid items found to create Sales Invoice.")

    return sales_invoice