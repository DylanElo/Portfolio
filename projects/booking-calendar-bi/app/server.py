"""
Booking Calendar BI - Interactive Dashboard Server

Flask app that serves the interactive dashboard and provides
API endpoints for live SQLite queries. Enables drill-down filtering
by supplier, date, location, service type, and agent.
"""

from flask import Flask, render_template, jsonify, request
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)

DB_PATH = Path(__file__).parent.parent / "data" / "bookings.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---- Pages ----

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/supplier")
def supplier_view():
    return render_template("supplier.html")


# ---- API: Filters (dropdowns) ----

@app.route("/api/filters")
def api_filters():
    """Return all available filter options for dropdowns."""
    conn = get_db()

    suppliers = [r[0] for r in conn.execute(
        "SELECT DISTINCT supplier_name FROM dim_supplier ORDER BY supplier_name"
    ).fetchall()]

    locations = [r[0] for r in conn.execute(
        "SELECT DISTINCT location_name FROM dim_location ORDER BY location_name"
    ).fetchall()]

    regions = [r[0] for r in conn.execute(
        "SELECT DISTINCT region FROM dim_location WHERE region IS NOT NULL ORDER BY region"
    ).fetchall()]

    service_types = [r[0] for r in conn.execute(
        "SELECT DISTINCT service_type FROM dim_service_type ORDER BY service_type"
    ).fetchall()]

    agents = [dict(r) for r in conn.execute("""
        SELECT DISTINCT a.agent_name, a.agent_country
        FROM dim_agent a
        JOIN fact_bookings fb ON a.agent_id = fb.agent_id
        ORDER BY a.agent_name
    """).fetchall()]

    years = [r[0] for r in conn.execute(
        "SELECT DISTINCT year FROM dim_date WHERE year BETWEEN 2015 AND 2027 ORDER BY year"
    ).fetchall()]

    conn.close()
    return jsonify({
        "suppliers": suppliers,
        "locations": locations,
        "regions": regions,
        "service_types": service_types,
        "agents": agents,
        "years": years,
    })


# ---- API: KPIs ----

@app.route("/api/kpis")
def api_kpis():
    """KPIs with optional date range filter."""
    conn = get_db()
    date_from = request.args.get("from", "2015-01-01")
    date_to = request.args.get("to", "2027-12-31")

    row = conn.execute("""
        SELECT
            COUNT(DISTINCT fb.booking_ref) as total_bookings,
            SUM(fb.pax) as total_pax,
            SUM(fb.total_services) as total_services,
            ROUND(AVG(fb.trip_days), 1) as avg_trip_days,
            COUNT(DISTINCT fb.agent_id) as active_agents
        FROM fact_bookings fb
        JOIN dim_date d ON fb.travel_date_id = d.date_id
        WHERE d.date BETWEEN ? AND ?
    """, (date_from, date_to)).fetchone()

    conn.close()
    return jsonify(dict(row))


# ---- API: Supplier Daily View ----

@app.route("/api/supplier/daily")
def api_supplier_daily():
    """
    Daily service count for a specific supplier.
    This is the key drill-down: for a hotel, see how many rooms/services
    are booked per day.

    Params:
      - supplier: supplier name (required)
      - from: start date (YYYY-MM-DD)
      - to: end date (YYYY-MM-DD)
      - service_type: filter by service type (optional)
    """
    conn = get_db()
    supplier = request.args.get("supplier")
    date_from = request.args.get("from", "2024-01-01")
    date_to = request.args.get("to", "2025-12-31")
    service_type = request.args.get("service_type")

    if not supplier:
        return jsonify({"error": "supplier parameter required"}), 400

    query = """
        SELECT
            d.date,
            d.day_name,
            d.is_weekend,
            COUNT(*) as service_count,
            SUM(fs.pax) as total_pax,
            COUNT(DISTINCT fs.booking_ref) as unique_bookings,
            GROUP_CONCAT(DISTINCT st.service_type) as service_types
        FROM fact_services fs
        JOIN dim_date d ON fs.service_date_id = d.date_id
        JOIN dim_supplier s ON fs.supplier_id = s.supplier_id
        JOIN dim_service_type st ON fs.service_type_id = st.service_type_id
        WHERE s.supplier_name = ?
          AND d.date BETWEEN ? AND ?
    """
    params = [supplier, date_from, date_to]

    if service_type:
        query += " AND st.service_type = ?"
        params.append(service_type)

    query += " GROUP BY d.date ORDER BY d.date"

    rows = [dict(r) for r in conn.execute(query, params).fetchall()]
    conn.close()
    return jsonify(rows)


# ---- API: Supplier Summary ----

