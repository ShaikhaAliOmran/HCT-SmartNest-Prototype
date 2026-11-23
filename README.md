# HCT SmartNest — Section 4.2 UI/UX Prototype

A static, interactive **concept prototype** of 11 nursery-management screens, based on the HCT SmartNest capstone requirements. Includes the supplied project logo and consistent blue/pink/gold branding.

## Preview locally

Open `index.html` in a browser, or run `python3 -m http.server 8000` in this folder and visit `http://localhost:8000`.

## Publish with GitHub Pages

1. Create a new **public** GitHub repository (e.g. `smartnest-prototype`).
2. Upload the **contents** of this folder to the repository root: `index.html`, `styles.css`, `script.js`, `assets/`, and `README.md`.
3. In GitHub, go to **Settings → Pages**.
4. Under **Build and deployment**, select **Deploy from a branch**, then branch **main** and folder **/(root)**. Save.
5. Wait for deployment; GitHub will show your Pages URL, normally `https://YOUR-USERNAME.github.io/smartnest-prototype/`.

No packages, build process, server, or API keys are needed.

## Screens and requirements

| Screen | Actor | FR |
|---|---|---|
| Login | All authorized users (simulated) | FR01 |
| Staff Dashboard | Nursery Staff | FR05, FR07 |
| Attendance | Nursery Staff | FR05 |
| Child Profile | Staff / Administrator | FR03, FR04 |
| Parent View | Parent / Guardian | FR06, FR07 |
| Consent | Authorized Staff / Administrator | FR15 |
| Messages | Parent / Staff | FR13 |
| Search | Staff / Administrator | FR17 |
| Reports | Staff / Administrator | FR11 |
| Notifications | Parent / Staff | FR09 |
| Pre-enrollment information | Prospective Parent / Guest | FR14 |

Every page includes a report-ready caption referencing NFR03 usability. The pre-enrollment page is **information only**, not an online application.

## Important security and scope notes

- **Demonstration only.** The role selector is not authentication, authorization, or secure login.
- All child names, attendance figures, messages, and consent entries are **fictional**.
- Data changes persist in the local browser's `localStorage` only. No server, real accounts, email, or database exists.
- Never upload real child records, health data, contact details, or passwords to this prototype.
- Do not present this prototype as a deployed production nursery system.
- Production would require a secure backend, authentication, permissions, encryption, audit logging, privacy safeguards, and validated workflows.

## Design decisions for next year's implementation

This version deliberately uses **simple tables, forms, cards, and navigation**, rather than complex charts or animations. The interface is a *visual and interaction prototype* for Section 4.2, not evidence that the underlying features have been implemented.

Suggested implementation order: authentication and user roles, child records, check-in/out with timestamps, parent-linked views, then consent, messages, reporting, and notifications. Backend validation and privacy controls must be designed before any real nursery data is used.

To capture report figures, open each screen in the browser, take a screenshot, and caption it with the screen name, actor, FR number and NFR03 usability note already displayed.
