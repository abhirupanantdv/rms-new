# import frappe
# from frappe.utils import get_url_to_form


# def get_recipients():
#     return frappe.get_all(
#         "Email Group Member",
#         filters={"email_group": "Issue Notification"},
#         pluck="email"
#     )


# def issue_created(doc, method=None):
#     recipients = get_recipients()

#     frappe.sendmail(
#         recipients=recipients,
#         subject=f"New Issue Created - {doc.name}",
#         message=f"""
#         A new Issue has been created.<br><br>

#         <b>Issue:</b> {doc.name}<br>
#         <b>Subject:</b> {doc.subject}<br><br>

#         <a href="{get_url_to_form('Issue', doc.name)}">Open Issue</a>
#         """,
#         now=True
#     )

# def issue_comment_added(doc, method=None):
#     if doc.reference_doctype != "Issue":
#         return

#     recipients = get_recipients()
#     issue = frappe.get_doc("Issue", doc.reference_name)

#     comments = frappe.get_all(
#         "Comment",
#         filters={
#             "reference_doctype": "Issue",
#             "reference_name": issue.name
#         },
#         fields=["owner", "creation", "content"],
#         order_by="creation asc"
#     )

#     comment_history = ""

#     for idx, c in enumerate(comments, start=1):
#         comment_history += f"""
#         <div style="margin-bottom:15px;padding:10px;border:1px solid #ddd;">
#             <b>Comment {idx}</b><br>
#             <b>By:</b> {c.owner}<br>
#             <b>Date:</b> {frappe.utils.format_datetime(c.creation)}<br><br>
#             {c.content}
#         </div>
#         """

#     frappe.sendmail(
#         recipients=recipients,
#         subject=f"Issue Updated - {issue.name}",
#         message=f"""
#         <h3>Issue Updated</h3>

#         <b>Issue:</b> {issue.name}<br>
#         <b>Subject:</b> {issue.subject}<br><br>

#         <h4>Comment History</h4>

#         {comment_history}

#         <br>

#         <a href="{get_url_to_form('Issue', issue.name)}">
#             Open Issue
#         </a>
#         """,
#         now=True
#     )


# import frappe
# from frappe.utils import get_url_to_form, format_datetime


# def get_recipients(issue=None):
#     recipients = frappe.get_all(
#         "Email Group Member",
#         filters={"email_group": "Issue Notification"},
#         pluck="email"
#     )
#     if issue and issue.contact:
#         contact_email = frappe.db.get_value(
#             "Contact",
#             issue.contact,
#             "email_id"
#         )
#         if contact_email:
#             recipients.append(contact_email)
#     return list(set(filter(None, recipients)))


# def issue_created(doc, method=None):
#     recipients = get_recipients(doc)
#     if not recipients:
#         return
#     frappe.sendmail(
#         recipients=recipients,
#         subject=f"New Issue Created - {doc.name}",
#         message=f"""
#         <h3>New Issue Created</h3>

#         <table border="1" cellpadding="5" cellspacing="0">
#             <tr>
#                 <td><b>Issue</b></td>
#                 <td>{doc.name}</td>
#             </tr>
#             <tr>
#                 <td><b>Subject</b></td>
#                 <td>{doc.subject or ""}</td>
#             </tr>
#             <tr>
#                 <td><b>Status</b></td>
#                 <td>{doc.status or ""}</td>
#             </tr>
#             <tr>
#                 <td><b>Priority</b></td>
#                 <td>{doc.priority or ""}</td>
#             </tr>
#         </table>
#         <br>
#         <a href="{get_url_to_form('Issue', doc.name)}">
#             Open Issue
#         </a>
#         """,
#         now=True
#     )


