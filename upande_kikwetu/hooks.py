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
        "dt": "Client Script",
        "filters": [
            ["name", "in", ["Hide Filter Button", "Generate Bucket Codes", "OPL Stems Calc Automation to FPL",
                            "Sales invoice Status", "Chemical Request", "Scan QR IN SCAN", "Change status after save",
                            "Harvest Scan V2", "Scan via honeywell v2", "New Form After Save", "Harvest Scan", "Scan Via Honeywell",
                            "Sales Tracker Button", "Sales Order connection with FPL and OPL", "Calculation Of Total Stems",
                            "Amount Calc Based on IGP", "SO Week Automation", "Ensure Bucket Is Scanned On Save",
                            "Field Rejects Stock Entry", "Grading Traceability Symbols", "Ensure Uppercase in Bay Field",
                            "Remove Read Only on Field", "Transfer Grading Stock", "Qr Code gen", "Scan QR Button", "Close Box Button",
                            "Grading Stock Entry", "Archive Employee", "Scan Data Field Listener", "Populate Number of Items", "Consignee Update", "CPL NO OF STEMS CALC","Sales order Consignee",
                            "Income Account Toggle","Get-Items-From-button(SI)","Sales order Consignee","Available quantity in sales order"]]
        ]
    },
    {
        "dt": "Server Script",
        "filters": [
            ["name", "in", ["Delivery Note Script", "CPL complete percentage tracker", "Material Transfer Submit",
                             "Create cpl", "Amount Calc Based on IGP",
                            "Create Box Labels", "Automate Rejects Material Issue",
                            "Harvest Stock Entry", "Stock Entry Script", "Stock Entry After Save","Get Pick List with Farm Packlist","Packed% on FPL","Completeness tracker CPL"]]
        ]
    },
    {
        "dt": "DocType",
        "filters": [
            ["name", "in", ["Box Label", "Box Label Item", "Breeders", "Bunch QR Code",
                            "Bucket QR Code", "Consolidated Pack List", "Dispatch Form",
                            "Dispatch Item Form", "Farm", "Farm Pack List", "Grader QR Code",
                            "Harvest", "Item Group Price", "Label Print",
                            "Order Pick List", "Order QR Code", "Pack List Item", "Packing List",
                            "Packing Qty Confirmation", "QR Code", "QR Codes", "QR Sequence", "Rejection Reason", "SKU Summary", "Scan",
                            "Scan Check", "Scan Check List", "Scan Location", "Scanned Items", "Stem Length","Harvest Rejects","Harvest Reject Items"


                            ]]
        ]
    }
]
