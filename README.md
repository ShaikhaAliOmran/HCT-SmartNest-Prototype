# HCT SmartNest — Streamlit UI/UX Prototype

A simple Python prototype for Capstone Section 4.2. It shows the 11 requested screens and uses the project logo. The interface is deliberately practical and uses mostly native Streamlit components so students can understand and extend the code.

## Technologies
- Python: application logic
- Streamlit: interface components and navigation
- A small amount of CSS in `app.py`: colors and spacing (no JavaScript needed)
- GitHub: source code hosting
- Streamlit Community Cloud: deployment

## Files
- `app.py`: complete Python source for all 11 screens
- `requirements.txt`: Python dependency
- `assets/smartnest-logo.png`: project logo

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (new GitHub branch)
1. In the existing `HCT-SmartNest-Prototype` repository, create a branch named `streamlit-version` from `main`.
2. On that branch, upload `app.py`, `requirements.txt`, `README.md`, and the `assets` folder from this ZIP. Existing HTML/CSS/JS files can remain in the branch but are not used by Streamlit.
3. Open https://share.streamlit.io and select **Create app** / **Deploy an app**.
4. Choose your repository, branch `streamlit-version`, and entrypoint `app.py`.
5. Deploy. GitHub Pages will continue serving the HTML version from `main`.

## Screen list and functional requirements
1. Login — FR01
2. Staff Dashboard — FR05, FR07
3. Attendance — FR05
4. Child Profile — FR03, FR04
5. Parent View — FR06, FR07
6. Consent — FR15
7. Messages — FR13
8. Search — FR17
9. Reports — FR11
10. Notifications — FR09
11. Pre-enrollment — FR14

Each screen also supports usability discussion under NFR03.

## Limitations
- All names and records are fictional.
- Login and role switching are simulated; there is no real authentication or authorization.
- Demo changes use Streamlit session state and do not persist in a database.
- No real children's records, credentials, signatures, or medical information should be entered.
- This is **not** suitable for actual nursery operations. Real deployment requires secure authentication, server-side permissions, database storage, audit logging, and privacy/security testing.

## Academic integrity
Explain that this is an AI-assisted prototype if required by your course policy. Review the code, customize it, test each screen, and document your team's contributions.