# def issue_comment_added(doc, method=None):
#     if doc.reference_doctype != "Issue":
#         return
#     issue = frappe.get_doc("Issue", doc.reference_name)
#     recipients = get_recipients(issue)
#     if not recipients:
#         return
#     comments = frappe.get_all(
#         "Comment",
#         filters={
#             "reference_doctype": "Issue",
#             "reference_name": issue.name
#         },
#         fields=[
#             "owner",
#             "creation",
#             "content"
#         ],
#         order_by="creation asc"
#     )
#     comment_history = ""
#     for i, c in enumerate(comments, start=1):
#         comment_history += f"""
#         <div style="border:1px solid #ddd;padding:10px;margin-bottom:10px;">
#             <b>Comment {i}</b><br>
#             <b>By:</b> {c.owner}<br>
#             <b>Date:</b> {format_datetime(c.creation)}<br><br>
#             {c.content}
#         </div>
#         """
#     frappe.sendmail(
#         recipients=recipients,
#         subject=f"Issue Updated - {issue.name}",
#         message=f"""
#         <h3>Issue Updated</h3>

#         <table border="1" cellpadding="5" cellspacing="0">
#             <tr>
#                 <td><b>Issue</b></td>
#                 <td>{issue.name}</td>
#             </tr>
#             <tr>
#                 <td><b>Subject</b></td>
#                 <td>{issue.subject or ""}</td>
#             </tr>
#             <tr>
#                 <td><b>Status</b></td>
#                 <td>{issue.status or ""}</td>
#             </tr>
#         </table>

#         <br>

#         <h3>Comment History</h3>

#         {comment_history}

#         <br>

#         <a href="{get_url_to_form('Issue', issue.name)}">
#             Open Issue
#         </a>
#         """,
#         now=True
#     )
# //////////////////////////////////////////////////////////////////////////////////
# import frappe
# from frappe.utils import get_url_to_form, format_datetime, escape_html


# EMAIL_GROUP = "Issue Notification"


# def get_recipients(issue=None):
#     recipients = frappe.get_all(
#         "Email Group Member",
#         filters={"email_group": EMAIL_GROUP},
#         pluck="email",
#     )
#     contact = getattr(issue, "contact", None) if issue else None
#     if contact:
#         contact_email = frappe.db.get_value(
#             "Contact",
#             contact,
#             "email_id",
#         )
#         if contact_email:
#             recipients.append(contact_email)
#     return list(set(filter(None, recipients)))

# def get_safe_value(value):
#     if value is None:
#         return ""
#     return escape_html(str(value))
# def get_status_badge(status):
#     status = get_safe_value(status or "Open")
#     return f"""
#         <span style="
#             display:inline-block;
#             background:#dbeafe;
#             color:#1e40af;
#             padding:5px 12px;
#             border-radius:20px;
#             font-size:12px;
#             font-weight:600;
#         ">
#             {status}
#         </span>
#     """
# def get_priority_badge(priority):
#     priority_text = priority or "Not Set"
#     safe_priority = get_safe_value(priority_text)
#     priority_colors = {
#         "Low": {
#             "background": "#dcfce7",
#             "color": "#166534",
#         },
#         "Medium": {
#             "background": "#fef3c7",
#             "color": "#92400e",
#         },
#         "High": {
#             "background": "#fee2e2",
#             "color": "#b91c1c",
#         },
#         "Urgent": {
#             "background": "#fecaca",
#             "color": "#991b1b",
#         },
#     }
#     colors = priority_colors.get(
#         priority_text,
#         {
#             "background": "#f3f4f6",
#             "color": "#374151",
#         },
#     )
#     return f"""
#         <span style="
#             display:inline-block;
#             background:{colors["background"]};
#             color:{colors["color"]};
#             padding:5px 12px;
#             border-radius:20px;
#             font-size:12px;
#             font-weight:600;
#         ">
#             {safe_priority}
#         </span>
#     """

