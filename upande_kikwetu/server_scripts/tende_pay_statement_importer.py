import frappe
import csv
import io
import hashlib
from frappe.utils import flt, nowdate

@frappe.whitelist()
def extract_csv_data(docname, doctype):
    doc = frappe.get_doc(doctype, docname)

    if not doc.get("tende_account_statement"):
        return

    try:
        file_doc = frappe.get_doc("File", {"file_url": doc.tende_account_statement})

        if not file_doc.file_name:
            frappe.throw("Could not read file content")

        csv_content = file_doc.get_content()
        csv_reader = csv.reader(io.StringIO(csv_content))

        transactions = []

        for i, row in enumerate(csv_reader):
            if not row or len(row) < 8:
                continue
            if i <= 4:
                continue

            try:
                txn = {
                    "date": row[0],
                    "service": row[1],
                    "recipient": row[2],
                    "message": row[3],
                    "remark": row[4],
                    "ref_no": row[5],
                    "amount_in": flt(row[6].replace(',', '')) if row[6].strip() else 0,
                    "amount_out": flt(row[7].replace(',', '')) if row[7].strip() else 0,
                }
                transactions.append(txn)
            except Exception as e:
                frappe.log_error(f"Row {i} skipped: {str(e)}", "CSV Transaction Parsing Error")

        created = 0
        skipped = 0
        tende_pay_account = "140121 - Tende Pay - KF"
        counter_account = "Petty Cash Expenses - KF"

        for txn in transactions:
            if not txn["amount_in"] and not txn["amount_out"]:
                continue

            # Generate a unique hash for each transaction
            def generate_txn_hash(ref_no, date, amount):
                raw = f"{ref_no}-{date}-{amount}"
                return hashlib.md5(raw.encode()).hexdigest()

            txn_amount = txn["amount_in"] if txn["amount_in"] > 0 else txn["amount_out"]
            txn_hash = generate_txn_hash(txn["ref_no"], txn["date"], txn_amount)

            # Check for duplicate via transaction hash (requires a custom field on Journal Entry)
            existing_je = frappe.get_all(
                "Journal Entry",
                filters={
                    "custom_transaction_hash": txn_hash,
                    "docstatus": ["<", 2]
                },
                fields=["name"]
            )

            if not existing_je:
                je = frappe.new_doc("Journal Entry")
                je.voucher_type = "Journal Entry"
                je.posting_date = txn["date"].split(" ")[0] or nowdate()
                je.user_remark = txn["remark"]
                je.cheque_no = txn["ref_no"]
                je.cheque_date = txn["date"]
                je.custom_transaction_hash = txn_hash 

                if txn["amount_in"] > 0:
                    je.append("accounts", {
                        "account": tende_pay_account,
                        "debit_in_account_currency": txn["amount_in"],
                        "user_remark": txn["remark"]
                    })
                    je.append("accounts", {
                        "account": counter_account,
                        "credit_in_account_currency": txn["amount_in"],
                        "user_remark": txn["remark"]
                    })

                if txn["amount_out"] > 0:
                    je.append("accounts", {
                        "account": counter_account,
                        "debit_in_account_currency": txn["amount_out"],
                        "user_remark": txn["remark"]
                    })
                    je.append("accounts", {
                        "account": tende_pay_account,
                        "credit_in_account_currency": txn["amount_out"],
                        "user_remark": txn["remark"]
                    })

                je.flags.ignore_permissions = True
                je.insert()
                je.submit()
                created += 1
            else:
                skipped += 1

        frappe.msgprint(f"{created} Journal Entries created from CSV")
        frappe.msgprint(f"{skipped} Journal Entries skipped from CSV")

    except Exception as e:
        frappe.log_error(f"Journal Entry Import Error: {str(e)}")
        frappe.throw(f"Error processing CSV file: {str(e)}")
