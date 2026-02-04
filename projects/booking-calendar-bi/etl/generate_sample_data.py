"""
Generate sample CSV data that mimics VBA-exported booking calendar data.

In production, these CSVs come from your VBA script extracting from the
company's booking system. This script generates realistic sample data
so the pipeline can be demonstrated end-to-end.

The VBA export splits data into multiple CSVs due to Excel row limits.
This script replicates that pattern:
  - bookings_2020.csv, bookings_2021.csv, ... bookings_2025.csv
  - clients.csv
  - services.csv
"""

import csv
import random
import os
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "sample"

# --- Reference data ---

CLIENT_TYPES = ["Corporate", "Individual", "Agency"]
REGIONS = ["Europe", "North America", "Asia-Pacific", "Middle East", "Oceania"]

CLIENTS = [
    {"id": 1, "name": "Sakura Travel Group", "type": "Agency", "region": "Asia-Pacific", "country": "Japan"},
    {"id": 2, "name": "Alpine Adventures GmbH", "type": "Agency", "region": "Europe", "country": "Germany"},
    {"id": 3, "name": "Pacific Coast Tours", "type": "Agency", "region": "North America", "country": "USA"},
    {"id": 4, "name": "Voyages Lumiere", "type": "Agency", "region": "Europe", "country": "France"},
    {"id": 5, "name": "Gulf Luxury Travel", "type": "Corporate", "region": "Middle East", "country": "UAE"},
    {"id": 6, "name": "Southern Cross Holidays", "type": "Agency", "region": "Oceania", "country": "Australia"},
    {"id": 7, "name": "Beijing Star International", "type": "Agency", "region": "Asia-Pacific", "country": "China"},
    {"id": 8, "name": "Nordic Explorers AB", "type": "Agency", "region": "Europe", "country": "Sweden"},
    {"id": 9, "name": "Maple Leaf Journeys", "type": "Agency", "region": "North America", "country": "Canada"},
    {"id": 10, "name": "Seoul Wanderers Co.", "type": "Agency", "region": "Asia-Pacific", "country": "South Korea"},
    {"id": 11, "name": "Roma Viaggi SRL", "type": "Agency", "region": "Europe", "country": "Italy"},
    {"id": 12, "name": "Kiwi Adventures Ltd", "type": "Agency", "region": "Oceania", "country": "New Zealand"},
    {"id": 13, "name": "Direct Client - Walk-in", "type": "Individual", "region": "Europe", "country": "France"},
    {"id": 14, "name": "Direct Client - Web", "type": "Individual", "region": "North America", "country": "USA"},
    {"id": 15, "name": "Horizon Corp Events", "type": "Corporate", "region": "Europe", "country": "UK"},
    {"id": 16, "name": "Mumbai Getaways Pvt", "type": "Agency", "region": "Asia-Pacific", "country": "India"},
    {"id": 17, "name": "Andalucia Sun Tours", "type": "Agency", "region": "Europe", "country": "Spain"},
    {"id": 18, "name": "Thai Smile Holidays", "type": "Agency", "region": "Asia-Pacific", "country": "Thailand"},
    {"id": 19, "name": "Amazon Corp Travel", "type": "Corporate", "region": "North America", "country": "USA"},
    {"id": 20, "name": "Swiss Premium Tours", "type": "Agency", "region": "Europe", "country": "Switzerland"},
]

SERVICES = [
    {"id": 1, "name": "City Walking Tour", "category": "Tour", "destination": "Paris"},
    {"id": 2, "name": "Airport Transfer", "category": "Transfer", "destination": "Paris"},
    {"id": 3, "name": "Hotel Le Marais", "category": "Accommodation", "destination": "Paris"},
    {"id": 4, "name": "Seine River Cruise", "category": "Tour", "destination": "Paris"},
    {"id": 5, "name": "Wine Tasting Bordeaux", "category": "Tour", "destination": "Bordeaux"},
    {"id": 6, "name": "Chateau Stay Bordeaux", "category": "Accommodation", "destination": "Bordeaux"},
    {"id": 7, "name": "Nice Coastal Tour", "category": "Tour", "destination": "Nice"},
    {"id": 8, "name": "Hotel Promenade Nice", "category": "Accommodation", "destination": "Nice"},
    {"id": 9, "name": "Lyon Food Tour", "category": "Tour", "destination": "Lyon"},
    {"id": 10, "name": "Mont Blanc Excursion", "category": "Tour", "destination": "Chamonix"},
    {"id": 11, "name": "D-Day Normandy Tour", "category": "Tour", "destination": "Normandy"},
    {"id": 12, "name": "TGV Train Booking", "category": "Transfer", "destination": "Multi-city"},
    {"id": 13, "name": "Private Car Service", "category": "Transfer", "destination": "Multi-city"},
    {"id": 14, "name": "Versailles Day Trip", "category": "Tour", "destination": "Versailles"},
    {"id": 15, "name": "Provence Lavender Tour", "category": "Tour", "destination": "Provence"},
    {"id": 16, "name": "Hotel Vieux Lyon", "category": "Accommodation", "destination": "Lyon"},
    {"id": 17, "name": "Strasbourg Christmas Tour", "category": "Tour", "destination": "Strasbourg"},
    {"id": 18, "name": "Marseille Port Tour", "category": "Tour", "destination": "Marseille"},
    {"id": 19, "name": "Ski Package Alps", "category": "Tour", "destination": "Chamonix"},
    {"id": 20, "name": "Hotel Negresco Nice", "category": "Accommodation", "destination": "Nice"},
]

