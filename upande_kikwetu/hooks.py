app_name = "upande_kikwetu"
app_title = "Upande Kikwetu"
app_publisher = "Upande Limited"
app_description = "ERPNext implementation for Kikwetu"
app_email = "newton@upande.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "upande_kikwetu",
# 		"logo": "/assets/upande_kikwetu/logo.png",
# 		"title": "Upande Kikwetu",
# 		"route": "/upande_kikwetu",
# 		"has_permission": "upande_kikwetu.api.permission.has_app_permission"
# 	}
# ]
app_include_js = [
    "/assets/upande_kikwetu/client_scripts/fetch_item_grp_price.js",
    "/assets/upande_kikwetu/client_scripts/update_stock_sales_inv.js",
    "/assets/upande_kikwetu/client_scripts/se_rejection_reason.js",
    "/assets/upande_kikwetu/client_scripts/so_stock_transfer.js",
    "/assets/upande_kikwetu/client_scripts/autofetch_pricelist.js"
]


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/upande_kikwetu/css/upande_kikwetu.css"
# app_include_js = "/assets/upande_kikwetu/js/upande_kikwetu.js"

# include js, css files in header of web template
# web_include_css = "/assets/upande_kikwetu/css/upande_kikwetu.css"
# web_include_js = "/assets/upande_kikwetu/js/upande_kikwetu.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "upande_kikwetu/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "upande_kikwetu/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "upande_kikwetu.utils.jinja_methods",
# 	"filters": "upande_kikwetu.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "upande_kikwetu.install.before_install"
# after_install = "upande_kikwetu.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "upande_kikwetu.uninstall.before_uninstall"
# after_uninstall = "upande_kikwetu.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "upande_kikwetu.utils.before_app_install"
# after_app_install = "upande_kikwetu.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "upande_kikwetu.utils.before_app_uninstall"
# after_app_uninstall = "upande_kikwetu.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "upande_kikwetu.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
doc_events = {
    "Sales Order": {
        "on_submit":
        "upande_kikwetu.server_scripts.pick_list_automation.create_pick_list_for_sales_order",
        "before_submit":
        "upande_kikwetu.upande_kikwetu.custom.sales_order_custom.validate_customer_check_limit",
        "on_update":
        "upande_kikwetu.server_scripts.so_delivery_warehouse.handle_sales_order_approval",
        "on_cancel":
        "upande_kikwetu.server_scripts.so_delivery_warehouse.handle_sales_order_cancellation"
    },
    "Consolidated Pack List": {
        "on_submit":
        "upande_kikwetu.server_scripts.create_sales_invoice.create_sales_invoice_from_packlist",
        "before_submit":
        "upande_kikwetu.server_scripts.completion_percentage.validate_completion_percentage"
    },
    "Sales Invoice": {
        "on_submit":
        "upande_kikwetu.server_scripts.sinv_approved_by.set_approved_by"
    },
    "Farm Pack List": {
        "before_cancel":
        "upande_kikwetu.server_scripts.fpl_to_cpl_link.before_cancel",
        # "on_submit":
        # "upande_kikwetu.server_scripts.create_box_sticker.create_box_sticker"
        "on_submit":
        "upande_kikwetu.server_scripts.box_label_creation.generate_box_labels_with_qr"
    
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"upande_kikwetu.tasks.all"
# 	],
# 	"daily": [
# 		"upande_kikwetu.tasks.daily"
# 	],
# 	"hourly": [
# 		"upande_kikwetu.tasks.hourly"
# 	],
# 	"weekly": [
# 		"upande_kikwetu.tasks.weekly"
# 	],
# 	"monthly": [
# 		"upande_kikwetu.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "upande_kikwetu.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "upande_kikwetu.event.get_events"
# }
override_class = {
    "erpnext.controllers.taxes_and_totals.calculate_taxes_and_totals":
    "upande_kikwetu.overrides.standard_system_rate.CustomTaxesAndTotals"
}

whitelisted_methods = {
    "get_item_group_price":
    "upande_kikwetu.server_scripts.fetch_item_grp_price.get_item_group_price",
    "create_sales_invoice":
    "upande_kikwetu.server_scripts.create_sales_invoice.create_sales_invoice",
#     "create_sales_invoice_from_packlist_button":
#     "upande_kikwetu.server_scripts.make_si_from_cpl_button.create_sales_invoice_from_packlist_button"
 }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "upande_kikwetu.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["upande_kikwetu.utils.before_request"]
# after_request = ["upande_kikwetu.utils.after_request"]

# Job Events
# ----------
# before_job = ["upande_kikwetu.utils.before_job"]
# after_job = ["upande_kikwetu.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"upande_kikwetu.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


fixtures = [
    {
        "dt": "Report",
        "filters": [
            ["name", "in", [
                "Greenhouse Supervisor's Summary",
                "No Of Transcations",
                "Tota Harvest Report Per Farm",
                "Total Stock Rejects",
                "Harvested Vs Received Report",
                "Farm Receiving Report(With Subtotals)",
                "Receiving",
                "No Of Created Records",
                "Farm Harvest Report(With Subtotals)",
                "Grading Report",
                "No of Bunches Per Grader",
                "Daily Order Pick List..",
                "Farm Harvest Summary",
                "Customer by Sales person",
                "Daily Order Pick List(No filters)",
                "Daily Order Pick List",
                "Test dpl",
                "Simplified Stock Balance Report",
                "Daily Order Pick List.",
                "opl",
                "opl color",
                "Rep opl",
                "#rep Order Pick List",
                "Packhouse Discards/Rejects Report",
                "Field Rejects Report",
            ]]
        ]
    },
    {
        "dt": "DocType",
        "filters": [
            ["name", "in", [
                "BLE Temperature Reading",
                "Box Details",
                "Box Label",
                "Box Label Item",
                "Bucket QR Code",
                "Bunch QR Code",
                "Custom Doctype 1",
                "Farm",
                "Grader QR Code",
                "Greenhouse Sections",
                "Harvest",
                "Harvest Reject Items",
                "Harvest Rejects",
                "Internal Delivery Note",
                "Internal Delivery Note Item",
                "Label Print",
                "Pack List Item",
                "QR Code",
                "QR Sequence",
                "Rejection Reason",
                "Rejects Data",
                "Rejects Data Items",
                "Scan",
                "Scan Check",
                "Scan Check List",
                "Scan Location",
                "Scanned Items",
                "Tendepay Statement Importer",
                "Truck Loading Manifest",
                "Update hooks file",
            ]]
        ]
    },
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "in", [
                "Journal Entry-custom_transaction_hash",
                "Material Request-custom_requisition_book_number",
                "Request for Quotation Supplier-custom_cc",
                "Sales Order Item-custom_mix_number",
                "Sales Order-custom_box_type",
                "Purchase Order-custom_shipping_method",
                "Stock Entry-custom_grader_name",
                "Supplier Quotation-custom_comment",
                "Stock Entry-custom_packed_by",
                "Stock Entry-custom_packing_details",
                "Stock Entry Detail-custom_discard_reason",
                "Material Request-custom_security_guard",
                "Material Request-custom_store_clerk",
                "Material Request-custom_employee",
                "Warehouse-custom_sections",
                "Supplier Quotation-custom_description",
                "Order Pick List-custom_stems",
                "Pick List Item-custom_stem_length",
                "Pick List Item-custom_number_of_boxes",
                "Sales Order-custom_consignee_address",
                "Sales Invoice-custom_sales_order",
                "Consolidated Pack List-custom_total_number_of_stems_on_cpl",
                "Stock Entry-custom_type",
                "Stock Entry-custom_vehicle_mileages",
                "Stock Entry-custom_registration_number",
                "Material Request-custom_vehicle_mileages",
                "Stock Entry-custom_cost_center",
                "Stock Entry-custom_employee",
                "Material Request-custom_cost_center",
                "Sales Invoice Item-custom_item_type",
                "Employee-custom_cost_center",
                "Sales Order Item-custom_number_of_boxes",
                "Material Request-custom_registration_number",
                "Warehouse-custom_block",
                "Warehouse-custom_varieties_grown",
                "Sales Order-custom_packing_date_",
                "Sales Invoice-custom_farm_code",
                "Sales Invoice-custom_consignee_address",
                "Sales Invoice-custom_consignee",
                "Customer-custom_consignee_details",
                "Customer-custom_consignee",
                "Sales Invoice-custom_dropoff_point",
                "Sales Order-custom_number_of_boxes",
                "Material Request-custom_automation_triggered",
                "Pick List Item-custom__stem_length",
                "Material Request-custom_type",
                "Custom Doctype 1-workflow_state",
                "Sales Order-custom_is_addition",
                "Purchase Order-custom_type",
                "Sales Order-custom_priority_level",
                "Asset Depreciation Schedule-farm",
                "Asset Movement Item-farm",
                "Payment Request-farm",
                "Payment Reconciliation Allocation-farm",
                "Payment Reconciliation-farm",
                "Supplier Quotation Item-farm",
                "Supplier Quotation-farm",
                "Account Closing Balance-farm",
                "Subcontracting Receipt Item-farm",
                "Subcontracting Receipt-farm",
                "Subcontracting Order Item-farm",
                "Subcontracting Order-farm",
                "Sales Order-farm",
                "Purchase Receipt-farm",
                "POS Invoice Item-farm",
                "POS Invoice-farm",
                "Subscription Plan-farm",
                "Subscription-farm",
                "Opening Invoice Creation Tool Item-farm",
                "Opening Invoice Creation Tool-farm",
                "POS Profile-farm",
                "Stock Reconciliation-farm",
                "Loyalty Program-farm",
                "Asset Capitalization-farm",
                "Asset Repair-farm",
                "Asset Value Adjustment-farm",
                "Landed Cost Item-farm",
                "Shipping Rule-farm",
                "Sales Taxes and Charges-farm",
                "Payment Entry Deduction-farm",
                "Stock Entry Detail-farm",
                "Purchase Receipt Item-farm",
                "Delivery Note Item-farm",
                "Material Request Item-farm",
                "Journal Entry Account-farm",
                "Sales Order Item-farm",
                "Purchase Invoice Item-farm",
                "Sales Invoice Item-farm",
                "Delivery Note-farm",
                "Budget-farm",
                "Stock Entry-farm",
                "Asset-farm",
                "Payment Entry-farm",
                "Purchase Invoice-farm",
                "Sales Invoice-farm",
                "Payment Ledger Entry-farm",
                "GL Entry-farm",
                "Asset Depreciation Schedule-greenhouse",
                "Asset Movement Item-greenhouse",
                "Payment Request-greenhouse",
                "Payment Reconciliation Allocation-greenhouse",
                "Payment Reconciliation-greenhouse",
                "Supplier Quotation Item-greenhouse",
                "Supplier Quotation-greenhouse",
                "Account Closing Balance-greenhouse",
                "Subcontracting Receipt Item-greenhouse",
                "Subcontracting Receipt-greenhouse",
                "Subcontracting Order Item-greenhouse",
                "Subcontracting Order-greenhouse",
                "Sales Order-greenhouse",
                "Purchase Receipt-greenhouse",
                "POS Invoice Item-greenhouse",
                "POS Invoice-greenhouse",
                "Subscription Plan-greenhouse",
                "Subscription-greenhouse",
                "Opening Invoice Creation Tool Item-greenhouse",
                "Opening Invoice Creation Tool-greenhouse",
                "POS Profile-greenhouse",
                "Stock Reconciliation-greenhouse",
                "Loyalty Program-greenhouse",
                "Asset Capitalization-greenhouse",
                "Asset Repair-greenhouse",
                "Asset Value Adjustment-greenhouse",
                "Landed Cost Item-greenhouse",
                "Shipping Rule-greenhouse",
                "Sales Taxes and Charges-greenhouse",
                "Payment Entry Deduction-greenhouse",
                "Stock Entry Detail-greenhouse",
                "Purchase Receipt Item-greenhouse",
                "Delivery Note Item-greenhouse",
                "Material Request Item-greenhouse",
                "Journal Entry Account-greenhouse",
                "Sales Order Item-greenhouse",
                "Purchase Invoice Item-greenhouse",
                "Sales Invoice Item-greenhouse",
                "Delivery Note-greenhouse",
                "Budget-greenhouse",
                "Stock Entry-greenhouse",
                "Asset-greenhouse",
                "Payment Entry-greenhouse",
                "Purchase Invoice-greenhouse",
                "Sales Invoice-greenhouse",
                "Payment Ledger Entry-greenhouse",
                "GL Entry-greenhouse",
                "Material Request-workflow_state",
                "Inter-Farm Transfer Request-workflow_state",
                "Warehouse-custom_farm",
                "Purchase Order-workflow_state",
                "Purchase Order-farm",
                "Purchase Taxes and Charges-farm",
                "Purchase Order Item-farm",
                "Purchase Order-greenhouse",
                "Purchase Taxes and Charges-greenhouse",
                "Purchase Order Item-greenhouse",
                "Sales Order Item-custom_no_of_boxes",
                "Sales Order-custom_total_stock_qty",
                "Customer-custom_priority_customer",
                "Print Settings-print_taxes_with_zero_amount",
                "Print Settings-print_uom_after_quantity",
                "Print Settings-compact_item_print",
                "Farm Pack List-custom_abbreviation",
                "Farm Pack List-custom_column_break_rdgtj",
                "Farm Pack List-custom_section_break_cx2w5",
                "Farm Pack List-custom_section_break_eiiiq",
                "Farm Pack List-custom_section_break_4orfq",
                "Farm Pack List-custom_column_break_dv6ss",
                "Farm Pack List-custom_column_break_qlxzd",
                "Farm Pack List-custom_column_break_emh3j",
                "Farm Pack List-custom_section_break_q7rqy",
                "Stock Entry Detail-custom_breeder",
                "Stock Entry Detail-custom_bay",
                "Farm Pack List-workflow_state",
                "Stock Entry Detail-custom_rejection_reason",
                "Consolidated Pack List-custom_farm_pack_list",
                "Consolidated Pack List-custom_currency",
                "Consolidated Pack List-custom_customer_address",
                "Consolidated Pack List-custom_column_break_yjdkb",
                "Consolidated Pack List-custom_total_stems",
                "Consolidated Pack List-custom_customer",
                "Consolidated Pack List-custom_section_break_sq88a",
                "Sales Invoice-custom_column_break_twget",
                "Sales Invoice-custom_column_break_3yno7",
                "Sales Invoice-custom_comment",
                "Sales Invoice-custom_section_break_d7jz8",
                "Pick List Item-custom_box_id",
                "Order Pick List-custom_consignee",
                "Sales Invoice-custom_approved_by",
                "Sales Order Item-custom_box_id",
                "Sales Invoice-workflow_state",
                "Sales Invoice-custom_consolidated_packlist",
                "Sales Order-custom_section_break_3tis5",
                "Sales Order-custom_column_break_alooa",
                "Farm Pack List-custom_currency",
                "Farm Pack List-custom_column_break_2rbeo",
                "Farm Pack List-custom_total_stems",
                "Farm Pack List-custom_column_break_d7v21",
                "Farm Pack List-custom_section_break_qgscf",
                "Farm Pack List-custom_customer_address",
                "Stock Entry-custom_scanned_grading",
                "Stock Entry-custom_bunch_id",
                "Sales Order-custom_available_stock",
                "Stock Entry-custom_bucket_id",
                "Farm Pack List-custom_customer",
                "Farm Pack List-custom_comment",
                "Pick List Item-custom_box_label",
                "Sales Order Item-custom_box_label",
                "Order Pick List-custom_comment",
                "Order Pick List-custom_section_break_rldqy",
                "Sales Order-custom_comment",
                "Order Pick List-custom_warehouse",
                "Order Pick List-custom_column_break_upapr",
                "Order Pick List-custom_truck_details",
                "Sales Order Item-custom_amount_stems",
                "Stock Entry-custom_grader_payroll_number",
                "Stock Entry-custom_harvester_payroll_number",
                "Consolidated Pack List-workflow_state",
                "Sales Invoice-custom_hs_code",
                "Sales Invoice-custom_shipping_agent",
                "Sales Invoice-custom_destination",
                "Sales Invoice-custom_point_of_entry",
                "Dispatch Form-custom_truck_reg_no",
                "Dispatch Form-custom_truck_drivers_name",
                "Sales Order-custom_column_break_5oo0s",
                "Sales Order-custom_shipping_agent",
                "Sales Order-custom_consignee",
                "Sales Order-custom_truck_details",
                "Sales Order-custom_material_transfer_created",
                "Dispatch Form Item-custom_number_of_stems",
                "Stock Entry-custom_column_break_flxs9",
                "Stock Entry-custom_bunched_by",
                "Stock Entry-custom_column_break_hwfte",
                "Employee-custom_archived",
                "Dispatch Form-custom_security_supervisor",
                "SKU Summary-custom_source_warehouse",
                "Dispatch Form-custom_sku_summary",
                "Dispatch Form Item-custom_stock_ledger_uom",
                "Employee-custom_workflow_section",
                "Sales Order-custom_delivery_point",
                "Order Pick List-custom_qr_code",
                "Consolidated Pack List-custom_dispatch_status",
                "Stock Entry-custom_bunch_qr_code",
                "Stock Entry-custom_scanned",
                "Farm Pack List-custom_sales_order",
                "Farm Pack List-custom_farm",
                "Farm Pack List-custom_status",
                "Sales Order-custom_s_number",
                "Sales Order-custom_column_break_mnsgv",
                "Dispatch Form-custom_week_",
                "Dispatch Form-custom_signature",
                "Dispatch Form-custom_compiled_bypacking_supervisor",
                "Dispatch Form-custom_column_break_vppm6",
                "Dispatch Form-custom_shipment_confirmation_awb_signature",
                "Dispatch Form-custom_comments",
                "Dispatch Form-custom_section_break_63l1f",
                "Dispatch Form-custom_column_break_y2q6x",
                "Dispatch Form-custom_dispatch_time",
                "Dispatch Form-custom_total_number_of_boxes_dispatched",
                "Dispatch Form-custom_section_break_mwy3p",
                "Stock Entry-custom_stem_length",
                "Dispatch Form-custom_trip",
                "Dispatch Form-custom_date",
                "Dispatch Form-custom_column_break_pdozs",
                "Dispatch Form-custom_section_break_fcmtc",
                "Dispatch Form-custom_arrival_time_at_dropoff_point",
                "Dispatch Form-custom_sample_temps",
                "Farm Pack List-custom_is_closed",
                "Sales Invoice Item-custom_length",
                "Dispatch Form-custom_company",
                "Pick List Item-custom_source_warehouse",
                "Customer-custom_check_limit",
                "Stock Entry-custom_column_break_9qtpv",
                "Stock Entry-custom_farm",
                "Item-custom_barcode",
                "Stock Entry-custom_barcode",
                "Stock Entry-custom_graded_by",
                "Stock Entry-custom_bunching_details",
                "Stock Entry-custom_greenhouse",
                "Stock Entry-custom_block__bed_number",
                "Stock Entry-custom_column_break_jpvrh",
                "Stock Entry-custom_harvester",
                "Stock Entry-custom_bucket_details",
                "Stock Entry Detail-custom_greenhouse",
                "Stock Entry Detail-custom_harvester",
                "Sales Order Item-custom_length",
                "Stock Entry Detail-custom_bunching_details",
                "Stock Entry Detail-custom_bunched_by",
                "Sales Order-custom_reason_for_rejected_sales_order",
                "Stock Entry Detail-custom_block__bed_number",
                "Stock Entry Detail-custom_column_break_a9reo",
                "Stock Entry Detail-custom_grower",
                "Stock Entry Type-custom_default_source_warehouse",
                "Stock Entry Detail-custom_section_break_z5bnh",
                "Sales Order Item-custom_source_warehouse",
                "Stock Entry Type-custom_default_target_warehouse",
                "Sales Order-workflow_state",
                "Delivery Note-custom_prepared",
                "Stock Entry-custom_qr_code",
                "Stock Entry-custom_column_break_yqk33",
                "Sales Invoice-custom_vat_no",
                "Sales Invoice-custom_export_no",
                "Item-custom_length",
                "Delivery Note-custom_stamp",
                "Delivery Note-custom_date",
                "Delivery Note-custom_sign",
                "Delivery Note-custom_received_by_name",
                "Delivery Note-custom_column_break_vmyq8",
                "Delivery Note-custom_signature",
                "Delivery Note-custom_name",
                "Delivery Note-custom_prepared_by",
                "Delivery Note-custom_prepared_by__received_by",
                "Delivery Note-custom_order_no",
                "Delivery Note-custom_invoice_no",
                "Sales Order-custom_statescountry",
                "Sales Order-custom_week",
                "Address-is_your_company_address",
                "Contact-is_billing_contact",
                "Address-tax_category",
            ]]
        ]
    },
    {
        "dt": "Property Setter",
        "filters": [
            ["name", "in", [
                "Journal Entry-main-field_order",
                "Warehouse-main-field_order",
                "Material Request-material_request_type-in_list_view",
                "Material Request-per_received-in_list_view",
                "Material Request-per_ordered-in_list_view",
                "Material Request-title-in_list_view",
                "Material Request-workflow_state-in_list_view",
                "Material Request-status-in_list_view",
                "Material Request-schedule_date-in_list_view",
                "Material Request-main-field_order",
                "Item Barcode-barcode-hidden",
                "Stock Entry Detail-t_warehouse-link_filters",
                "Stock Entry Detail-s_warehouse-link_filters",
                "Stock Entry Detail-main-field_order",
                "Stock Entry Detail-barcode-hidden",
                "Stock Entry Detail-allow_zero_valuation_rate-default",
                "Customer-territory-in_list_view",
                "Customer-naming_series-reqd",
                "Customer-naming_series-hidden",
                "Customer-main-field_order",
                "Customer-customer_name-in_list_view",
                "Customer-customer_group-in_list_view",
                "Dispatch Form-naming_series-options",
                "Dispatch Form-naming_series-hidden",
                "Dispatch Form-main-field_order",
                "Dispatch Form-main-default_print_format",
                "Employee-main-search_fields",
                "Employee-main-field_order",
                "Employee-main-autoname",
                "Material Request-work_order-depends_on",
                "Material Request-set_warehouse-in_list_view",
                "Material Request-scan_barcode-hidden",
                "Material Request-main-default_print_format",
                "Item-naming_series-reqd",
                "Item-naming_series-options",
                "Item-naming_series-hidden",
                "Item-main-links_order",
                "Item-main-field_order",
                "Item-item_code-reqd",
                "Item-item_code-hidden",
                "Item-barcodes-hidden",
                "Farm Pack List-packed-in_list_view",
                "Farm Pack List-naming_series-read_only",
                "Farm Pack List-naming_series-options",
                "Farm Pack List-naming_series-hidden",
                "Farm Pack List-main-search_fields",
                "Farm Pack List-main-naming_rule",
                "Farm Pack List-main-links_order",
                "Farm Pack List-main-field_order",
                "Farm Pack List-main-default_print_format",
                "Farm Pack List-main-autoname",
                "Farm Pack List-custom_sales_order-in_list_view",
                "Farm Pack List-custom_farm-in_list_view",
                "Dispatch Form Item-main-field_order",
                "Dispatch Form Item-item_group-fetch_from",
                "Sales Invoice Item-uom-label",
                "Sales Invoice Item-uom-in_list_view",
                "Sales Invoice Item-target_warehouse-hidden",
                "Sales Invoice Item-stock_qty-label",
                "Sales Invoice Item-stock_qty-in_list_view",
                "Sales Invoice Item-qty-label",
                "Sales Invoice Item-main-field_order",
                "Sales Invoice Item-item_group-in_list_view",
                "Sales Invoice Item-item_code-link_filters",
                "Sales Invoice Item-discount_account-mandatory_depends_on",
                "Sales Invoice Item-discount_account-hidden",
                "Sales Invoice Item-barcode-hidden",
                "Stock Entry-to_warehouse-in_list_view",
                "Stock Entry-target_warehouse_address-hidden",
                "Stock Entry-stock_entry_type-in_list_view",
                "Stock Entry-source_warehouse_address-hidden",
                "Stock Entry-section_break_7qsm-hidden",
                "Stock Entry-scan_barcode-hidden",
                "Stock Entry-sb0-label",
                "Stock Entry-sb0-hidden",
                "Stock Entry-purpose-in_list_view",
                "Stock Entry-posting_time-in_list_view",
                "Stock Entry-posting_date-in_list_view",
                "Stock Entry-per_transferred-in_list_view",
                "Stock Entry-naming_series-options",
                "Stock Entry-naming_series-default",
                "Stock Entry-main-field_order",
                "Stock Entry-is_return-in_list_view",
                "Stock Entry-from_warehouse-in_list_view",
                "Stock Entry-custom_stem_length-in_list_view",
                "Stock Entry-custom_bunched_by-in_list_view",
                "Stock Entry-bom_info_section-hidden",
                "Sales Order Item-warehouse-link_filters",
                "Sales Order Item-warehouse-default",
                "Sales Order Item-uom-label",
                "Sales Order Item-uom-in_list_view",
                "Sales Order Item-stock_qty-label",
                "Sales Order Item-stock_qty-in_list_view",
                "Sales Order Item-qty-label",
                "Sales Order Item-main-field_order",
                "Sales Order Item-item_group-in_list_view",
                "Sales Order Item-item_group-hidden",
                "Sales Order Item-item_code-link_filters",
                "Sales Order Item-delivery_date-label",
                "Sales Order Item-company_total_stock-label",
                "Sales Order Item-actual_qty-label",
                "Packed Item-rate-read_only",
                "SKU Summary-main-field_order",
                "Order Pick List-source_warehouse-in_list_view",
                "Order Pick List-source_warehouse-fetch_from",
                "Order Pick List-sales_order-in_standard_filter",
                "Order Pick List-sales_order-in_list_view",
                "Order Pick List-naming_series-options",
                "Order Pick List-naming_series-default",
                "Order Pick List-main-search_fields",
                "Order Pick List-main-field_order",
                "Order Pick List-main-default_print_format",
                "Order Pick List-date_created-in_list_view",
                "Order Pick List-customer-in_list_view",
                "Order Pick List-custom_warehouse-in_list_view",
                "Sales Order-workflow_state-in_list_view",
                "Sales Order-total_qty-label",
                "Sales Order-tax_id-print_hide",
                "Sales Order-tax_id-hidden",
                "Sales Order-status-in_list_view",
                "Sales Order-set_warehouse-label",
                "Sales Order-set_warehouse-hidden",
                "Sales Order-scan_barcode-hidden",
                "Sales Order-rounded_total-print_hide",
                "Sales Order-rounded_total-hidden",
                "Sales Order-po_no-hidden",
                "Sales Order-po_date-hidden",
                "Sales Order-per_delivered-in_list_view",
                "Sales Order-per_billed-in_list_view",
                "Sales Order-payment_schedule-print_hide",
                "Sales Order-order_type-hidden",
                "Sales Order-naming_series-read_only",
                "Sales Order-naming_series-options",
                "Sales Order-naming_series-hidden",
                "Sales Order-naming_series-default",
                "Sales Order-main-field_order",
                "Sales Order-main-default_print_format",
                "Sales Order-in_words-print_hide",
                "Sales Order-in_words-hidden",
                "Sales Order-grand_total-in_list_view",
                "Sales Order-due_date-print_hide",
                "Sales Order-disable_rounded_total-default",
                "Sales Order-delivery_date-reqd",
                "Sales Order-delivery_date-label",
                "Sales Order-delivery_date-in_list_view",
                "Sales Order-customer_name-in_list_view",
                "Sales Order-base_rounded_total-print_hide",
                "Sales Order-base_rounded_total-hidden",
                "Stock Entry Type-main-field_order",
                "Purchase Order-scan_barcode-hidden",
                "Purchase Order-rounded_total-print_hide",
                "Purchase Order-rounded_total-hidden",
                "Purchase Order-payment_schedule-print_hide",
                "Purchase Order-main-field_order",
                "Purchase Order-main-default_print_format",
                "Purchase Order-in_words-print_hide",
                "Purchase Order-in_words-hidden",
                "Purchase Order-due_date-print_hide",
                "Purchase Order-disable_rounded_total-default",
                "Purchase Order-base_rounded_total-print_hide",
                "Purchase Order-base_rounded_total-hidden",
                "Sales Invoice-workflow_state-in_list_view",
                "Sales Invoice-title-in_list_view",
                "Sales Invoice-tax_id-print_hide",
                "Sales Invoice-tax_id-hidden",
                "Sales Invoice-status-in_list_view",
                "Sales Invoice-scan_barcode-hidden",
                "Sales Invoice-rounded_total-print_hide",
                "Sales Invoice-rounded_total-hidden",
                "Sales Invoice-payment_schedule-print_hide",
                "Sales Invoice-paid_amount-in_list_view",
                "Sales Invoice-outstanding_amount-in_list_view",
                "Sales Invoice-naming_series-options",
                "Sales Invoice-naming_series-hidden",
                "Sales Invoice-naming_series-default",
                "Sales Invoice-main-field_order",
                "Sales Invoice-main-default_print_format",
                "Sales Invoice-in_words-print_hide",
                "Sales Invoice-in_words-hidden",
                "Sales Invoice-grand_total-in_list_view",
                "Sales Invoice-farm-default",
                "Sales Invoice-due_date-print_hide",
                "Sales Invoice-disable_rounded_total-default",
                "Sales Invoice-base_rounded_total-print_hide",
                "Sales Invoice-base_rounded_total-hidden",
                "Sales Invoice-additional_discount_account-mandatory_depends_on",
                "Sales Invoice-additional_discount_account-hidden",
                "Consolidated Pack List-naming_series-options",
                "Consolidated Pack List-main-field_order",
                "Consolidated Pack List-main-default_print_format",
                "Consolidated Pack List-approval_status-read_only",
                "Consolidated Pack List-approval_status-in_list_view",
                "Consolidated Pack List-approval_status-hidden",
                "Pick List Item-warehouse-in_standard_filter",
                "Pick List Item-uom-label",
                "Pick List Item-stock_qty-label",
                "Pick List Item-qty-label",
                "Pick List Item-main-field_order",
                "Delivery Note-tax_id-print_hide",
                "Delivery Note-tax_id-hidden",
                "Delivery Note-scan_barcode-hidden",
                "Delivery Note-rounded_total-print_hide",
                "Delivery Note-rounded_total-hidden",
                "Delivery Note-main-field_order",
                "Delivery Note-in_words-print_hide",
                "Delivery Note-in_words-hidden",
                "Delivery Note-disable_rounded_total-default",
                "Delivery Note-base_rounded_total-print_hide",
                "Delivery Note-base_rounded_total-hidden",
                "Delivery Note Item-target_warehouse-hidden",
                "Delivery Note Item-barcode-hidden",
                "Material Request-naming_series-options",
                "Purchase Receipt-naming_series-options",
                "Work Order-naming_series-options",
                "Employee-naming_series-options",
                "Supplier Quotation-naming_series-options",
                "Request for Quotation-naming_series-options",
                "Purchase Order-naming_series-options",
                "Purchase Invoice-naming_series-options",
                "Payment Entry-naming_series-options",
                "Bank Transaction-naming_series-default",
                "Bank Transaction-naming_series-options",
                "Request for Quotation Supplier-main-field_order",
                "Request for Quotation-message_for_supplier-fetch_from",
                "Request for Quotation-message_for_supplier-in_list_view",
                "Request for Quotation-transaction_date-in_list_view",
                "Request for Quotation-naming_series-in_list_view",
                "Request for Quotation-company-in_list_view",
                "Supplier Quotation-main-field_order",
                "Purchase Order-per_received-in_list_view",
                "Purchase Order-per_billed-in_list_view",
                "Purchase Order-grand_total-in_list_view",
                "Purchase Order-transaction_date-in_list_view",
                "Purchase Order-supplier_name-in_list_view",
                "Supplier Quotation-valid_till-in_list_view",
                "Supplier Quotation-grand_total-in_list_view",
                "Supplier Quotation-transaction_date-in_list_view",
                "Supplier Quotation-title-in_list_view",
                "Internal Delivery Note-naming_series-options",
                "Request for Quotation-billing_address-hidden",
                "Purchase Receipt Item-section_break_29-print_hide",
                "Purchase Receipt Item-section_break_29-hidden",
                "Purchase Receipt Item-amount-print_hide",
                "Purchase Receipt Item-amount-hidden",
                "Purchase Receipt Item-rate-print_hide",
                "Purchase Receipt Item-rate-hidden",
                "Purchase Receipt Item-sec_break1-print_hide",
                "Purchase Receipt Item-sec_break1-hidden",
                "Purchase Receipt Item-discount_and_margin_section-print_hide",
                "Purchase Receipt Item-discount_and_margin_section-hidden",
                "Purchase Receipt Item-rate_and_amount-print_hide",
                "Purchase Receipt Item-rate_and_amount-hidden",
                "Purchase Receipt Item-base_amount-hidden",
                "Purchase Receipt Item-main-field_order",
                "Purchase Receipt-currency_and_price_list-hidden",
                "Purchase Receipt-pricing_rule_details-hidden",
                "Purchase Receipt-sec_tax_breakup-hidden",
                "Purchase Receipt-section_break_42-hidden",
                "Purchase Receipt-section_break_46-hidden",
                "Purchase Receipt-totals-hidden",
                "Purchase Receipt-taxes_section-hidden",
                "Purchase Receipt-taxes_charges_section-hidden",
                "Purchase Receipt-net_total-hidden",
                "Purchase Receipt-total-hidden",
                "Purchase Receipt-base_total-hidden",
                "Purchase Receipt-main-field_order",
                "Purchase Order-accounting_dimensions_section-hidden",
                "Mode of Payment-type-in_list_view",
                "Mode of Payment-mode_of_payment-in_list_view",
                "Consolidated Pack List-custom_dispatch_status-in_list_view",
                "Stem Length-naming_series-options",
                "Bucket QR Code-custom_status-in_list_view",
                "Bucket QR Code-last_stock_entry-in_list_view",
                "Bucket QR Code-id-in_list_view",
                "Bucket QR Code-status-in_list_view",
                "Purchase Receipt Item-from_warehouse-hidden",
                "Purchase Invoice Item-from_warehouse-hidden",
                "POS Invoice-scan_barcode-hidden",
                "Purchase Receipt-scan_barcode-hidden",
                "Purchase Invoice-scan_barcode-hidden",
                "Stock Reconciliation-scan_barcode-hidden",
                "Pick List-scan_barcode-hidden",
                "Quotation-scan_barcode-hidden",
                "Purchase Receipt Item-barcode-hidden",
                "Stock Reconciliation Item-barcode-hidden",
                "POS Invoice Item-barcode-hidden",
                "Job Card-barcode-hidden",
                "Purchase Receipt-provisional_expense_account-hidden",
                "Budget-budget_against-options",
                "Store Requisition Voucher-scan_barcode-hidden",
                "Store Issuance Voucher-scan_barcode-hidden",
                "Inter-Farm Transfer Request-scan_barcode-hidden",
                "Purchase Invoice-payment_schedule-print_hide",
                "Purchase Invoice-due_date-print_hide",
                "Purchase Receipt-in_words-print_hide",
                "Purchase Receipt-in_words-hidden",
                "Purchase Invoice-in_words-print_hide",
                "Purchase Invoice-in_words-hidden",
                "Supplier Quotation-in_words-print_hide",
                "Supplier Quotation-in_words-hidden",
                "Quotation-in_words-print_hide",
                "Quotation-in_words-hidden",
                "Purchase Receipt-disable_rounded_total-default",
                "Purchase Receipt-rounded_total-print_hide",
                "Purchase Receipt-rounded_total-hidden",
                "Purchase Receipt-base_rounded_total-print_hide",
                "Purchase Receipt-base_rounded_total-hidden",
                "Purchase Invoice-disable_rounded_total-default",
                "Purchase Invoice-rounded_total-print_hide",
                "Purchase Invoice-rounded_total-hidden",
                "Purchase Invoice-base_rounded_total-print_hide",
                "Purchase Invoice-base_rounded_total-hidden",
                "Supplier Quotation-disable_rounded_total-default",
                "Supplier Quotation-rounded_total-print_hide",
                "Supplier Quotation-rounded_total-hidden",
                "Supplier Quotation-base_rounded_total-print_hide",
                "Supplier Quotation-base_rounded_total-hidden",
                "Quotation-disable_rounded_total-default",
                "Quotation-rounded_total-print_hide",
                "Quotation-rounded_total-hidden",
                "Quotation-base_rounded_total-print_hide",
                "Quotation-base_rounded_total-hidden",
                "Supplier-naming_series-hidden",
                "Supplier-naming_series-reqd",
            ]]
        ]
    },
    {
        "dt": "Client Script",
        "filters": [
            ["name", "in", [
                "Hooks Updater",
                "Tende Pay Statement Imports",
                "Get-Items-From-button(SI)",
                "Generate Bucket Codes",
                "Grading Stock Entry",
                "Vehicle Registration and Mileages",
                "Employee and Cost Center",
                "Hide Filter Button",
                "WHT Calculator WHT Payment Template",
                "WHT Calculator W-VAT Template",
                "Default Warehouse setting SO",
                "Sales order Consignee",
                "CPL NO OF STEMS CALC",
                "completion % on FPL",
                "OPL Stems Calc Automation to FPL",
                "Income Account Toggle",
                "FPL Completion %",
                "Available quantity in sales order",
                "Set default Target warehouse",
                "Consignee Update",
                "Sales invoice Status",
                "Chemical Request",
                "Scan QR IN SCAN",
                "Change status after save",
                "Harvest Scan V2",
                "Scan via honeywell v2",
                "Scan Via Honeywell",
                "New Form After Save",
                "Harvest Scan",
                "All harvest labels in use",
                "Sales Tracker Button",
                "Sales Order connection with FPL and OPL",
                "Calculation Of Total Stems",
                "Amount Calc Based on IGP",
                "SO Week Automation",
                "Ensure Bucket Is Scanned On Save",
                "Field Rejects Stock Entry",
                "Grading Traceability Symbols",
                "Ensure Uppercase in Bay Field",
                "Remove Read Only on Field",
                "Transfer Grading Stock",
                "Qr Code gen",
                "Scan QR Button",
                "Close Box Button",
                "Archive Employee",
                "Scan Data Field Listener",
                "Populate Number of Items",
            ]]
        ]
    },
    {
        "dt": "Server Script",
        "filters": [
            ["name", "in", [
                "greenHouseSupervisorSummary",
                "loadTruck",
                "Create Box Labels",
                "createOrUpdateFarmPackList",
                "RFQ Send CC Emails",
                "inkBirdBLE",
                "automate",
                "Get-items-from-api",
                "Delivery Note Script",
                "FetchGreenhouseByBucketId",
                "UpdateBucketStatus",
                "Credit Limit Alert",
                "Validate Stock Entry",
                "Create cpl",
                "Completeness tracker CPL",
                "Packed% on FPL",
                "sales Invoic etest",
                "Get Pick List with Farm Packlist",
                "fetch stems from opl to fpl",
                "CPL complete percentage tracker",
                "Material Transfer Submit",
                "FPL Completeness Tracker",
                "Amount Calc Based on IGP",
                "Automate Rejects Material Issue",
                "Harvest Stock Entry",
                "Stock Entry Script",
                "Stock Entry After Save",
            ]]
        ]
    },
    {
        "dt": "Print Format",
        "filters": [
            ["name", "in", [
                "test bunch label",
                "Trial Bunch Print Format",
                "Box Label - QR Code",
                "Box label1",
                "Request For Quotation KF",
                "Trial Bunch Print Format 2",
                "bunch",
                "maina bunch",
                "Test Bucket KF",
                "Test Bunch",
                "Sales invoice - KF",
                "Farm Pack List - KF",
                "Purchase Invoice KF",
                "Material Request Transfer",
                "For OPL",
                "Harvest Label Perm",
                "Sales order-KF",
                "Purchase Order KF",
                "Supplier Quotation KF",
                "Purchase Receipt KF",
                "Materials Print Format(Temp)",
                "Material Request: Transfer",
                "Transfer 1",
                "Grader QR Print format 2",
                "Grader QR Print Format",
                "Harvest Label 2",
                "Bunch QR Code",
                "Harvest Label",
                "Box Label",
                "QR Code Only",
                "Sales Invoice Print",
                "Purchase Receipt Serial and Batch Bundle Print",
                "Dunning Letter",
                "POS Invoice",
                "IRS 1099 Form",
                "Return POS Invoice",
                "Purchase eInvoice",
                "Point of Sale",
                "Pick List",
                "Sales Invoice Return",
                "Credit Note",
                "Sales Auditing Voucher",
                "Journal Auditing Voucher",
                "Bank and Cash Payment Voucher",
                "Purchase Auditing Voucher",
                "Detailed Tax Invoice",
                "Tax Invoice",
                "Simplified Tax Invoice",
                "Drop Shipping Format",
                "Payment Receipt Voucher",
                "Cheque Printing Format",
            ]]
        ]
    },
    {
        "dt": "Workflow",
        "filters": [
            ["name", "in", [
                "Material Request Workflow",
                "Purchase Order Approval Workflow 2",
                "Stores Workflow 2",
                "Sales Invoice",
                "Stores Workflow",
                "fpl",
                "Purchase Order Approval Workflow",
            ]]
        ]
    },
    {
        "dt": "Workflow Action Master",
        "filters": [
            ["name", "in", [
                "Forward to Farm Manager",
                "Submit bill for Approval",
                "Cancel",
                "Forward to Security",
                "Final Approval",
                "Submit for Approval",
                "Review",
                "Reject",
                "Approve",
            ]]
        ]
    },
    {
        "dt": "Notification",
        "filters": [
            ["name", "in", [
                "Proforma sales invoice",
                "Notify Manager on SRV Submit",
                "Notify HOD SRV is Rejected",
                "Notify Store Clerk on Security Approval",
                "Notify Manager on Inter-Farm Transfer Submit",
                "Purchase Order Finance Manager Approval Notification",
                "Purchase Order Farm Manger Approval Notification",
                "Purchase Order Director Approval Notification",
                "Purchase Order Rejected Notification",
                "Purchase Order Approved Notification",
                "SRV Approval",
                "Material Request Receipt Notification",
                "Notification for new fiscal year",
            ]]
        ]
    },
]
