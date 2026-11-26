# HCT SmartNest — Iterations 1 and 2 UI/UX prototype

Python Streamlit educational prototype, updated from the user's `streamlit-clean` branch `app.py`.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy with Streamlit Community Cloud

Upload **the contents of this ZIP** to your GitHub repository branch, preserving `assets/smartnest-logo.png` and `.streamlit/config.toml`. Select that branch and `app.py` as the main file when deploying. Test in a new branch before replacing the existing deployment.

## Screens

Original 11 screens retained: Login, Staff Dashboard, Attendance, Child Profile, Parent View, Consent, Messages, Search, Reports, Notifications, Pre-enrollment.

Five added screens: User Management, Child Registration, System Monitoring, Security Management, Authorized Pick-up.

- **Administrator**: all screens, including the five additions.
- **Parent**: existing parent screens plus a read-only authorized pick-up view for the fictional linked child.
- **Staff**: original staff screens.
- **Prospective parent**: original demo login and pre-enrollment.

## Screenshot checklist for capstone Design section

1. Login — blank demo form and Enter demo result.
2. User Management — filled sample form and updated user directory.
3. Child Registration — filled fictional form and updated child list, then Child Profile/Attendance.
4. Attendance — select a child, check in/out, capture the updated attendance register.
5. System Monitoring — show simulated metrics and filtered activity events.
6. Security Management — proposed settings form and displayed saved configuration.
7. Consent — select child, save status, show current status.
8. Child Profile — edited form and saved result.
9. Authorized Pick-up — Administrator form and list, plus Parent read-only view.
10. Access Control — demonstrate role-specific sidebar visibility. This is **not** actual access control.

Use fictional names and masked contact values such as `050-XXX-1234` only.

## Critical scope limitation

This is a **UI/UX concept prototype**, not a deployed nursery information system. All records are fictional. Data are kept only in Streamlit session state; they are not persistent. Login does not verify passwords; demo role switching is not secure authorization; the proposed MFA, timeout, and access-review settings do not enforce controls; system monitoring is simulated; and authorized pick-up lists do not verify identity. Do not use with real child, parent, or staff data.
