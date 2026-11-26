"""HCT SmartNest | Section 4.2 interactive UI/UX prototype.

All children, contact details and records are fictional. This app deliberately
uses session state instead of a database and has no real authentication.
"""
from __future__ import annotations

from datetime import datetime
import re
from io import StringIO
from pathlib import Path
import csv
import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "assets" / "smartnest-logo.png"

st.set_page_config(page_title="HCT SmartNest | Nursery Prototype", page_icon="🏠", layout="wide", initial_sidebar_state="expanded")

# CSS is limited to visual decoration. Never hide Streamlit's main containers.
st.markdown("""
<style>
[data-testid="stSidebar"] {background: #202D91; border-right: 0;}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] span, [data-testid="stSidebar"] small,
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {color:#FFFFFF !important;}
[data-testid="stSidebar"] [data-testid="stImage"] img {
 background:white; border-radius:10px; padding:9px; max-width:170px;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
 background:#3443A3; border-color:#6773BC; color:white;
}
[data-testid="stSidebar"] [data-baseweb="select"] span {color:white !important;}
[data-testid="stSidebar"] [role="radiogroup"] label {
 padding:6px 8px; border-radius:6px; margin-bottom:2px;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
 background:#C65C7B;
}
[data-testid="stSidebar"] hr {border-color:#6471BD;}
[data-testid="stMetric"] {background:white;border:1px solid #DFE4F1;border-radius:9px;padding:16px;}
[data-testid="stForm"] {background:white;border:1px solid #DFE4F1;border-radius:9px;padding:18px;}
[data-testid="stMain"] h1,[data-testid="stMain"] h2,[data-testid="stMain"] h3 {color:#202D4A;}
[data-testid="stMain"] button[kind="primary"] {background:#202D91;border-color:#202D91;}
[data-testid="stMain"] button {border-radius:7px;}
.sn-note {background:#FFF8E8;border-left:4px solid #F0BF50;border-radius:5px;padding:10px 14px;color:#4D4A42;margin:12px 0 22px;}
.sn-kicker {color:#68758D;font-size:.91rem;margin-top:-.3rem;margin-bottom:.6rem;}
</style>
""", unsafe_allow_html=True)

SCREENS = ["Login", "Staff Dashboard", "Attendance", "Child Profile", "Parent View", "Consent", "Messages", "Search", "Reports", "Notifications", "Pre-enrollment", "User Management", "Child Registration", "System Monitoring", "Security Management", "Authorized Pick-up"]
META = {
    "Login": ("All authorized users", "FR01"),
    "Staff Dashboard": ("Nursery staff", "FR05, FR07"),
    "Attendance": ("Nursery staff", "FR05"),
    "Child Profile": ("Nursery staff / Administrator", "FR03, FR04"),
    "Parent View": ("Parent / Guardian", "FR06, FR07"),
    "Consent": ("Authorized staff / Administrator", "FR15"),
    "Messages": ("Parent / Nursery staff", "FR13"),
    "Search": ("Nursery staff / Administrator", "FR17"),
    "Reports": ("Nursery staff / Administrator", "FR11"),
    "Notifications": ("Parent / Nursery staff", "FR09"),
    "Pre-enrollment": ("Prospective parent", "FR14"),
    "User Management": ("Administrator", "Iteration 1 · User management"),
    "Child Registration": ("Administrator", "Iteration 1 · Child registration"),
    "System Monitoring": ("Administrator", "Iteration 2 · System monitoring"),
    "Security Management": ("Administrator", "Iteration 2 · Security management"),
    "Authorized Pick-up": ("Parent / Administrator", "Iteration 2 · Authorized pick-up"),
}
ROLE_PAGES = {
    "Staff": ["Login", "Staff Dashboard", "Attendance", "Child Profile", "Messages", "Search", "Reports", "Notifications", "Pre-enrollment"],
    "Parent": ["Login", "Parent View", "Authorized Pick-up", "Messages", "Notifications", "Pre-enrollment"],
    "Administrator": SCREENS,
    "Prospective parent": ["Login", "Pre-enrollment"],
}