# def get_comment_history(issue_name):
#     comments = frappe.get_all(
#         "Comment",
#         filters={
#             "reference_doctype": "Issue",
#             "reference_name": issue_name,
#             "comment_type": "Comment",
#         },
#         fields=[
#             "owner",
#             "creation",
#             "content",
#         ],
#         order_by="creation asc",
#     )
#     if not comments:
#         return """
#             <div style="
#                 background:#f9fafb;
#                 border:1px dashed #d1d5db;
#                 border-radius:6px;
#                 padding:18px;
#                 text-align:center;
#                 color:#6b7280;
#                 font-size:14px;
#             ">
#                 No comments have been added yet.
#             </div>
#         """
#     comment_history = ""
#     for index, comment in enumerate(comments, start=1):
#         owner_name = frappe.db.get_value(
#             "User",
#             comment.owner,
#             "full_name",
#         ) or comment.owner

#         safe_owner = get_safe_value(owner_name)
#         safe_owner_email = get_safe_value(comment.owner)
#         comment_date = format_datetime(comment.creation)
#         comment_content = comment.content or ""
#         comment_history += f"""
#             <div style="
#                 border:1px solid #e5e7eb;
#                 border-radius:8px;
#                 margin-bottom:14px;
#                 overflow:hidden;
#                 background:#ffffff;
#             ">

#                 <div style="
#                     background:#f8fafc;
#                     border-bottom:1px solid #e5e7eb;
#                     padding:10px 14px;
#                 ">
#                     <table style="
#                         width:100%;
#                         border-collapse:collapse;
#                         font-size:13px;
#                     ">
#                         <tr>
#                             <td style="
#                                 color:#1f2937;
#                                 font-weight:600;
#                             ">
#                                 Comment {index}
#                             </td>

#                             <td style="
#                                 text-align:right;
#                                 color:#6b7280;
#                             ">
#                                 {comment_date}
#                             </td>
#                         </tr>
#                     </table>
#                 </div>

#                 <div style="padding:14px 16px;">

#                     <div style="
#                         margin-bottom:10px;
#                         font-size:13px;
#                         color:#4b5563;
#                     ">
#                         <strong style="color:#111827;">
#                             {safe_owner}
#                         </strong>

#                         <span style="color:#9ca3af;">
#                             &nbsp;({safe_owner_email})
#                         </span>
#                     </div>

#                     <div style="
#                         color:#374151;
#                         font-size:14px;
#                         line-height:1.6;
#                         word-break:break-word;
#                     ">
#                         {comment_content}
#                     </div>

#                 </div>

#             </div>
#         """

#     return comment_history

# def build_issue_email(
#     issue,
#     heading,
#     introduction,
#     comment_history="",
#     show_comments=False,
# ):
#     issue_name = get_safe_value(issue.name)
#     subject = get_safe_value(issue.subject)
#     owner = get_safe_value(issue.owner)
#     contact = get_safe_value(getattr(issue, "contact", None))
#     raised_by = get_safe_value(getattr(issue, "raised_by", None))

#     status_badge = get_status_badge(issue.status)
#     priority_badge = get_priority_badge(issue.priority)
#     issue_url = get_url_to_form("Issue", issue.name)
#     comments_section = ""
#     if show_comments:
#         comments_section = f"""
#             <div style="margin-top:28px;">

#                 <h3 style="
#                     color:#1e3a8a;
#                     font-size:17px;
#                     margin:0 0 15px 0;
#                     padding-bottom:9px;
#                     border-bottom:2px solid #e5e7eb;
#                 ">
#                     Comment History
#                 </h3>

#                 {comment_history}

#             </div>
#         """

#     return f"""
#         <div style="
#             margin:0;
#             padding:25px 10px;
#             background:#f4f6f9;
#             font-family:Arial,Helvetica,sans-serif;
#             color:#1f2937;
#         ">

#             <div style="
#                 max-width:800px;
#                 margin:0 auto;
#                 background:#ffffff;
#                 border-radius:10px;
#                 border:1px solid #dbe1e8;
#                 overflow:hidden;
#                 box-shadow:0 4px 14px rgba(0,0,0,0.06);
#             ">

