# Business Intelligence Projects – Documentation Hub

Welcome to Dylan Elo's BI portfolio documentation. This directory serves as the central hub for strategic and technical documentation across multiple BI case studies.

---

## 📊 Featured BI Projects

### 1. Studio Pierrot Anime Analytics
**Path:** [../projects/studio-pierrot-bi/](../projects/studio-pierrot-bi/)

**Strategic Question:** Why are Studio Pierrot's flagship IPs struggling to capture the same global momentum as newer titles like Jujutsu Kaisen—and what should they do about it?

**Capabilities:**
- Multi-lens BI dashboard (Global Fandom, Revenue Timeline, Streaming, Domestic, Production)
- Star schema data warehouse with SQLite
- Python ETL pipeline (Jikan API → Transform → Load)
- Tableau export package with 4 CSV files
- Strategic documentation (executive requirements, stakeholder specs, strategy doc)

**Key Insights:**
- Production Model Impact: Seasonal (<10% filler) = 8.7 avg score vs Continuous (42% filler) = 6.1
- Revenue Momentum: Legacy IP declining (-19% for Naruto) while competitor hits surge (+140% for JJK)
- Streaming Gap: JJK 71.2x demand vs Pierrot portfolio 2-12x
- Revival Success: Bleach TYBW proves Pierrot CAN compete with 8.99 score

**Live Dashboard:** [View on GitHub Pages](https://dylanelo.github.io/Portfolio/projects/studio-pierrot-bi/dashboard/index.html)

**Documentation:**
- [Executive Requirements](../projects/studio-pierrot-bi/docs/executive_requirements.md) – C-level dashboard expectations
- [Stakeholder Requirements](../projects/studio-pierrot-bi/docs/stakeholder_requirements.md) – Cross-functional team needs
- [Strategy Document](../projects/studio-pierrot-bi/docs/strategy_document.md) – Project goals, success metrics
- [Data Model Specification](../projects/studio-pierrot-bi/docs/data_model_spec.md) – Star schema design

---

### 2. Japan Inbound Travel Intelligence Hub
**Path:** [../projects/inbound-japan-bi/](../projects/inbound-japan-bi/)

**Business Context:** DMC (Destination Management Company) BI platform for forecasting inbound travel demand to Japan across multiple data lenses.

**Capabilities:**
- Multi-source ETL pipeline (JNTO arrivals, Frankfurter FX, weather, flight data)
- Dimensional warehouse with star schema
- Real-time dashboard with demand forecasting
- Seasonal risk analysis (typhoons, heatwaves)
- Airport capacity vs demand tracking

**Data Sources:**
- **Real:** JNTO monthly arrivals (2019-2024), Frankfurter FX rates
- **Mock (realistic):** Weather patterns, daily flight volumes

**Live Dashboard:** [View on GitHub Pages](https://dylanelo.github.io/Portfolio/projects/inbound-japan-bi/dashboard/index.html)

**Documentation:**
- [Strategy Document](../projects/inbound-japan-bi/docs/strategy_document.md) – Project vision and approach
- [Stakeholder Requirements](../projects/inbound-japan-bi/docs/stakeholder_requirements.md) – Cross-functional needs
- [Technical Specification](../projects/inbound-japan-bi/docs/technical_spec.md) – Architecture and implementation
- [Phase Walkthroughs](../projects/inbound-japan-bi/docs/) – Phased implementation guides (Phase 1-5)

---

## 🎯 BI Methodology Demonstrated

These projects showcase a complete Business Intelligence workflow aligned with Google BI Professional Certificate best practices:

```
Requirements Gathering
        ↓
Strategy & Planning
        ↓
Data Modeling (Star Schema)
        ↓
ETL Pipeline Development
        ↓
Dashboard Development
        ↓
Stakeholder Delivery
```

Each project includes:
- ✅ **Executive Requirements** – Business goals and success metrics
- ✅ **Stakeholder Requirements** – Departmental analytical needs
- ✅ **Strategy Document** – Technical approach and roadmap
- ✅ **Data Model Specifications** – Dimensional design (facts & dimensions)
- ✅ **ETL Pipeline** – Automated data extraction, transformation, loading
- ✅ **Interactive Dashboards** – Multi-lens analytical views
- ✅ **Documentation** – Data dictionaries, technical specs, walkthroughs

---

## 💡 Why This Documentation Matters

In real-world BI projects, **requirements gathering and strategic planning** are often the most critical phases. This documentation demonstrates:

- **Stakeholder Alignment:** Ensuring all parties agree on objectives before development
- **Scope Definition:** Clear boundaries prevent scope creep
- **Success Metrics:** Measurable criteria for project success
- **Business Context:** Connecting technical work to business value
- **Technical Rigor:** Dimensional modeling, ETL design, data quality standards

---

## 🔗 Related Links

- **Main Portfolio:** [../index.html](../index.html)
- **Portfolio README:** [../README.md](../README.md)
- **Project Overview Page:** [../project.html](../project.html)

---

*These BI case studies are part of Dylan Elo's professional portfolio, demonstrating end-to-end Business Intelligence capabilities from requirements to delivery.*