# Sample records are small on purpose, so the prototype is easy to explain.
DEMO_CHILDREN = [
    {"ID":"SN-001","Child":"Aisha M.","Class":"Blue Room","Status":"Present","Check-in":"08:04","Check-out":"","Allergies":"None recorded","Emergency contact":"050-XXX-0101"},
    {"ID":"SN-002","Child":"Omar H.","Class":"Blue Room","Status":"Present","Check-in":"08:12","Check-out":"","Allergies":"Peanut allergy (fictional)","Emergency contact":"050-XXX-0102"},
    {"ID":"SN-003","Child":"Noor A.","Class":"Yellow Room","Status":"Absent","Check-in":"","Check-out":"","Allergies":"None recorded","Emergency contact":"050-XXX-0103"},
    {"ID":"SN-004","Child":"Salem K.","Class":"Yellow Room","Status":"Present","Check-in":"08:21","Check-out":"","Allergies":"None recorded","Emergency contact":"050-XXX-0104"},
]


def initialize():
    if "children" not in st.session_state:
        st.session_state.children = [row.copy() for row in DEMO_CHILDREN]
    if "role" not in st.session_state:
        st.session_state.role = "Staff"
    if "page" not in st.session_state:
        st.session_state.page = "Staff Dashboard"
    if "messages" not in st.session_state:
        st.session_state.messages = [{"From":"Nursery staff", "To":"Parent", "Message":"Please bring a spare change of clothes tomorrow."}]
    if "notifications" not in st.session_state:
        st.session_state.notifications = ["Weekly activity summary will be shared on Thursday.", "Please check your authorized pickup details."]
    if "consents" not in st.session_state:
        st.session_state.consents = {}
    if "users" not in st.session_state:
        st.session_state.users = [
            {"Username": "admin.demo", "Display name": "Nursery Administrator", "Role": "Administrator", "Status": "Active"},
            {"Username": "staff.demo", "Display name": "Nursery Staff", "Role": "Staff", "Status": "Active"},
            {"Username": "parent.demo", "Display name": "Sample Parent", "Role": "Parent", "Status": "Active"},
        ]
    if "pickup" not in st.session_state:
        st.session_state.pickup = [
            {"Child ID": "SN-001", "Authorized person": "Mariam A. (sample)", "Relationship": "Mother", "Phone": "050-XXX-0201", "Status": "Approved"}
        ]
    if "events" not in st.session_state:
        st.session_state.events = [{"Time": "Demo start", "Category": "System", "Event": "Sample monitoring log initialized"}]
    if "security_demo" not in st.session_state:
        st.session_state.security_demo = {"MFA required (proposed)": True, "Session timeout (minutes)": 15, "Access review (proposed)": "Monthly"}
    if "daily_updates" not in st.session_state:
        st.session_state.daily_updates = ["Story time completed this morning.", "Outdoor play completed before lunch."]


def log_event(category, event):
    """Records fictional activity in the current browser session only."""
    st.session_state.events.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Category": category, "Event": event})


def safe_demo_phone(value):
    """Allow only masked fictional numbers in the public demo."""
    return bool(re.fullmatch(r"050-XXX-\d{4}", value.strip()))


def attendance_table():
    fields = ["ID", "Child", "Class", "Status", "Check-in", "Check-out"]
    return pd.DataFrame([{key: child[key] or "—" for key in fields} for child in st.session_state.children])


def child_selector(key):
    ids = [child["ID"] for child in st.session_state.children]
    selected = st.selectbox("Select child", ids, format_func=lambda cid: next(f'{c["Child"]} · {cid}' for c in st.session_state.children if c["ID"] == cid), key=key)
    return next(child for child in st.session_state.children if child["ID"] == selected)



def go(page):
    st.session_state.pending_page = page
    st.rerun()



def section_header(page):
    actor, fr = META[page]
    st.title(page if page != "Parent View" else "Parent Dashboard")
    st.markdown(f'<div class="sn-kicker">Screen: {page} &nbsp; | &nbsp; Actor: {actor} &nbsp; | &nbsp; {fr} &nbsp; | &nbsp; NFR03 Usability</div>', unsafe_allow_html=True)