#                 <div style="
#                     background:#2563eb;
#                     color:#ffffff;
#                     padding:20px 24px;
#                 ">
#                     <div style="
#                         font-size:12px;
#                         text-transform:uppercase;
#                         letter-spacing:1px;
#                         opacity:0.85;
#                         margin-bottom:5px;
#                     ">
#                         ERPNext Issue Management
#                     </div>

#                     <h2 style="
#                         margin:0;
#                         font-size:22px;
#                         line-height:1.3;
#                     ">
#                         {heading}
#                     </h2>
#                 </div>

#                 <div style="padding:24px;">

#                     <p style="
#                         margin:0 0 20px 0;
#                         color:#4b5563;
#                         font-size:14px;
#                         line-height:1.6;
#                     ">
#                         {introduction}
#                     </p>

#                     <table style="
#                         width:100%;
#                         border-collapse:collapse;
#                         font-size:14px;
#                     ">

#                         <tr>
#                             <td style="
#                                 width:30%;
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 background:#f8fafc;
#                                 font-weight:600;
#                                 color:#374151;
#                             ">
#                                 Issue
#                             </td>

#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 color:#111827;
#                                 font-weight:600;
#                             ">
#                                 {issue_name}
#                             </td>
#                         </tr>

#                         <tr>
#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 background:#f8fafc;
#                                 font-weight:600;
#                                 color:#374151;
#                             ">
#                                 Subject
#                             </td>

#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 color:#111827;
#                             ">
#                                 {subject}
#                             </td>
#                         </tr>

#                         <tr>
#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 background:#f8fafc;
#                                 font-weight:600;
#                                 color:#374151;
#                             ">
#                                 Issue Owner
#                             </td>

#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 color:#111827;
#                             ">
#                                 {owner}
#                             </td>
#                         </tr>

#                         <tr>
#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 background:#f8fafc;
#                                 font-weight:600;
#                                 color:#374151;
#                             ">
#                                 Contact
#                             </td>

#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 color:#111827;
#                             ">
#                                 {contact or "Not specified"}
#                             </td>
#                         </tr>

#                         <tr>
#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 background:#f8fafc;
#                                 font-weight:600;
#                                 color:#374151;
#                             ">
#                                 Raised By
#                             </td>

#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 color:#111827;
#                             ">
#                                 {raised_by or "Not specified"}
#                             </td>
#                         </tr>

#                         <tr>
#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 background:#f8fafc;
#                                 font-weight:600;
#                                 color:#374151;
#                             ">
#                                 Status
#                             </td>

#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                             ">
#                                 {status_badge}
#                             </td>
#                         </tr>

#                         <tr>
#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                                 background:#f8fafc;
#                                 font-weight:600;
#                                 color:#374151;
#                             ">
#                                 Priority
#                             </td>

#                             <td style="
#                                 padding:11px 12px;
#                                 border:1px solid #e5e7eb;
#                             ">
#                                 {priority_badge}
#                             </td>
#                         </tr>

#                     </table>

#                     {comments_section}

#                     <div style="
#                         text-align:center;
#                         margin-top:28px;
#                     ">

#                         <a
#                             href="{issue_url}"
#                             style="
#                                 background:#2563eb;
#                                 color:#ffffff;
#                                 padding:12px 26px;
#                                 text-decoration:none;
#                                 border-radius:6px;
#                                 font-size:14px;
#                                 font-weight:600;
#                                 display:inline-block;
#                             "
#                         >
#                             Open Issue in ERPNext
#                         </a>

#                     </div>

#                 </div>

#                 <div style="
#                     background:#f3f4f6;
#                     border-top:1px solid #e5e7eb;
#                     padding:14px 20px;
#                     text-align:center;
#                     font-size:12px;
#                     color:#6b7280;
#                     line-height:1.5;
#                 ">
#                     This is an automated notification from ERPNext.
#                     Please do not reply unless the sender mailbox is monitored.
#                 </div>

#             </div>

#         </div>
#     """

# def issue_created(doc, method=None):
#     recipients = get_recipients(doc)
#     if not recipients:
#         return
#     message = build_issue_email(
#         issue=doc,
#         heading="New Issue Created",
#         introduction=(
#             "A new issue has been created "
#             "The issue details are provided below."
#         ),
#     )

