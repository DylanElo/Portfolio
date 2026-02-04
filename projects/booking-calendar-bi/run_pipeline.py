"""
Pipeline Orchestrator - Runs the full ETL pipeline in sequence.

Usage:
    python run_pipeline.py           # Run full pipeline with sample data
    python run_pipeline.py --real    # Run with real data from data/raw/

Pipeline steps:
    1. Ingest CSVs → SQLite staging tables
    2. Build dimension tables (star schema)
    3. Build fact table with FK lookups
    4. Export JSON for dashboard + CSV for Looker Studio
"""

import subprocess
import sys
import time
from pathlib import Path

ETL_DIR = Path(__file__).parent / "etl"

STEPS = [
    ("01_ingest_csvs.py", "Ingesting CSVs into SQLite"),
    ("10_build_dimensions.py", "Building dimension tables"),
    ("20_build_fact_bookings.py", "Building fact table"),
    ("99_export_for_dashboard.py", "Exporting dashboard data"),
]


def run_step(script, description):
    print(f"\n{'='*50}")
    print(f"  {description}")
    print(f"  Running: {script}")
    print(f"{'='*50}\n")

    result = subprocess.run(
        [sys.executable, str(ETL_DIR / script)],
        capture_output=False,
    )

    if result.returncode != 0:
        print(f"\n  FAILED: {script} (exit code {result.returncode})")
        sys.exit(1)


def main():
    start = time.time()
    use_real = "--real" in sys.argv

    print("\n" + "=" * 50)
    print("  BOOKING CALENDAR BI - ETL PIPELINE")
    print(f"  Data source: {'data/raw/' if use_real else 'data/sample/'}")
    print("=" * 50)

    if use_real:
        # Patch the ingestion script to use raw dir
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "ingest", ETL_DIR / "01_ingest_csvs.py"
        )
        mod = importlib.util.module_from_spec(spec)
        # Will be handled by DATA_SOURCE variable in the script
        print("\n  To use real data, update DATA_SOURCE in 01_ingest_csvs.py to 'raw'")
        print("  Then run: python run_pipeline.py\n")

    for script, desc in STEPS:
        run_step(script, desc)

    elapsed = time.time() - start
    print(f"\n{'='*50}")
    print(f"  Pipeline complete ({elapsed:.1f}s)")
    print(f"{'='*50}")
    print(f"\n  Dashboard: dashboard/index.html")
    print(f"  Looker CSV: data/looker_export/bookings_flat.csv")
    print(f"  Database:   data/bookings.db\n")


if __name__ == "__main__":
    main()
