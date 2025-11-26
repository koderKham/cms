# Safe helper to add missing Case columns to SQLite DB used by the app.
# Run: python add_case_type_columns.py
from app import app, db
from sqlalchemy import text

COLUMNS = {
    # Personal Injury
    "injuries": "TEXT",
    "accident_date": "TEXT",
    "accident_location": "VARCHAR(255)",
    "treating_physicians": "TEXT",
    "medical_record_refs": "TEXT",
    "lost_wages": "VARCHAR(100)",
    "insurance_info": "TEXT",
    "settlement_amount": "VARCHAR(100)",
    # Criminal
    "jurisdiction": "TEXT",
    "defendant": "VARCHAR(200)",
    "co_defendants": "INTEGER",
    "retained_date": "TEXT",
    "charges": "TEXT",
    "arresting_agency": "VARCHAR(200)",
    "case_status": "VARCHAR(100)",
    # Estate / Probate
    "decedent_name": "VARCHAR(200)",
    "date_of_death": "TEXT",
    "will_present": "INTEGER",
    "executor_name": "VARCHAR(200)",
    "beneficiaries": "TEXT",
    "estate_value": "VARCHAR(100)",
    "probate_case_number": "VARCHAR(100)",
    # Other
    "matter_description": "TEXT",
    "opposing_party": "VARCHAR(200)",
    "priority": "VARCHAR(50)",
    "court": "VARCHAR(200)",
}

def table_columns(conn, table_name="case"):
    res = conn.execute(text(f"PRAGMA table_info(\"{table_name}\")")).fetchall()
    return {r[1] for r in res}

if __name__ == "__main__":
    with app.app_context():
        conn = db.session.connection()
        existing = table_columns(conn, "case")
        added = []
        for col, typ in COLUMNS.items():
            if col not in existing:
                try:
                    conn.execute(text(f'ALTER TABLE "case" ADD COLUMN {col} {typ};'))
                    added.append(col)
                except Exception as e:
                    print(f"Failed to add {col}: {e}")
        if added:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
        print("Added columns:", added if added else "none (table already up-to-date)")