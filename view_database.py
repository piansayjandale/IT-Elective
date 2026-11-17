"""
LedgerCraft PRO - Database Inspector (Pure Python)
Run this script to inspect tables and rows in ledgercraft.db cleanly:
    python view_database.py
    python view_database.py invoices
    python view_database.py users
    python view_database.py bills
"""
import sqlite3
import sys
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ledgercraft.db")

def inspect_table(table_name="invoices", limit=10):
    if not os.path.exists(DB_PATH):
        print(f"[!] Database file '{DB_PATH}' not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get list of all tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [r[0] for r in cur.fetchall() if r[0] != 'sqlite_sequence']

    if table_name not in tables:
        print(f"Unknown table '{table_name}'. Available tables: {', '.join(tables)}")
        return

    cur.execute(f"SELECT * FROM {table_name} LIMIT ?", (limit,))
    rows = cur.fetchall()

    print("=" * 80)
    print(f" TABLE: {table_name} (Showing up to {limit} rows) - Total Available Tables: {tables}")
    print("=" * 80)

    if not rows:
        print(" (No records found in this table)")
        return

    columns = rows[0].keys()
    print("Columns:", " | ".join(columns))
    print("-" * 80)

    for i, row in enumerate(rows, 1):
        print(f"Row #{i}:")
        for col in columns:
            val = row[col]
            if val is not None and str(val).strip():
                print(f"   {col:20}: {val}")
        print("-" * 40)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "invoices"
    inspect_table(target)