def sidebar():
    with st.sidebar:
        st.image(str(LOGO), width=155)
        st.markdown("**HCT SmartNest**")
        st.caption("Nursery management · UI/UX prototype")
        role_names = list(ROLE_PAGES)
        role = st.selectbox("Demo user", role_names, index=role_names.index(st.session_state.role))
        if role != st.session_state.role:
            st.session_state.role = role
            st.session_state.page = "Parent View" if role == "Parent" else "Pre-enrollment" if role == "Prospective parent" else "Staff Dashboard"
            st.session_state[f"nav_{role}"] = st.session_state.page
            st.rerun()
        options = ROLE_PAGES[role]
        if st.session_state.page not in options:
            st.session_state.page = options[0]
         
        pending = st.session_state.pop("pending_page", None)
        if pending is not None and pending in options:
            st.session_state.page = pending
            st.session_state[f"nav_{role}"] = pending

        chosen = st.radio("Navigation", options, index=options.index(st.session_state.page), key=f"nav_{role}")
        if chosen != st.session_state.page:
            st.session_state.page = chosen
            st.rerun()
        st.divider()
        st.caption("DEMO ONLY · Fictional child records. Role selection is not real authentication.")
    return role, st.session_state.page


def login(role):
    st.write("Select a demo user from the sidebar to explore the proposed system.")
    with st.form("login_form"):
        st.text_input("Username", value="smartnest.demo")
        st.text_input("Password (demo only)", type="password")
        submitted = st.form_submit_button("Enter demo", type="primary")
    if submitted:
        go("Parent View" if role == "Parent" else "Pre-enrollment" if role == "Prospective parent" else "Staff Dashboard")
    st.info("This is a visual login demonstration. No passwords are verified or saved.")


def dashboard():
    st.subheader("Today's nursery overview")
    children = st.session_state.children
    a, b, c, d = st.columns(4)
    a.metric("Enrolled children", len(children))
    b.metric("Present", sum(c["Status"] == "Present" for c in children))
    c.metric("Checked out", sum(c["Status"] == "Checked out" for c in children))
    d.metric("Absent", sum(c["Status"] == "Absent" for c in children))
    st.subheader("Today's attendance")
    st.dataframe(attendance_table(), width="stretch", hide_index=True)
    st.subheader("Quick actions")
    left, mid, right = st.columns(3)
    if left.button("Record attendance", width="stretch", type="primary"):
        go("Attendance")
    if mid.button("Find child", width="stretch"):
        go("Search")
    if right.button("View reports", width="stretch"):
        go("Reports")
    st.caption("Nursery staff should continue the existing identity-verification process for child pickup.")


def attendance():
    st.write("Record arrival and departure using a simple child selection and two buttons.")
    child = child_selector("attendance_child")
    st.write(f'**Current status:** {child["Status"]}  ·  **Check-in:** {child["Check-in"] or "—"}  ·  **Check-out:** {child["Check-out"] or "—"}')
    left, right = st.columns(2)
    if left.button("Check in", type="primary", disabled=child["Status"] == "Present"):
        child.update({"Status":"Present", "Check-in":datetime.now().strftime("%H:%M"), "Check-out":""})
        log_event("Attendance", f'Checked in {child["ID"]}')
        st.rerun()
    if right.button("Check out", disabled=child["Status"] != "Present"):
        child.update({"Status":"Checked out", "Check-out":datetime.now().strftime("%H:%M")})
        log_event("Attendance", f'Checked out {child["ID"]}')
        st.rerun()
    st.subheader("Attendance register")
    st.dataframe(attendance_table(), width="stretch", hide_index=True)


def profile():
    child = child_selector("profile_child")
    st.write("Edit a fictional child's basic details. Sensitive fields would require additional permissions in the real system.")
    with st.form("profile_form"):
        name = st.text_input("Child name", child["Child"])
        room = st.selectbox("Class", ["Blue Room", "Yellow Room"], index=["Blue Room", "Yellow Room"].index(child["Class"]))
        emergency = st.text_input("Emergency contact", child["Emergency contact"])
        allergies = st.text_input("Allergy note (fictional)", child["Allergies"])
        if st.form_submit_button("Save sample profile", type="primary"):
            if not name.strip():
                st.error("Child name cannot be empty.")
            else:
                child.update({"Child":name.strip(), "Class":room, "Emergency contact":emergency, "Allergies":allergies})
                log_event("Child profile", f'Updated profile {child["ID"]}')
                st.success("Sample profile updated for this session.")