#     frappe.sendmail(
#         recipients=recipients,
#         subject=f"New Issue Created - {doc.name}",
#         message=message,
#         reference_doctype="Issue",
#         reference_name=doc.name,
#         now=True,
#     )


# def issue_comment_added(doc, method=None):

#     if doc.reference_doctype != "Issue":
#         return

#     if doc.comment_type != "Comment":
#         return

#     if not doc.reference_name:
#         return

#     issue = frappe.get_doc(
#         "Issue",
#         doc.reference_name,
#     )

#     recipients = get_recipients(issue)

#     if not recipients:
#         return

#     comment_history = get_comment_history(issue.name)

#     message = build_issue_email(
#         issue=issue,
#         heading="Issue Updated",
#         introduction=(
#             "A new comment has been added to this issue. "
#             "Review the issue details and complete comment history below."
#         ),
#         comment_history=comment_history,
#         show_comments=True,
#     )

#     frappe.sendmail(
#         recipients=recipients,
#         subject=f"Issue Updated - {issue.name}",
#         message=message,
#         reference_doctype="Issue",
#         reference_name=issue.name,
#         now=True,
#     )




# final 
import frappe
from frappe.utils import escape_html, format_datetime, get_url_to_form

EMAIL_GROUP = "Issue Notification"


def get_safe_value(value, default=""):
    if value in (None, ""):
        value = default
    return escape_html(str(value))


def get_recipients(issue=None):
    recipients = frappe.get_all(
        "Email Group Member",
        filters={"email_group": EMAIL_GROUP},
        pluck="email"
    )
    contact = getattr(issue, "contact", None) if issue else None
    if contact:
        contact_email = frappe.db.get_value(
            "Contact",
            contact,
            "email_id"
        )
        if contact_email:
            recipients.append(contact_email)
    return sorted({
        email.strip()
        for email in recipients
        if email and email.strip()
    })


def get_status_badge(status):
    status_text = status or "Open"
    safe_status = get_safe_value(status_text)
    return f"""
    <span style="display:inline-block;background:#dbeafe;color:#1e40af;padding:5px 12px;border-radius:20px;font-size:12px;font-weight:600;">
        {safe_status}
    </span>
    """


def get_priority_badge(priority):
    priority_text = priority or "Not Set"
    safe_priority = get_safe_value(priority_text)

    priority_colors = {
        "Low": {
            "background": "#dcfce7",
            "color": "#166534"
        },
        "Medium": {
            "background": "#fef3c7",
            "color": "#92400e"
        },
        "High": {
            "background": "#fee2e2",
            "color": "#b91c1c"
        },
        "Urgent": {
            "background": "#fecaca",
            "color": "#991b1b"
        }
    }

    colors = priority_colors.get(
        priority_text,
        {
            "background": "#f3f4f6",
            "color": "#374151"
        }
    )
    return f"""
    <span style="display:inline-block;background:{colors["background"]};color:{colors["color"]};padding:5px 12px;border-radius:20px;font-size:12px;font-weight:600;">
        {safe_priority}
    </span>
    """


