import frappe
import os
import json


@frappe.whitelist()
def update_hooks_file(docname=None):
    doctypes = [
        "Custom Field",
        "Property Setter",
        "Client Script",
        "Server Script",
        "Print Format",
        "Workflow",
        "Workflow Action Master",
        "Notification",
    ]

    customizations_map = {}

    # Include custom reports only
    try:
        custom_reports = frappe.get_all(
            "Report",
            filters={"is_standard": "No"},
            pluck="name"
        )
        if custom_reports:
            customizations_map["Report"] = custom_reports
    except Exception as e:
        frappe.log_error("Report error", str(e))

    # Get all custom DocTypes as a single fixture group
    try:
        custom_doctypes = frappe.get_all(
            "DocType", filters={"custom": 1}, pluck="name"
        )
        if custom_doctypes:
            customizations_map["DocType"] = sorted(custom_doctypes)
    except Exception as e:
        frappe.log_error("Custom Doctype error", str(e))

    # Add other doctypes normally
    for doctype in doctypes:
        try:
            records = frappe.get_all(
                doctype, fields=["name"], order_by="modified desc"
            )
            if records:
                customizations_map[doctype] = [r.name for r in records]
        except Exception as e:
            frappe.log_error(f"{doctype} error", str(e))

    # Format the fixtures block
    formatted_fixtures = "fixtures = [\n"
    for dt, names in customizations_map.items():
        if names:
            formatted_fixtures += "    {\n"
            formatted_fixtures += f"        \"dt\": \"{dt}\",\n"
            formatted_fixtures += "        \"filters\": [\n"
            formatted_fixtures += "            [\"name\", \"in\", [\n"
            for name in names:
                formatted_fixtures += f"                \"{name}\",\n"
            formatted_fixtures += "            ]]\n"
            formatted_fixtures += "        ]\n"
            formatted_fixtures += "    },\n"
    formatted_fixtures += "]\n"

    # Update customizations field in the DocType record
    if docname:
        try:
            doc = frappe.get_doc("Update hooks file", docname)
            doc.customizations = formatted_fixtures
            doc.save(ignore_permissions=True)
        except Exception as e:
            frappe.log_error("Doc update error", str(e))

    # Path to hooks.py (1 folder up from this file)
    hooks_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "hooks.py"))

    try:
        with open(hooks_path, "r") as f:
            lines = f.readlines()

        # Remove existing fixtures block using bracket tracking
        start_idx = -1
        bracket_count = 0
        for idx, line in enumerate(lines):
            if "fixtures" in line and "=" in line and "[" in line:
                start_idx = idx
                bracket_count = line.count("[") - line.count("]")
                break

        if start_idx != -1:
            end_idx = start_idx
            for i in range(start_idx + 1, len(lines)):
                bracket_count += lines[i].count("[") - lines[i].count("]")
                end_idx = i
                if bracket_count <= 0:
                    break
            del lines[start_idx:end_idx + 1]

        # Append new fixtures block
        lines.append("\n" + formatted_fixtures)

        with open(hooks_path, "w") as f:
            f.writelines(lines)

        return formatted_fixtures

    except Exception as e:
        frappe.log_error("Hooks Write Error", str(e))
        return f"❌ Failed to write to hooks.py: {e}"