def parent_view():
    child = st.session_state.children[0]  # A fixed fictional link for the parent demo.
    st.subheader("My child's information")
    a, b, c = st.columns(3)
    a.metric("Child", child["Child"])
    b.metric("Class", child["Class"])
    c.metric("Attendance today", child["Status"])
    st.write(f'**Check-in:** {child["Check-in"] or "—"} &nbsp;&nbsp; **Check-out:** {child["Check-out"] or "—"}')
    st.subheader("Daily updates")
    for item in st.session_state.daily_updates:
        st.info(item)
    st.caption("The demo parent sees only SN-001. This is simulated, not secure access control.")


def consent():
    st.write("Authorized staff record whether parental consent has been received. No real signatures are collected.")
    child = child_selector("consent_child")
    options = ["Pending", "Received", "Declined"]
    with st.form("consent_form"):
        status = st.selectbox("Parental consent status", options, index=options.index(st.session_state.consents.get(child["ID"], "Pending")))
        st.text_area("Internal note (fictional only)")
        if st.form_submit_button("Save consent status", type="primary"):
            st.session_state.consents[child["ID"]] = status
            log_event("Consent", f'Updated consent for {child["ID"]}: {status}')
            st.success("Sample consent status saved.")
    st.write("Current status:", st.session_state.consents.get(child["ID"], "Pending"))


def messages(role):
    st.write("A simple messaging demonstration between nursery staff and parents.")
    st.dataframe(pd.DataFrame(st.session_state.messages), width="stretch", hide_index=True)
    with st.form("message_form", clear_on_submit=True):
        recipient = st.selectbox("Send to", ["Nursery staff", "Parent", "Administrator"])
        message = st.text_area("Message", max_chars=300)
        if st.form_submit_button("Send sample message", type="primary"):
            if message.strip():
                st.session_state.messages.append({"From":role, "To":recipient, "Message":message.strip()})
                st.success("Sample message added.")
            else:
                st.warning("Please enter a message.")


def search():
    query = st.text_input("Search by child name or ID", placeholder="e.g. Aisha or SN-001")
    data = attendance_table()
    if query:
        data = data[data["Child"].str.contains(query, case=False, regex=False) | data["ID"].str.contains(query, case=False, regex=False)]
    st.dataframe(data, width="stretch", hide_index=True)
    st.caption("Search results exclude medical and emergency-contact details.")


def reports():
    st.subheader("Attendance summary")
    data = attendance_table()
    st.dataframe(data, width="stretch", hide_index=True)
    st.download_button("Download sample attendance CSV", data=data.to_csv(index=False), file_name="smartnest_demo_attendance.csv", mime="text/csv")
    st.caption("Demo export only. This is not an official SPEA submission.")


def notifications(role):
    for notice in st.session_state.notifications:
        st.info(notice)
    if role in ("Staff", "Administrator"):
        with st.form("notification_form", clear_on_submit=True):
            text = st.text_input("New sample announcement")
            if st.form_submit_button("Add notification", type="primary"):
                if text.strip():
                    st.session_state.notifications.insert(0, text.strip())
                    st.success("Announcement added to this session.")
                else:
                    st.warning("Enter an announcement first.")


def pre_enrollment():
    st.write("This page provides information only. Full online applications are outside the current project scope.")
    steps = [
        ("Contact the nursery", "Ask about availability, age groups and opening hours."),
        ("Review the required documents", "Request the nursery's current document checklist."),
        ("Arrange a visit", "Speak with nursery administration about the admission process."),
        ("Complete registration with the nursery", "Submit documents using the nursery's approved process."),
    ]
    for index, (heading, detail) in enumerate(steps, 1):
        with st.container(border=True):
            st.markdown(f"**Step {index} — {heading}**")
            st.write(detail)
    st.caption("No application submission, document upload or payment is included.")