def get_comment_history(issue_name):
    comments = frappe.get_all(
        "Comment",
        filters={
            "reference_doctype": "Issue",
            "reference_name": issue_name,
            "comment_type": "Comment"
        },
        fields=[
            "owner",
            "creation",
            "content"
        ],
        order_by="creation asc"
    )

    if not comments:
        return """
        <div style="background:#f9fafb;border:1px dashed #d1d5db;border-radius:6px;padding:18px;text-align:center;color:#6b7280;font-size:14px;">
            No comments have been added yet.
        </div>
        """

    owners = list({
        comment.owner
        for comment in comments
        if comment.owner
    })
    user_names = {}
    if owners:
        users = frappe.get_all(
            "User",
            filters={"name": ["in", owners]},
            fields=["name", "full_name"]
        )
        user_names = {
            user.name: user.full_name or user.name
            for user in users
        }
    comment_blocks = []
    for index, comment in enumerate(comments, start=1):
        owner_email = comment.owner or ""
        owner_name = user_names.get(owner_email, owner_email)
        safe_owner = get_safe_value(
            owner_name,
            "Unknown User"
        )
        safe_owner_email = get_safe_value(owner_email)
        comment_date = get_safe_value(
            format_datetime(comment.creation)
        )
        comment_content = comment.content or ""
        comment_blocks.append(
            f"""
            <div style="border:1px solid #e5e7eb;border-radius:8px;margin-bottom:14px;overflow:hidden;background:#ffffff;">
                <div style="background:#f8fafc;border-bottom:1px solid #e5e7eb;padding:10px 14px;">
                    <table style="width:100%;border-collapse:collapse;font-size:13px;">
                        <tr>
                            <td style="color:#1f2937;font-weight:600;">
                                Comment {index}
                            </td>
                            <td style="text-align:right;color:#6b7280;">
                                {comment_date}
                            </td>
                        </tr>
                    </table>
                </div>

                <div style="padding:14px 16px;">
                    <div style="margin-bottom:10px;font-size:13px;color:#4b5563;">
                        <strong style="color:#111827;">
                            {safe_owner}
                        </strong>
                        <span style="color:#9ca3af;">
                            ({safe_owner_email})
                        </span>
                    </div>

                    <div style="color:#374151;font-size:14px;line-height:1.6;word-break:break-word;">
                        {comment_content}
                    </div>
                </div>
            </div>
            """
        )

    return "".join(comment_blocks)

def build_issue_email(
    issue,
    heading,
    introduction,
    comment_history="",
    show_comments=False
):
    issue_name = get_safe_value(
        getattr(issue, "name", None)
    )
    subject = get_safe_value(
        getattr(issue, "subject", None),
        "No subject"
    )
    owner = get_safe_value(
        getattr(issue, "owner", None),
        "Not specified"
    )
    contact = get_safe_value(
        getattr(issue, "contact", None),
        "Not specified"
    )
    status_badge = get_status_badge(
        getattr(issue, "status", None)
    )
    priority_badge = get_priority_badge(
        getattr(issue, "priority", None)
    )
    issue_url = get_url_to_form(
        "Issue",
        issue.name
    )
    safe_heading = get_safe_value(heading)
    safe_introduction = get_safe_value(introduction)
    comments_section = ""
    if show_comments:
        comments_section = f"""
        <div style="margin-top:28px;">
            <h3 style="color:#1e3a8a;font-size:17px;margin:0 0 15px 0;padding-bottom:9px;border-bottom:2px solid #e5e7eb;">
                Comment History
            </h3>

            {comment_history}
        </div>
        """
    return f"""
    <div style="margin:0;padding:25px 10px;background:#f4f6f9;font-family:Arial,Helvetica,sans-serif;color:#1f2937;">
        <div style="max-width:800px;margin:0 auto;background:#ffffff;border-radius:10px;border:1px solid #dbe1e8;overflow:hidden;box-shadow:0 4px 14px rgba(0,0,0,0.06);">

            <div style="background:#2563eb;color:#ffffff;padding:20px 24px;">
                <div style="font-size:12px;text-transform:uppercase;letter-spacing:1px;opacity:0.85;margin-bottom:5px;">
                    Service Desk & Issue Resolution
                </div>

                <h2 style="margin:0;font-size:22px;line-height:1.3;color:#ffffff;">
                    {safe_heading}
                </h2>
            </div>

            <div style="padding:24px;">
                <p style="margin:0 0 20px 0;color:#4b5563;font-size:14px;line-height:1.6;">
                    {safe_introduction}
                </p>

                <table style="width:100%;border-collapse:collapse;font-size:14px;">
                    <tr>
                        <td style="width:30%;padding:11px 12px;border:1px solid #e5e7eb;background:#f8fafc;font-weight:600;color:#374151;">
                            Issue
                        </td>
                        <td style="padding:11px 12px;border:1px solid #e5e7eb;color:#111827;font-weight:600;">
                            {issue_name}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:11px 12px;border:1px solid #e5e7eb;background:#f8fafc;font-weight:600;color:#374151;">
                            Subject
                        </td>
                        <td style="padding:11px 12px;border:1px solid #e5e7eb;color:#111827;">
                            {subject}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:11px 12px;border:1px solid #e5e7eb;background:#f8fafc;font-weight:600;color:#374151;">
                            Issue Owner
                        </td>
                        <td style="padding:11px 12px;border:1px solid #e5e7eb;color:#111827;">
                            {owner}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:11px 12px;border:1px solid #e5e7eb;background:#f8fafc;font-weight:600;color:#374151;">
                            Contact
                        </td>
                        <td style="padding:11px 12px;border:1px solid #e5e7eb;color:#111827;">
                            {contact}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:11px 12px;border:1px solid #e5e7eb;background:#f8fafc;font-weight:600;color:#374151;">
                            Status
                        </td>
                        <td style="padding:11px 12px;border:1px solid #e5e7eb;">
                            {status_badge}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:11px 12px;border:1px solid #e5e7eb;background:#f8fafc;font-weight:600;color:#374151;">
                            Priority
                        </td>
                        <td style="padding:11px 12px;border:1px solid #e5e7eb;">
                            {priority_badge}
                        </td>
                    </tr>
                </table>

                {comments_section}

                <div style="text-align:center;margin-top:28px;">
                    <a href="{issue_url}" style="background:#2563eb;color:#ffffff;padding:12px 26px;text-decoration:none;border-radius:6px;font-size:14px;font-weight:600;display:inline-block;">
                        Open Issue
                    </a>
                </div>
            </div>

            <div style="background:#f3f4f6;border-top:1px solid #e5e7eb;padding:14px 20px;text-align:center;font-size:12px;color:#6b7280;line-height:1.5;">
                This is an automated notification from Ductus.
                Please do not reply unless the sender mailbox is monitored.
            </div>

        </div>
    </div>
    """

