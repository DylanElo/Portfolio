# Portfolio Project Audit Report

**Date:** 2026-02-06
**Scope:** Full-stack audit of Dylan Elo's Portfolio project
**Areas:** Security, Accessibility, Performance, Code Quality, CI/CD, Data Engineering

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Critical Issues](#critical-issues)
3. [Security Audit](#security-audit)
4. [Accessibility Audit](#accessibility-audit)
5. [Performance Audit](#performance-audit)
6. [Code Quality Audit](#code-quality-audit)
7. [Build & CI/CD Audit](#build--cicd-audit)
8. [Python ETL Audit](#python-etl-audit)
9. [Summary & Prioritized Recommendations](#summary--prioritized-recommendations)

---

## Project Overview

| Attribute | Detail |
|-----------|--------|
| Stack | Vite 7.2.4 + Vanilla JS + Chart.js + Python ETL + SQLite |
| Pages | `index.html` (landing), `project.html` (case study) |
| Dashboards | Studio Pierrot BI, Inbound Japan BI |
| Deployment | GitHub Pages + Railway.app |
| CI/CD | GitHub Actions (deploy + daily ETL) |

---

## Critical Issues

These require immediate attention:

### 1. SQL Injection Vulnerabilities (ETL)

- **`projects/studio-pierrot-bi/etl/load.py:35`** - `cursor.execute(f"DELETE FROM {table}")` uses f-string interpolation for table names
- **`projects/studio-pierrot-bi/etl/load_warehouse.py:35`** - Same pattern
- **`projects/studio-pierrot-bi/etl/verify_db.py:23`** - `cursor.execute(f"PRAGMA table_info({table_name});")`

**Fix:** Whitelist table names with a constant set, validate before use.

### 2. Path Disclosure in Production Code

- **`projects/studio-pierrot-bi/dashboard/data.js:1-2`** - Auto-generated comment exposes full Windows file path: `C:\Users\dylan\OneDrive\Documents\Portfolio\...`

**Fix:** Strip source path comments from exported data files.

### 3. CDN Resources Without Subresource Integrity

- **`projects/studio-pierrot-bi/dashboard/index.html:8-10`** - Tailwind, Chart.js, and Google Fonts loaded without `integrity` attributes
- **`projects/inbound-japan-bi/dashboard/index.html:9`** - Chart.js loaded without `integrity`

**Fix:** Add SRI hashes to all `<script>` and `<link>` tags from CDNs.

### 4. Widespread Resource Leaks (Python ETL)

12+ database connections and 10+ file handles opened without context managers across both ETL pipelines. On exception, these resources are never closed.

**Fix:** Use `with sqlite3.connect(path) as conn:` and `with open(path) as f:` everywhere.

---

## Security Audit

### HTML / Frontend

| Issue | Location | Severity |
|-------|----------|----------|
| innerHTML with dynamic data (potential XSS) | `studio-pierrot-bi/dashboard/dashboard.js:31,230,711` | Medium |
| No Content Security Policy | Both dashboard `index.html` files | Medium |
| CDN scripts without SRI | Both dashboard `index.html` files | Medium |
| Inline `onclick` handlers | `studio-pierrot-bi/dashboard/index.html:89-98` | Low |
| `console.log` in production | `studio-pierrot-bi/dashboard/dashboard.js:10,14,22,734` | Low |
| External link missing `rel="noopener"` | `project.html:140` - GitHub link has it, but verify all | Low |

### Python ETL

| Issue | Location | Severity |
|-------|----------|----------|
| SQL injection via f-strings | `load.py:35`, `load_warehouse.py:35`, `verify_db.py:23` | Critical |
| No timeout on `requests.get()` | `extract_mal.py:78`, `generate_expanded_dataset.py:39`, `02_fetch_fx_rates.py:39` | High |
| No API retry logic | All 4 scripts that make HTTP requests | High |
| Broad `except Exception` | `extract_mal.py:86`, `generate_expanded_dataset.py:63` | Medium |

### Positive Findings

- No hardcoded API keys or secrets found
- `.gitignore` correctly excludes `.db` files and `__pycache__`
- External links use `target="_blank" rel="noopener"` in most places
- No unsafe deserialization patterns

---

## Accessibility Audit

### Critical

| Issue | Location |
|-------|----------|
| Canvas charts have no `aria-label` or fallback text | Both dashboards: all `<canvas>` elements (14+ total) |
| Emoji icons used without `aria-hidden="true"` or text alternatives | Both dashboard `index.html` files |
| Tab navigation missing ARIA roles (`role="tablist"`, `role="tab"`, `aria-selected`) | `studio-pierrot-bi/dashboard/index.html:88-99` |

### High

| Issue | Location |
|-------|----------|
| Dynamic content updates not announced via `aria-live` | Both dashboards: KPI values, tab switches |
| Loading states (`"Loading..."`) not in `aria-live` region | `inbound-japan-bi/dashboard/index.html:27,31,35` |

### Medium

| Issue | Location |
|-------|----------|
| No skip-to-content link | `index.html`, `project.html` |
| `<div class="section-header">About</div>` used instead of proper heading hierarchy | `index.html:72` |
| No `<meta name="description">` for SEO and screen readers | Both main HTML pages |
| No `lang` attribute issues (correctly set to `en`) | N/A - this is correct |

---

## Performance Audit

### Build & Assets

| Issue | Impact | Location |
|-------|--------|----------|
| `style.css` loaded with cache-buster `?v=4` but no content hash | Manual cache management; could serve stale CSS | `index.html:8` |
| Google Fonts loaded render-blocking from external CDN | Blocks first paint | `style.css:1` |
| Tailwind loaded from CDN (play CDN, not production build) | ~300KB+ unoptimized CSS for development use only | `studio-pierrot-bi/dashboard/index.html:8` |
| All dashboard data modules imported eagerly | Delays time-to-interactive | `studio-pierrot-bi/dashboard/dashboard.js:3-8` |

### Runtime

| Issue | Impact | Location |
|-------|--------|----------|
| Data arrays re-sorted on every tab switch | Wasted CPU cycles | `studio-pierrot-bi/dashboard/dashboard.js:133,179,227,650` |
| Color arrays duplicated across functions | Minor memory waste; maintenance burden | `inbound-japan-bi/dashboard/app.js:129,297` |
| No chart instance cleanup before re-creation | Memory leak if tabs switched repeatedly | Both dashboards |

---

## Code Quality Audit

### HTML

| Issue | Location |
|-------|----------|
| Unclosed `<div>` tag (missing closing for container div) | `project.html:75` - `</section>` before closing the container `<div>` from line 32 |
| Excessive inline `style` attributes (20+ instances) | `project.html` throughout, `index.html:82,117,138,157,162,202,207,236` |
| Footer copyright year inconsistency: 2025 vs 2024 | `index.html:252` says 2025, `project.html:253` says 2024 |
| No favicon defined | Both HTML pages |
| `window.pageYOffset` is deprecated | `src/main.js:69` - use `window.scrollY` instead |

### JavaScript

| Issue | Location |
|-------|----------|
| `console.log` statements in production | `studio-pierrot-bi/dashboard/dashboard.js:10,14,22,734` |
| Duplicate `switchTab` function definition | `studio-pierrot-bi/dashboard/index.html` (inline) AND `dashboard.js:74` |
| Magic numbers without named constants | `dashboard.js:133,160,184,210` (`.slice(0, 10)`, score ranges) |
| Hardcoded chart data instead of data-driven labels | `dashboard.js:387-433` |
| No null checks on DOM queries in multiple render functions | `inbound-japan-bi/dashboard/app.js:49,81,107,164,225` |
| Global namespace pollution via `window.switchTab` | `studio-pierrot-bi/dashboard/dashboard.js:74` |

### CSS

| Issue | Location |
|-------|----------|
| Light theme toggle defined in CSS but no JS implements the toggle | `style.css:24-40` - `.light-theme` rules exist, no toggle mechanism |
| Duplicate layout definitions: `.nav` and `.nav-container` do the same thing | `style.css:126-131` vs `style.css:534-541` |
| Hardcoded `rgba(15, 23, 42, 0.95)` instead of using CSS variable | `style.css:501` |

### Python ETL

| Issue | Location |
|-------|----------|
| `print()` used everywhere instead of `logging` module | All 23 Python files |
| Missing docstrings and type hints | Most functions across all ETL scripts |
| Dead / duplicate anime IDs in target list | `extract_mal.py:13-72` - includes non-Pierrot anime, has duplicates |
| `os.remove()` without existence check | `generate_data_v2.py:15` |
| Unused dependencies in `requirements.txt` | `inbound-japan-bi/requirements.txt` lists `openpyxl`, `matplotlib`, `seaborn` - unused in ETL |
| Missing dependency: pandas used but not in requirements | `studio-pierrot-bi/requirements.txt` - only lists `requests` |
| Typo in output | `04_fetch_opensky_flights.py:25` - `"Gener ating"` |

---

## Build & CI/CD Audit

### `package.json`

| Issue | Detail |
|-------|--------|
| Build script uses `cp -r` (Unix-only) | `npm run build` will fail on Windows without WSL |
| `serve` is a runtime dependency but only used for production serving | Could be `devDependencies` or use Vite preview |

### `vite.config.js`

| Issue | Detail |
|-------|--------|
| `__dirname` used in ES module context | Works with Vite but is not standard ESM; consider `import.meta.dirname` (Node 21+) |
| Dashboard directories not included in Vite build | Copied manually via `cp -r` in build script; fragile |

### `deploy.yml` (GitHub Pages)

| Issue | Detail |
|-------|--------|
| Only copies Studio Pierrot dashboard, not Inbound Japan | Line 39-40: `cp -r projects/studio-pierrot-bi/dashboard/*` but missing `inbound-japan-bi` |
| Uses `actions/checkout@v4` | Good - pinned to major version |
| No caching of `node_modules` | Slower builds; add `cache: 'npm'` to setup-node |

### `daily_etl.yml`

| Issue | Detail |
|-------|--------|
| Uses older action versions (`actions/checkout@v3`, `setup-python@v4`) | `checkout@v3` should be updated to `v4` for consistency |
| `git config --global` sets name/email globally | Should use local config for the repository |
| No error handling if ETL scripts fail partway | Pipeline continues even if `extract_mal.py` fails |
| Commits directly to `main` | No PR review; could introduce broken data |
| Only runs Studio Pierrot ETL, not Inbound Japan | Inbound Japan data never refreshes automatically |

### `railway.json`

- Configuration looks correct
- Uses NIXPACKS builder (appropriate for Node.js)
- Health check and restart policy properly configured

---

## Summary & Prioritized Recommendations

### Severity Counts

| Severity | Count |
|----------|-------|
| Critical | 4 (SQL injection, resource leaks, SRI missing, path disclosure) |
| High | 10 (accessibility gaps, missing error handling, no API retry/timeout) |
| Medium | 14 (performance, code quality, CI/CD gaps) |
| Low | 8 (style, minor inconsistencies) |

### Phase 1: Critical Fixes

1. **Fix SQL injection** - Whitelist table names in `load.py` and `load_warehouse.py`
2. **Add SRI hashes** to CDN `<script>` and `<link>` tags in both dashboards
3. **Remove path disclosure** from `data.js` auto-generated comments
4. **Use context managers** for all DB connections and file operations in Python ETL
5. **Add `requests.get()` timeouts** (e.g., `timeout=10`) to all HTTP calls

### Phase 2: High-Priority Fixes

6. **Add `aria-label`** to all `<canvas>` chart elements
7. **Add proper ARIA roles** to tab navigation (tablist/tab/tabpanel)
8. **Remove `console.log`** statements from production dashboard code
9. **Add `<meta name="description">`** to both main HTML pages
10. **Fix deploy.yml** to also copy the Inbound Japan dashboard
11. **Add retry logic** with exponential backoff to API-calling ETL scripts
12. **Fix footer year inconsistency** (2024 vs 2025)
13. **Fix unclosed `<div>`** in `project.html:75`

### Phase 3: Quality Improvements

14. Replace Tailwind play CDN with production build or remove
15. Add `node_modules` caching to deploy workflow
16. Update `daily_etl.yml` to use `actions/checkout@v4`
17. Add ETL error handling (fail pipeline if extract fails)
18. Fix `requirements.txt` mismatches in both projects
19. Replace `print()` with `logging` in Python scripts
20. Clean up dead code / duplicate anime IDs in `extract_mal.py`
21. Implement light/dark theme toggle in JS (CSS rules exist but aren't wired up)
22. Replace deprecated `window.pageYOffset` with `window.scrollY`

---

*Generated by automated project audit*