def user_management():
    st.write("Administrator-only UI concept for managing demo users. No accounts are created and no passwords are stored.")
    with st.form("add_demo_user", clear_on_submit=True):
        username = st.text_input("Username (demo ID)", placeholder="e.g. teacher.demo")
        display_name = st.text_input("Display name (fictional)")
        role = st.selectbox("Assigned role", ["Staff", "Parent", "Administrator"])
        status = st.selectbox("Account status", ["Active", "Disabled"])
        submitted = st.form_submit_button("Save demo user", type="primary")
    if submitted:
        username = username.strip().lower()
        if not re.fullmatch(r"[a-z][a-z0-9._-]{2,29}", username):
            st.error("Enter a demo username of 3–30 characters, starting with a letter.")
        elif not display_name.strip():
            st.error("Enter a fictional display name.")
        elif any(row["Username"] == username for row in st.session_state.users):
            st.error("That username already exists.")
        else:
            st.session_state.users.append({"Username": username, "Display name": display_name.strip(), "Role": role, "Status": status})
            log_event("User management", f"Created sample user {username} with role {role}")
            st.success(f"Demo user {username} added to the list below.")
    st.subheader("Demo user directory — output")
    st.dataframe(pd.DataFrame(st.session_state.users), width="stretch", hide_index=True)
    st.caption("Roles in this prototype control the visible navigation only; they do not enforce backend authorization.")


def child_registration():
    st.write("Register a fictional child for the UI/UX demonstration. This is not a real nursery enrollment or permanent record.")
    with st.form("child_registration_form", clear_on_submit=True):
        name = st.text_input("Child name (fictional)", placeholder="e.g. Layla S.")
        room = st.selectbox("Assigned class", ["Blue Room", "Yellow Room"])
        allergies = st.text_input("Allergy note (fictional)", value="None recorded")
        contact = st.text_input("Emergency contact (masked sample only)", placeholder="050-XXX-1234")
        submit = st.form_submit_button("Register sample child", type="primary")
    if submit:
        if not name.strip():
            st.error("Enter a fictional child name.")
        elif not safe_demo_phone(contact):
            st.error("Use a masked sample number such as 050-XXX-1234. Do not enter real contact details.")
        else:
            next_id = max([int(row["ID"].split("-")[1]) for row in st.session_state.children] or [0]) + 1
            cid = f"SN-{next_id:03d}"
            st.session_state.children.append({"ID": cid, "Child": name.strip(), "Class": room, "Status": "Absent", "Check-in": "", "Check-out": "", "Allergies": allergies.strip() or "None recorded", "Emergency contact": contact.strip()})
            log_event("Registration", f"Registered fictional child {cid}")
            st.success(f"Registration saved for this session: {cid}. The child now appears in Child Profile and Attendance.")
    st.subheader("Registered children — output")
    st.dataframe(attendance_table(), width="stretch", hide_index=True)


def system_monitoring():
    st.write("Simulated system monitoring dashboard. These indicators are demonstration values, not live infrastructure measurements.")
    a, b, c = st.columns(3)
    a.metric("Demo application status", "Running")
    b.metric("Activity events (session)", len(st.session_state.events))
    c.metric("Demo users", len(st.session_state.users))
    st.subheader("Sample activity log — output")
    st.dataframe(pd.DataFrame(st.session_state.events), width="stretch", hide_index=True)
    with st.form("monitoring_filter"):
        category = st.selectbox("Filter activity category", ["All", "System", "Attendance", "Registration", "Child profile", "Consent", "User management", "Pick-up", "Security"])
        filter_now = st.form_submit_button("Apply filter", type="primary")
    if filter_now:
        records = [row for row in st.session_state.events if category == "All" or row["Category"] == category]
        st.write(f"Showing {len(records)} event(s) for {category}.")
        if records:
            st.dataframe(pd.DataFrame(records), width="stretch", hide_index=True)
        else:
            st.info("No demo events in this category yet.")
    st.caption("No real monitoring, uptime probes, intrusion detection, or audit logging is implemented.")


