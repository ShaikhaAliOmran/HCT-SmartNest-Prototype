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
    }
    handlers[page]()
    st.divider()
    st.caption("HCT SmartNest · Section 4.2 · NFR03 usability · Educational prototype")


if __name__ == "__main__":
    main()