def send_issue_email(
    recipients,
    subject,
    message,
    issue_name,
    error_title
):
    if not recipients:
        return

    try:
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            message=message,
            reference_doctype="Issue",
            reference_name=issue_name
        )

    except Exception:
        frappe.log_error(
            message=frappe.get_traceback(),
            title=error_title
        )


def issue_created(doc, method=None):
    recipients = get_recipients(doc)
    if not recipients:
        return
    message = build_issue_email(
        issue=doc,
        heading="New Issue Created",
        introduction=(
            "A new issue has been created. "
            "The issue details are provided below."
        )
    )
    send_issue_email(
        recipients=recipients,
        subject=f"New Issue Created - {doc.name}",
        message=message,
        issue_name=doc.name,
        error_title="Issue Creation Email Failed"
    )

def issue_comment_added(doc, method=None):
    if getattr(doc, "reference_doctype", None) != "Issue":
        return
    if getattr(doc, "comment_type", None) != "Comment":
        return
    issue_name = getattr(
        doc,
        "reference_name",
        None
    )
    if not issue_name:
        return
    if not frappe.db.exists("Issue", issue_name):
        return
    issue = frappe.get_doc(
        "Issue",
        issue_name
    )
    recipients = get_recipients(issue)
    if not recipients:
        return
    comment_history = get_comment_history(
        issue.name
    )
    message = build_issue_email(
        issue=issue,
        heading="Issue Updated",
        introduction=(
            "A new comment has been added to this issue. "
            "Review the issue details and complete comment history below."
        ),
        comment_history=comment_history,
        show_comments=True
    )
    send_issue_email(
        recipients=recipients,
        subject=f"Issue Updated - {issue.name}",
        message=message,
        issue_name=issue.name,
        error_title="Issue Comment Email Failed"
    )