AGENTS = [
    {"id": 1, "name": "Marie Dubois", "team": "Inbound Europe"},
    {"id": 2, "name": "Pierre Martin", "team": "Inbound Europe"},
    {"id": 3, "name": "Sophie Laurent", "team": "Inbound Asia"},
    {"id": 4, "name": "Jean-Luc Bernard", "team": "Inbound Americas"},
    {"id": 5, "name": "Camille Moreau", "team": "Corporate"},
    {"id": 6, "name": "Nicolas Petit", "team": "Inbound Asia"},
    {"id": 7, "name": "Isabelle Leroy", "team": "Inbound Europe"},
    {"id": 8, "name": "Thomas Roux", "team": "Inbound Americas"},
]

STATUSES = ["Confirmed", "Pending", "Cancelled", "Completed"]


def seasonal_weight(month):
    """Booking volume varies by season - peaks in spring/summer."""
    weights = {
        1: 0.5, 2: 0.6, 3: 0.9, 4: 1.2, 5: 1.3, 6: 1.4,
        7: 1.5, 8: 1.3, 9: 1.1, 10: 0.9, 11: 0.6, 12: 0.7
    }
    return weights[month]


def yearly_growth(year):
    """Simulate business growth with COVID dip."""
    factors = {
        2020: 0.3,   # COVID crash
        2021: 0.5,   # Partial recovery
        2022: 0.8,   # Recovery
        2023: 1.0,   # Back to normal
        2024: 1.15,  # Growth
        2025: 1.25,  # Continued growth
    }
    return factors.get(year, 1.0)


def generate_bookings_for_year(year):
    """Generate booking records for a single year."""
    bookings = []
    booking_id_start = (year - 2020) * 5000 + 1

    base_monthly = 120  # base bookings per month
    booking_id = booking_id_start

    for month in range(1, 13):
        # Skip future months in current year
        if year == 2025 and month > 11:
            continue

        n_bookings = int(base_monthly * seasonal_weight(month) * yearly_growth(year))
        n_bookings += random.randint(-10, 10)  # noise

        days_in_month = 28 if month == 2 else (30 if month in [4, 6, 9, 11] else 31)

        for _ in range(max(1, n_bookings)):
            day = random.randint(1, days_in_month)
            booking_date = datetime(year, month, day)

            # Check-in is 1-90 days after booking
            lead_time = random.randint(1, 90)
            checkin_date = booking_date + timedelta(days=lead_time)

            # Duration 1-7 nights for tours, 1-14 for accommodation
            service = random.choice(SERVICES)
            if service["category"] == "Accommodation":
                nights = random.randint(1, 14)
            elif service["category"] == "Transfer":
                nights = 0
            else:
                nights = random.randint(0, 3)

            checkout_date = checkin_date + timedelta(days=max(1, nights))

            client = random.choice(CLIENTS)
            agent = random.choice(AGENTS)
            pax = random.randint(1, 12)

            # Revenue based on service category
            if service["category"] == "Accommodation":
                base_price = random.uniform(80, 350) * max(1, nights) * pax
            elif service["category"] == "Transfer":
                base_price = random.uniform(30, 150) * pax
            else:
                base_price = random.uniform(50, 200) * pax

            revenue = round(base_price, 2)
            cost = round(revenue * random.uniform(0.55, 0.80), 2)

            # Status distribution
            if checkin_date < datetime.now():
                status = random.choices(
                    ["Completed", "Cancelled"],
                    weights=[0.85, 0.15]
                )[0]
            else:
                status = random.choices(
                    ["Confirmed", "Pending", "Cancelled"],
                    weights=[0.6, 0.25, 0.15]
                )[0]

            bookings.append({
                "booking_id": f"BK-{booking_id:06d}",
                "booking_date": booking_date.strftime("%Y-%m-%d"),
                "checkin_date": checkin_date.strftime("%Y-%m-%d"),
                "checkout_date": checkout_date.strftime("%Y-%m-%d"),
                "client_id": client["id"],
                "client_name": client["name"],
                "service_id": service["id"],
                "service_name": service["name"],
                "service_category": service["category"],
                "destination": service["destination"],
                "agent_id": agent["id"],
                "agent_name": agent["name"],
                "status": status,
                "pax": pax,
                "nights": nights,
                "revenue": revenue,
                "cost": cost,
                "currency": "EUR",
            })
            booking_id += 1

    return bookings


def write_bookings_csv(bookings, year):
    """Write bookings to a CSV file for a single year (mimics VBA split)."""
    filepath = OUTPUT_DIR / f"bookings_{year}.csv"
    fieldnames = [
        "booking_id", "booking_date", "checkin_date", "checkout_date",
        "client_id", "client_name", "service_id", "service_name",
        "service_category", "destination", "agent_id", "agent_name",
        "status", "pax", "nights", "revenue", "cost", "currency"
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bookings)
    print(f"  bookings_{year}.csv: {len(bookings)} rows")


def write_clients_csv():
    filepath = OUTPUT_DIR / "clients.csv"
    fieldnames = ["id", "name", "type", "region", "country"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(CLIENTS)
    print(f"  clients.csv: {len(CLIENTS)} rows")


def write_services_csv():
    filepath = OUTPUT_DIR / "services.csv"
    fieldnames = ["id", "name", "category", "destination"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(SERVICES)
    print(f"  services.csv: {len(SERVICES)} rows")


def write_agents_csv():
    filepath = OUTPUT_DIR / "agents.csv"
    fieldnames = ["id", "name", "team"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(AGENTS)
    print(f"  agents.csv: {len(AGENTS)} rows")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating sample booking calendar data...")
    print("(Mimics VBA export: split by year due to Excel row limits)\n")

    total = 0
    for year in range(2020, 2026):
        bookings = generate_bookings_for_year(year)
        write_bookings_csv(bookings, year)
        total += len(bookings)

    write_clients_csv()
    write_services_csv()
    write_agents_csv()

    print(f"\nTotal booking records: {total}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
