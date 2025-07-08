import frappe
import os
import json
import re


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
    skipped_duplicates = {}

    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "upande_kikwetu"))

    def to_snake_case(name):
        return re.sub(r'[\W]+', '_', name.strip()).lower()

    def is_already_exported(doctype, name):
        folder_name = to_snake_case(name)
        doctype_folder = doctype.lower().replace(" ", "_")

        possible_dirs = [
            os.path.join(app_path, "custom", doctype_folder, folder_name),
            os.path.join(app_path, "doctype", folder_name),
            os.path.join(app_path, folder_name),
        ]
        return any(os.path.isdir(path) for path in possible_dirs)

    def record_skipped(dt, name):
        skipped_duplicates.setdefault(dt, []).append(name)

    # Include custom reports only
    try:
        custom_reports = frappe.get_all("Report", filters={"is_standard": "No"}, pluck="name")
        filtered = []
        for r in custom_reports:
            if is_already_exported("Report", r):
                record_skipped("Report", r)
            else:
                filtered.append(r)
        if filtered:
            customizations_map["Report"] = filtered
    except Exception as e:
        frappe.log_error("Report error", str(e))

    # Include custom doctypes
    try:
        custom_doctypes = frappe.get_all("DocType", filters={"custom": 1}, pluck="name")
        filtered = []
        for dt in custom_doctypes:
            if is_already_exported("DocType", dt):
                record_skipped("DocType", dt)
            else:
                filtered.append(dt)
        if filtered:
            customizations_map["DocType"] = sorted(filtered)
    except Exception as e:
        frappe.log_error("Custom Doctype error", str(e))

    # Add normal doctypes
    for doctype in doctypes:
        try:
            records = frappe.get_all(doctype, fields=["name"], order_by="modified desc")
            filtered = []
            for r in records:
                if is_already_exported(doctype, r.name):
                    record_skipped(doctype, r.name)
                else:
                    filtered.append(r.name)
            if filtered:
                customizations_map[doctype] = filtered
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

    # Path to hooks.py
    hooks_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hooks.py"))

    try:
        with open(hooks_path, "r") as f:
            lines = f.readlines()

        # Remove existing fixtures block
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

        lines.append("\n" + formatted_fixtures)

        with open(hooks_path, "w") as f:
            f.writelines(lines)

    except Exception as e:
        frappe.log_error("Hooks Write Error", str(e))
        return f"❌ Failed to write to hooks.py: {e}"

    return {
        "fixtures": formatted_fixtures,
        "skipped": skipped_duplicates,
    }