@app.route("/api/supplier/summary")
def api_supplier_summary():
    """Monthly summary for a supplier."""
    conn = get_db()
    supplier = request.args.get("supplier")
    date_from = request.args.get("from", "2020-01-01")
    date_to = request.args.get("to", "2027-12-31")

    if not supplier:
        return jsonify({"error": "supplier parameter required"}), 400

    rows = [dict(r) for r in conn.execute("""
        SELECT
            m.year, m.month, m.month_name,
            COUNT(*) as service_count,
            SUM(fs.pax) as total_pax,
            COUNT(DISTINCT fs.booking_ref) as unique_bookings
        FROM fact_services fs
        JOIN dim_date d ON fs.service_date_id = d.date_id
        JOIN dim_month m ON CAST(substr(d.date, 1, 4) || substr(d.date, 6, 2) AS INTEGER) = m.month_id
        JOIN dim_supplier s ON fs.supplier_id = s.supplier_id
        WHERE s.supplier_name = ?
          AND d.date BETWEEN ? AND ?
        GROUP BY m.year, m.month
        ORDER BY m.year, m.month
    """, (supplier, date_from, date_to)).fetchall()]

    conn.close()
    return jsonify(rows)


# ---- API: Monthly Trend (filterable) ----

@app.route("/api/monthly")
def api_monthly():
    """Monthly booking trend with optional filters."""
    conn = get_db()
    date_from = request.args.get("from", "2015-01-01")
    date_to = request.args.get("to", "2027-12-31")
    agent_country = request.args.get("country")
    region = request.args.get("region")

    query = """
        SELECT
            m.year, m.month, m.month_name,
            COUNT(DISTINCT fb.booking_ref) as total_bookings,
            SUM(fb.pax) as total_pax
        FROM fact_bookings fb
        JOIN dim_month m ON fb.month_id = m.month_id
        JOIN dim_date d ON fb.travel_date_id = d.date_id
        JOIN dim_agent a ON fb.agent_id = a.agent_id
    """
    conditions = ["d.date BETWEEN ? AND ?"]
    params = [date_from, date_to]

    if agent_country:
        conditions.append("a.agent_country = ?")
        params.append(agent_country)

    query += " WHERE " + " AND ".join(conditions)
    query += " GROUP BY m.year, m.month ORDER BY m.year, m.month"

    rows = [dict(r) for r in conn.execute(query, params).fetchall()]
    conn.close()
    return jsonify(rows)


# ---- API: Location Daily ----

@app.route("/api/location/daily")
def api_location_daily():
    """Daily services by location (for capacity planning)."""
    conn = get_db()
    location = request.args.get("location")
    date_from = request.args.get("from", "2024-01-01")
    date_to = request.args.get("to", "2025-12-31")

    if not location:
        return jsonify({"error": "location parameter required"}), 400

    rows = [dict(r) for r in conn.execute("""
        SELECT
            d.date,
            d.day_name,
            st.service_type,
            COUNT(*) as service_count,
            SUM(fs.pax) as total_pax,
            COUNT(DISTINCT fs.booking_ref) as unique_bookings
        FROM fact_services fs
        JOIN dim_date d ON fs.service_date_id = d.date_id
        JOIN dim_location l ON fs.location_id = l.location_id
        JOIN dim_service_type st ON fs.service_type_id = st.service_type_id
        WHERE l.location_name = ?
          AND d.date BETWEEN ? AND ?
        GROUP BY d.date, st.service_type
        ORDER BY d.date, st.service_type
    """, (location, date_from, date_to)).fetchall()]

    conn.close()
    return jsonify(rows)


# ---- API: Top suppliers for a date range ----

@app.route("/api/top-suppliers")
def api_top_suppliers():
    conn = get_db()
    date_from = request.args.get("from", "2024-01-01")
    date_to = request.args.get("to", "2025-12-31")
    service_type = request.args.get("service_type")
    limit = request.args.get("limit", 20, type=int)

    query = """
        SELECT
            s.supplier_name,
            COUNT(*) as service_count,
            SUM(fs.pax) as total_pax,
            COUNT(DISTINCT fs.booking_ref) as unique_bookings
        FROM fact_services fs
        JOIN dim_date d ON fs.service_date_id = d.date_id
        JOIN dim_supplier s ON fs.supplier_id = s.supplier_id
        JOIN dim_service_type st ON fs.service_type_id = st.service_type_id
        WHERE d.date BETWEEN ? AND ?
    """
    params = [date_from, date_to]

    if service_type:
        query += " AND st.service_type = ?"
        params.append(service_type)

    query += " GROUP BY s.supplier_id ORDER BY service_count DESC LIMIT ?"
    params.append(limit)

    rows = [dict(r) for r in conn.execute(query, params).fetchall()]
    conn.close()
    return jsonify(rows)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
