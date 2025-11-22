"""
Test SQL analytical queries and display results.
"""
import sqlite3
from pathlib import Path

def run_query(conn, query_name, query_sql):
    """Run a query and display results."""
    cursor = conn.cursor()
    cursor.execute(query_sql)
    
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    print(f"\n{'='*80}")
    print(f"{query_name}")
    print(f"{'='*80}")
    
    if not results:
        print("No results found.")
        return
    
    # Print header
    print(" | ".join(f"{col:15}" for col in columns))
    print("=" * 80)
    
    # Print rows (limit to 10)
    for row in results[:10]:
        formatted_row = []
        for val in row:
            if isinstance(val, float):
                formatted_row.append(f"{val:15.2f}")
            elif isinstance(val, int):
                formatted_row.append(f"{val:15,}")
            else:
                val_str = str(val) if val is not None else ""
                formatted_row.append(f"{val_str[:15]:15}")
        print(" | ".join(formatted_row))
    
    if len(results) > 10:
        print(f"... ({len(results) - 10} more rows)")

def main():
    """Test key analytical queries."""
    db_path = Path(__file__).parent.parent / "studio_pierrot.db"
    conn = sqlite3.connect(db_path)
    
    try:
        # Q1: Recent vs Classic performance
        run_query(conn, "Q1: Recent vs Classic Performance", """
            SELECT 
                CASE 
                    WHEN CAST(SUBSTR(a.start_date, 1, 4) AS INTEGER) >= 2015 THEN 'Recent (2015+)'
                    ELSE 'Classic (< 2015)'
                END AS era,
                COUNT(DISTINCT a.anime_id) AS num_anime,
                ROUND(AVG(m.score), 2) AS avg_score,
                ROUND(AVG(m.members), 0) AS avg_members,
                ROUND(AVG(CAST(m.dropped AS REAL) / NULLIF(m.members, 0) * 100), 2) AS avg_drop_rate_pct
            FROM dim_anime a
            JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
            WHERE a.start_date IS NOT NULL
            GROUP BY era
            ORDER BY era DESC
        """)
        
        # Q2: Top performers
        run_query(conn, "Q2: Top 5 Anime by Score", """
            SELECT 
                a.title,
                SUBSTR(a.start_date, 1, 4) AS year,
                m.score,
                m.members,
                s.filler_ratio
            FROM dim_anime a
            JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
            LEFT JOIN dim_season s ON a.anime_id = s.anime_id
            ORDER BY m.score DESC
            LIMIT 5
        """)
        
        # Q3: Filler ratio impact
        run_query(conn, "Q3: Filler Ratio Impact on Performance", """
            SELECT 
                CASE 
                    WHEN s.filler_ratio < 0.10 THEN 'Low (<10%)'
                    WHEN s.filler_ratio < 0.25 THEN 'Medium (10-25%)'
                    WHEN s.filler_ratio < 0.40 THEN 'High (25-40%)'
                    ELSE 'Very High (40%+)'
                END AS filler_category,
                COUNT(*) AS num_anime,
                ROUND(AVG(m.score), 2) AS avg_score,
                ROUND(AVG(CAST(m.dropped AS REAL) / NULLIF(m.members, 0) * 100), 2) AS avg_drop_rate_pct
            FROM dim_season s
            JOIN dim_anime a ON s.anime_id = a.anime_id
            JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
            GROUP BY filler_category
        """)
        
        # Q6: ROI Analysis
        run_query(conn, "Q6: Top 5 Anime by ROI", """
            SELECT 
                a.title,
                SUBSTR(a.start_date, 1, 4) AS year,
                f.estimated_revenue - f.production_cost - f.marketing_cost AS profit,
                ROUND((f.estimated_revenue - f.production_cost - f.marketing_cost) / 
                      NULLIF(f.production_cost + f.marketing_cost, 0) * 100, 1) AS roi_pct
            FROM dim_anime a
            JOIN fact_financials f ON a.anime_id = f.anime_id
            ORDER BY profit DESC
            LIMIT 5
        """)
        
        print("\n" + "="*80)
        print("✓ SQL query tests complete!")
        print("="*80)
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
