# FSD – Frontend Static Directory

This document describes the **FSD** (Frontend Static Directory) used by the Resume Maker app. The Flask app serves these files as static assets and pages (see `config/app_config.py`: `FSD_DIR`, `HTML_DIR`, `CSS_DIR`, `JS_DIR`, `IMG_DIR`; `app.py` sets `static_folder=FSD_DIR`). **No other files were changed.**

---

## 1. Purpose

FSD holds all frontend static files:

- **HTML** – Page markup (landing, auth, dashboard, resume steps, templates, etc.)
- **CSS** – Styles per page and per resume template
- **JS** – Scripts for pages, resume builder, templates, and shared logic
- **IMG** – Images (e.g. template thumbnails)
- **templates/** – Resume layout templates (each with `template.html` and `style.css`)

Flask serves FSD via `page_controller` (HTML from `HTML_DIR`) and the app’s `static_folder=FSD_DIR`, so URLs map to files under `FSD/`.

---

## 2. Directory Layout

```
FSD/
├── HTML/          # Page HTML files (one per route)
├── CSS/           # Stylesheets (per-page and shared)
├── JS/            # JavaScript (per-page and shared)
├── IMG/           # Images (e.g. template previews)
└── templates/     # Resume templates (each: template.html + style.css)
```

---

## 3. HTML (`FSD/HTML/`)

Pages served by `Controller/page_controller.py` from `HTML_DIR`:

| File | Route / purpose |
|------|------------------|
| landing page.html | `/` – Landing page |
| loginPage.html | `/login`, `/loginPage.html` |
| signUp.html | Sign-up page |
| login-success.html | `/login-success` – Post-login redirect |
| dashboard.html | `/dashboard` |
| contact.html | `/contact` |
| settings.html | `/settings` |
| documents.html | `/documents` – User’s documents list |
| terms.html | `/terms` |
| forgot-password.html | `/forgot-password` |
| choose-template.html | Template selection |
| step-1.html | Resume step 1 (e.g. personal) |
| step-2.html | Resume step 2 (e.g. education) |
| step-3.html | Resume step 3 (e.g. experience) |
| step-4.html | Resume step 4 (e.g. skills) |
| build-resume.html | Build / preview resume |
| navbar.html | Shared navbar fragment |
| feedback.html | Feedback form |
| about.html | About page |
| reset-password.html | Password reset (token in URL) |

---

## 4. CSS (`FSD/CSS/`)

Stylesheets aligned with pages and flows:

- **Page-specific:** `loginPage.css`, `signUp.css`, `dashboard.css`, `documents.css`, `contact.css`, `settings.css`, `about.css`, `feedback.css`, `terms.css`, `forgotPassword.css`, `resetPassword.css`, `loginSuccess.css`, `choose-template.css`, `step-1.css` … `step-4.css`, `build-resume.css`, `navbar.css`, `landing page.css`
- Template styles live under `FSD/templates/<template-name>/style.css` (see below).

---

## 5. JS (`FSD/JS/`)

Scripts for pages and resume builder:

| File | Role |
|------|------|
| common.js | Shared utilities / helpers |
| navbar-loader.js | Load or inject navbar (e.g. navbar.html) |
| showPassword.js | Toggle password visibility |
| landing page.js | Landing page behavior |
| dashboard.js | Dashboard logic |
| documents.js | Documents page logic |
| contact.js | Contact form |
| settings.js | Settings page |
| feedback.js | Feedback form |
| choose-template.js | Template selection UI |
| step-1.js … step-4.js | Resume steps 1–4 (form, validation, data) |
| build-resume.js | Build / assemble resume |
| live-preview.js | Live resume preview |
| preview.js | Preview handling |
| templates.js | Template loading / rendering |

---

## 6. IMG (`FSD/IMG/`)

Image assets, including template preview thumbnails (e.g. `template2.png`, `template4.png`, `template6.png`, `template8.png`).

---

## 7. Resume Templates (`FSD/templates/`)

Each resume template is in its own folder with:

- **template.html** – Resume markup/structure
- **style.css** – Template-specific styles

Template folder names (as used in the project):

| Template folder | Description (by name) |
|-----------------|------------------------|
| template-academic-yellow | Academic yellow theme |
| template-blue-corporate | Blue corporate |
| template-Bold-red-Accent | Bold red accent |
| template-box-shadow | Box shadow style |
| template-card-based | Card-based layout |
| template-classic-serif | Classic serif |
| template-clean-profile | Clean profile |
| template-dark-elegant | Dark elegant |
| template-fresh-gradient | Fresh gradient |
| template-glassmorphism | Glassmorphism |
| template-infographic | Infographic style |
| template-modern-clean | Modern clean |
| template-soft-green-minimal | Soft green minimal |
| template-split-header-modern | Split header modern |
| template-tech-look | Tech look |
| template-timeline-resume | Timeline resume |
| template-ultra-clean | Ultra clean |
| template-ultra-minimal-black&white | Ultra minimal B&W |

`FSD/JS/templates.js` (and related JS) typically loads or switches between these templates by folder name.

---

## 8. How the backend uses FSD

- **config/app_config.py** – Defines `FSD_DIR`, `HTML_DIR`, `CSS_DIR`, `JS_DIR`, `IMG_DIR` (all under project `FSD/`).
- **app.py** – Creates Flask app with `static_folder=FSD_DIR`, so static URLs resolve under `FSD/`.
- **Controller/page_controller.py** – Serves HTML pages via `send_from_directory(HTML_DIR, "<page>.html")` for each route (e.g. `/`, `/login`, `/dashboard`, `/step-1.html`, etc.).

So FSD is the single source of frontend static content; only **docs/FSD.md** was added—nothing else was changed.