def security_management():
    st.write("Proposed security settings for the system design. Changes below update only this mock-up and do NOT enforce security.")
    settings = st.session_state.security_demo
    with st.form("security_settings"):
        mfa = st.checkbox("Require multi-factor authentication (proposed)", value=settings["MFA required (proposed)"])
        timeout = st.number_input("Proposed session timeout (minutes)", min_value=5, max_value=120, value=settings["Session timeout (minutes)"], step=5)
        review = st.selectbox("Proposed access-review frequency", ["Weekly", "Monthly", "Quarterly"], index=["Weekly", "Monthly", "Quarterly"].index(settings["Access review (proposed)"]))
        save = st.form_submit_button("Save proposed settings", type="primary")
    if save:
        st.session_state.security_demo = {"MFA required (proposed)": mfa, "Session timeout (minutes)": timeout, "Access review (proposed)": review}
        log_event("Security", "Updated proposed security settings (simulation only)")
        st.success("Proposed security configuration saved in this demo session only.")
    st.subheader("Proposed configuration — output")
    st.dataframe(pd.DataFrame([{"Setting": k, "Demo value": str(v)} for k, v in st.session_state.security_demo.items()]), width="stretch", hide_index=True)
    st.warning("Not implemented: password verification, MFA, session enforcement, secure access control, and real security monitoring.")


def authorized_pickup(role):
    st.write("Demo authorized pick-up register. Staff must verify identity through the nursery's approved real-world process.")
    if role == "Parent":
        child = st.session_state.children[0]
        st.info(f'Showing fictional authorized pick-up contacts for {child["Child"]} only.')
        records = [row for row in st.session_state.pickup if row["Child ID"] == child["ID"]]
    else:
        with st.form("pickup_form", clear_on_submit=True):
            child_id = st.selectbox("Child", [row["ID"] for row in st.session_state.children], format_func=lambda cid: next(f'{r["Child"]} · {cid}' for r in st.session_state.children if r["ID"] == cid))
            person = st.text_input("Authorized person's name (fictional)")
            relationship = st.selectbox("Relationship", ["Mother", "Father", "Guardian", "Grandparent", "Other"])
            phone = st.text_input("Phone (masked sample only)", placeholder="050-XXX-1234")
            status = st.selectbox("Approval status", ["Pending", "Approved", "Revoked"])
            save = st.form_submit_button("Save sample pick-up contact", type="primary")
        if save:
            if not person.strip():
                st.error("Enter a fictional contact name.")
            elif not safe_demo_phone(phone):
                st.error("Use a masked sample phone number such as 050-XXX-1234.")
            else:
                st.session_state.pickup.append({"Child ID": child_id, "Authorized person": person.strip(), "Relationship": relationship, "Phone": phone.strip(), "Status": status})
                log_event("Pick-up", f"Saved sample pick-up contact for {child_id}: {status}")
                st.success("Sample authorized pick-up contact saved below.")
        records = st.session_state.pickup
    st.subheader("Authorized pick-up list — output")
    if records:
        st.dataframe(pd.DataFrame(records), width="stretch", hide_index=True)
    else:
        st.info("No sample pick-up contacts found.")
    st.caption("This screen is not proof of identity or permission to release a child.")


def main():
    initialize()
    role, page = sidebar()
    section_header(page)
    st.markdown('<div class="sn-note">UI/UX CONCEPT PROTOTYPE · Fictional records only · No real authentication, database, or access control.</div>', unsafe_allow_html=True)
    handlers = {
        "Login": lambda: login(role),
        "Staff Dashboard": dashboard,
        "Attendance": attendance,
        "Child Profile": profile,
        "Parent View": parent_view,
        "Consent": consent,
        "Messages": lambda: messages(role),
        "Search": search,
        "Reports": reports,
        "Notifications": lambda: notifications(role),
        "Pre-enrollment": pre_enrollment,
        "User Management": user_management,
        "Child Registration": child_registration,
        "System Monitoring": system_monitoring,
        "Security Management": security_management,
        "Authorized Pick-up": lambda: authorized_pickup(role),
    }
    handlers[page]()
    st.divider()
    st.caption("HCT SmartNest · Section 4.2 · NFR03 usability · Educational prototype")


if __name__ == "__main__":
    main()
