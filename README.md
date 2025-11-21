# Studio Pierrot Turnaround Strategy: BI Capstone

A strategic Business Intelligence project designed to "save" Studio Pierrot by analyzing the performance of 10 iconic anime franchises. This project demonstrates a full-stack data engineering and analytics workflow, culminating in an interactive "XXL" executive dashboard.

**[🔴 Live Dashboard Demo](https://dylanelo.github.io/Portfolio/project_studio_pierrot.html)**

## 🎯 Project Objective: The "Savior" Persona

**Scenario:** Studio Pierrot (Naruto, Bleach, Tokyo Ghoul) is facing declining ROI on recent productions. As a new Data Analyst, your mission is to identify the root causes and propose a data-driven turnaround strategy.

**Key Questions Answered:**
1.  **The Filler Trap:** Does "padding" episodes (filler) significantly hurt profitability?
2.  **Quality vs. Quantity:** How does animation budget correlate with global streaming revenue?
3.  **Global Shift:** What is the revenue split between domestic broadcast and international streaming?

## 📊 Architecture & Tech Stack

This project is built from scratch without relying on pre-made BI tools like Tableau, demonstrating full-stack capability.

```mermaid
graph LR
    A[Raw Data (Jikan API)] --> B[Python ETL]
    B --> C[SQLite Data Warehouse]
    C --> D[JSON Data Export]
    D --> E[Interactive Web Dashboard]
```

*   **ETL Pipeline:** Python (`pandas`, `requests`) to extract data and generate realistic business metrics (150k+ rows).
*   **Data Warehouse:** SQLite with a **Star Schema** design (`dim_anime`, `dim_date`, `fact_daily_performance`).
*   **Frontend:** Vanilla HTML5, **Tailwind CSS** for styling, and **Chart.js** for visualizations.
*   **Deployment:** GitHub Pages.

## 🚀 Key Features

### 1. "XXL" Executive Dashboard
A high-density, interactive command center for studio executives.
*   **Global KPI Cards:** Real-time tracking of Revenue, Views, Watch Time, and Sentiment.
*   **Interactive Filters:** Filter all charts by Date Range (2023/2024), Specific Anime, and Platform.
*   **Advanced Visualizations:**
    *   **ROI vs. Filler % (Scatter Plot):** Visual proof that high filler correlates with low ROI.
    *   **Revenue Trend (Multi-Axis):** Correlating daily views with revenue spikes.
    *   **Platform Split:** Breakdown of revenue by Netflix, Crunchyroll, Hulu, etc.

### 2. Strategic Insights
*   **Actionable Recommendations:** Specific business moves based on data (e.g., "Cap filler at 10%").
*   **Persona-Driven Narrative:** The entire project is framed as a strategic proposal to studio leadership.

## 🗄️ Data Model (Star Schema)

The data warehouse is designed for performance and analytical flexibility.

*   **`dim_anime`**: Metadata for 10 iconic franchises (Naruto, Bleach, Tokyo Ghoul, etc.).
*   **`dim_platform`**: Streaming platforms (Crunchyroll, Netflix, etc.).
*   **`dim_date`**: Date dimension for time-series analysis.
*   **`fact_daily_performance`**: Granular daily metrics (views, revenue, sentiment) for 2 years.

## 📚 Strategic Documents

This project includes comprehensive business documentation demonstrating the full BI workflow:

- **[Executive Requirements](docs/executive_requirements.md)**: High-level business objectives and success metrics defined by studio leadership.
- **[Stakeholder Requirements](docs/stakeholder_requirements.md)**: Detailed analytical needs from Production, Marketing, and Finance teams.
- **[Strategy Document](docs/strategy_document.md)**: Technical implementation roadmap and BI approach.

These documents showcase the **requirements gathering** and **stakeholder alignment** process that precedes any data project.

## 🛠️ Setup & Usage

### Local Development
1.  Clone the repository.
2.  Run the dashboard locally:
    ```bash
    npx serve .
    ```
3.  Open `http://localhost:3000/dashboard/index.html`.

### ETL Pipeline (Optional)
To regenerate the data:
1.  Navigate to the `etl` directory.
2.  Run the generation script:
    ```bash
    python generate_data_v2.py
    ```
3.  Export the dashboard data:
    ```bash
    python export_dashboard_data.py
    ```

## 📄 License

This is a portfolio project created by Dylan Elo.
