# Dylan Elo – Portfolio

Modern portfolio for my work as a **Software Engineer & BI / Data Analyst**.

The repository contains both the source code for this website and a full **end-to-end Business Intelligence case study** built around the anime industry and Studio Pierrot.

---

## 🚀 Tech Stack

- **Frontend**
  - Vite, vanilla JS, modern CSS
  - Chart.js for interactive charts
- **Backend / ETL**
  - Python 3.11
  - Requests + standard library
  - SQLite as lightweight warehouse
- **Business Intelligence**
  - Dimensional model (star schema) with facts & dimensions
  - Automated daily ETL workflow via GitHub Actions
  - Multi-lens dashboards (global fandom, domestic TV, streaming & finance)

---

## 🧩 Repository Structure

```text
.
├─ .github/workflows/        # CI for build + daily ETL
├─ docs/                     # BI documentation (stakeholders, strategy, model spec)
├─ assets/                   # Built dashboard assets (Vite)
├─ src/                      # Portfolio website styles
├─ index.html                # Main portfolio page
├─ project.html              # Projects overview page
└─ projects/
   └─ studio-pierrot-bi/     # Flagship BI case study
```

Key documentation in `docs/`:

* `stakeholder_requirements.md` – who cares about what, and why
* `strategy_document.md` – project goals, success metrics, constraints
* `data_model_spec.md` – star schema, facts & dimensions
* `executive_requirements.md` – C-level dashboard expectations

---

## 🎬 Flagship Project – Studio Pierrot BI

**Path:** `projects/studio-pierrot-bi/`

**Role:** BI Analyst at Studio Pierrot (simulated scenario, Tokyo, Japan)
**Business Question:** how can Studio Pierrot compete with MAPPA / ufotable in the streaming era while leveraging its legacy IP?

    * `README.md` (this folder)
    * `DATA_DICTIONARY.md`
    * `PHASE3B_DASHBOARD_INSIGHTS.md`

### Running the BI project locally

From the repo root:

```bash
cd projects/studio-pierrot-bi

# (Optional) create a virtual env first
# python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows

pip install -r requirements.txt

# 1. Run ETL to build / refresh the SQLite warehouse
python etl/extract_mal.py
python etl/load_warehouse.py

# 2. Export data for the dashboard
python etl/export_to_dashboard.py
```

Then open in your browser:

* `projects/studio-pierrot-bi/dashboard/index.html`

A GitHub Actions workflow (`.github/workflows/daily_etl.yml`) can also run this ETL and commit updated `data/` and `dashboard/data.js` on a schedule.

---

## 🌐 Portfolio Website

The portfolio itself is a small Vite app.

From the repo root:

```bash
npm install
npm run dev
```

Then visit the local URL shown in the terminal (usually `http://localhost:5173`).

Main files:

* `index.html` – landing page (hero, about, projects, resume, contact)
* `src/style.css` – glassmorphism-inspired UI, dark theme
* `project.html` – project listing page that links to Studio Pierrot BI and other work

---

## 🤝 Feedback

If you're a recruiter, hiring manager, or fellow data practitioner and you'd like more detail on:

* the BI modeling decisions,
* how the simulated metrics were calibrated,
* or how this case study could translate to your domain,

feel free to reach out via the **Contact** section on the site or open an issue in this repo.
