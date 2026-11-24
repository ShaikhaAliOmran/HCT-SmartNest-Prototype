# HCT SmartNest — Streamlit UI/UX Prototype

A clean, educational prototype for **Capstone Section 4.2**. Built with **Python, Streamlit and pandas**. It is not a working nursery management system.

## Screens

| Screen | Actor | Requirement |
|---|---|---|
| Login | Authorized users | FR01 |
| Staff Dashboard | Nursery staff | FR05, FR07 |
| Attendance (check-in/out) | Nursery staff | FR05 |
| Child Profile | Staff / Administrator | FR03, FR04 |
| Parent View | Parent / Guardian | FR06, FR07 |
| Consent | Authorized staff / Administrator | FR15 |
| Messages | Parent / Staff | FR13 |
| Search | Staff / Administrator | FR17 |
| Reports | Staff / Administrator | FR11 |
| Notifications | Parent / Staff | FR09 |
| Pre-enrollment steps | Prospective parent | FR14 |

All screens support **NFR03 usability** through consistent navigation, clear labels, and straightforward forms.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy with Streamlit Community Cloud

1. Upload the **contents of this ZIP** to the root of your existing GitHub `streamlit-version` branch. Keep `.streamlit/config.toml` and `assets/smartnest-logo.png` in their folders.
2. In Streamlit Community Cloud, select repository `ShaikhaAliOmran/HCT-SmartNest-Prototype`, branch `streamlit-version`, and entrypoint `app.py`.
3. Deploy or reboot the existing Streamlit app after the new commit.

Your original GitHub Pages site on `main` is unaffected.

## How the code works

- `app.py`: all UI screens, sample records, navigation and demonstration interactions.
- `.streamlit/config.toml`: SmartNest color theme (royal blue sidebar, white text, light background).
- `assets/smartnest-logo.png`: original team logo.
- `requirements.txt`: required Python packages.

`st.session_state` stores demonstration changes temporarily. Refreshing/restarting the server may reset the sample data. The **Demo user** selector is not real login. This app must not contain real children’s data, credentials, medical information, or contact details. A production system needs a backend, database, verified authentication, role-based authorization, audit logging and privacy safeguards.

## Design limitations

The pre-enrollment page is informational only (FR14), not an online application. The parent view shows one fictional child. SPEA reports and direct integrations are not implemented. Screens are conceptual prototypes, not completed features.

## Suggested figure caption

*Figure 4.2.X: [Screen name] — Actor: [user role]; Requirement: [FR]. The interface allows the user to [task]. Consistent navigation and clearly labeled controls support NFR03 usability.*


## Clean branch deployment
Upload the contents of this folder to the ROOT of your new GitHub branch. Do not upload the enclosing folder. Configure Streamlit Community Cloud with the repository, the new branch name, and main file `app.py`. This build has been syntax-checked; live Streamlit interactions still require browser testing.
