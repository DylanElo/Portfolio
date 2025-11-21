"""
Export data from the warehouse to JSON for the web dashboard.
Creates dashboard/data.json with all necessary metrics.
"""
import sqlite3
import json
from pathlib import Path

def export_dashboard_data():
    """Query warehouse and export to JSON."""
    db_path = Path(__file__).parent.parent / "studio_pierrot.db"
    output_path = Path(__file__).parent.parent / "dashboard" / "data.json"
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # 1. Main Anime Dataset
        cursor.execute("""
            SELECT 
                a.title,
                a.studio,
                a.start_date,
                m.score,
                m.members,
                m.popularity,
                s.filler_ratio,
                s.production_stability,
                f.estimated_revenue,
                f.production_cost,
                f.marketing_cost,
                (f.estimated_revenue - f.production_cost - f.marketing_cost) as profit,
                CAST(m.dropped AS REAL) / NULLIF(m.members, 0) * 100 as drop_rate
            FROM dim_anime a
            JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
            LEFT JOIN dim_season s ON a.anime_id = s.anime_id
            LEFT JOIN fact_financials f ON a.anime_id = f.anime_id
            ORDER BY m.score DESC
        """)
        anime_list = [dict(row) for row in cursor.fetchall()]
        
        # 2. Aggregates by Studio
        cursor.execute("""
            SELECT 
                a.studio,
                COUNT(*) as count,
                AVG(m.score) as avg_score,
                AVG(m.members) as avg_members,
                AVG(s.filler_ratio) as avg_filler
            FROM dim_anime a
            JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
            LEFT JOIN dim_season s ON a.anime_id = s.anime_id
            GROUP BY a.studio
            HAVING count >= 1
        """)
        studio_stats = [dict(row) for row in cursor.fetchall()]
        
        # 3. Filler Impact
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN s.filler_ratio < 0.10 THEN 'Low (<10%)'
                    WHEN s.filler_ratio < 0.25 THEN 'Medium (10-25%)'
                    WHEN s.filler_ratio < 0.40 THEN 'High (25-40%)'
                    ELSE 'Very High (40%+)'
                END AS category,
                AVG(m.score) as avg_score,
                AVG(CAST(m.dropped AS REAL) / NULLIF(m.members, 0) * 100) as avg_drop_rate
            FROM dim_season s
            JOIN fact_anime_metrics m ON s.anime_id = m.anime_id
            GROUP BY category
        """)
        filler_stats = [dict(row) for row in cursor.fetchall()]
        
        data = {
            "anime": anime_list,
            "studios": studio_stats,
            "filler_analysis": filler_stats
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"✓ Exported dashboard data to {output_path}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    export_dashboard_data()
