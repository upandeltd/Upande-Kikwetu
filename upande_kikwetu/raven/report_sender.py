import frappe
from frappe.utils import today
from frappe.utils.data import nowdate

def send_daily_summary(recipient_email="mathia@example.com"):
    data = frappe.db.sql(get_summary_query(), as_dict=True)
    report = format_transaction_summary(data)
    send_email_report(report, recipient_email)

def get_summary_query():
    return """
    WITH transaction_summary AS (
        -- (Your long SQL goes here, remove the extra % signs from DATE_FORMAT)
        -- Replace %%Y-%%m-%%d with %Y-%m-%d
        -- I'll truncate here for brevity
        SELECT 
            'Purchase Order' as transaction_type,
            'Buying' as category,
            COALESCE(workflow_state, 'Unknown') as document_status,
            DATE_FORMAT(MIN(transaction_date), '%Y-%m-%d') as earliest_date,
            DATE_FORMAT(MAX(transaction_date), '%Y-%m-%d') as latest_date,
            COUNT(CASE WHEN DATE(transaction_date) = CURDATE() - INTERVAL 1 DAY THEN 1 END) as yesterday_count,
            COUNT(CASE WHEN DATE(transaction_date) = CURDATE() THEN 1 END) as today_count,
            COUNT(CASE WHEN transaction_date >= NOW() - INTERVAL 7 DAY THEN 1 END) as last_7_days,
            COUNT(*) as count
        FROM `tabPurchase Order`
        GROUP BY workflow_state

        UNION ALL
        -- continue with the rest of your query
        -- just fix %%Y-%%m-%%d to %Y-%m-%d
    )
    SELECT * FROM transaction_summary
    ORDER BY category, transaction_type, 
        CASE document_status 
            WHEN 'Draft' THEN 1 
            WHEN 'Open' THEN 2 
            WHEN 'Submitted' THEN 3 
            WHEN 'Cancelled' THEN 99 
            ELSE 50 
        END;
    """

def format_transaction_summary(data):
    if not data:
        return "No activity recorded today."

    sections = {}
    for row in data:
        cat = row['category']
        sections.setdefault(cat, []).append(row)

    report = [f"📊 ERP Usage Summary — {nowdate()}\n"]
    for category, items in sections.items():
        report.append(f"\n{category}")
        for item in items:
            report.append(
                f"- {item['transaction_type']} — {item['document_status']}: {item['today_count']} today, {item['yesterday_count']} yesterday"
            )
    return "\n".join(report)

def send_email_report(message, to):
    frappe.sendmail(
        recipients=[to],
        subject=f"ERP Usage Summary — {today()}",
        message=frappe.utils.markdown(message)
    )
