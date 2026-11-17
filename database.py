"""
LedgerCraft PRO - Financial OS Database & Business Logic
"""
import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ledgercraft.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Invoices table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT UNIQUE NOT NULL,
        client_name TEXT NOT NULL,
        client_email TEXT,
        issue_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        is_overdue BOOLEAN DEFAULT 0,
        subtotal REAL NOT NULL,
        tax REAL DEFAULT 0,
        total_amount REAL NOT NULL,
        paid_amount REAL DEFAULT 0,
        balance_due REAL NOT NULL,
        status TEXT NOT NULL, -- 'Paid', 'Sent', 'Overdue', 'Partial', 'Archived', 'Draft'
        is_archived INTEGER DEFAULT 0,
        created_by TEXT DEFAULT 'alex',
        created_by_name TEXT DEFAULT 'Alex Rivera',
        created_by_role TEXT DEFAULT 'Admin',
        archived_by TEXT,
        archived_at TEXT,
        notes TEXT,
        accounting_notes TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Migration check: Ensure ownership & archive columns exist in invoices
    cursor.execute("PRAGMA table_info(invoices)")
    inv_cols = [c[1] for c in cursor.fetchall()]
    for col_name, col_def in [
        ('is_archived', 'INTEGER DEFAULT 0'),
        ('created_by', "TEXT DEFAULT 'alex'"),
        ('created_by_name', "TEXT DEFAULT 'Alex Rivera'"),
        ('created_by_role', "TEXT DEFAULT 'Admin'"),
        ('archived_by', 'TEXT'),
        ('archived_at', 'TEXT'),
        ('accounting_notes', 'TEXT')
    ]:
        if col_name not in inv_cols:
            cursor.execute(f"ALTER TABLE invoices ADD COLUMN {col_name} {col_def}")

    # Invoice line items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoice_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        quantity REAL NOT NULL,
        unit_price REAL NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE
    )
    """)

    # Payments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER NOT NULL,
        payment_date TEXT NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL, -- 'Wire Transfer', 'ACH Direct Debit', 'Credit Card', 'Corporate Check'
        reference_no TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE
    )
    """)

    # Bills (Accounts Payable) table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_number TEXT UNIQUE NOT NULL,
        vendor_name TEXT NOT NULL,
        category TEXT NOT NULL,
        due_date TEXT NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL, -- 'Due', 'Pending Approval', 'Paid', 'Scheduled', 'Archived'
        is_archived INTEGER DEFAULT 0,
        created_by TEXT DEFAULT 'alex',
        created_by_name TEXT DEFAULT 'Alex Rivera',
        created_by_role TEXT DEFAULT 'Admin',
        archived_by TEXT,
        archived_at TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Migration check: Ensure ownership & archive columns exist in bills
    cursor.execute("PRAGMA table_info(bills)")
    bill_cols = [c[1] for c in cursor.fetchall()]
    for col_name, col_def in [
        ('is_archived', 'INTEGER DEFAULT 0'),
        ('created_by', "TEXT DEFAULT 'alex'"),
        ('created_by_name', "TEXT DEFAULT 'Alex Rivera'"),
        ('created_by_role', "TEXT DEFAULT 'Admin'"),
        ('archived_by', 'TEXT'),
        ('archived_at', 'TEXT')
    ]:
        if col_name not in bill_cols:
            cursor.execute(f"ALTER TABLE bills ADD COLUMN {col_name} {col_def}")

    # Audit Trail table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_trail (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        action TEXT NOT NULL,
        user_name TEXT NOT NULL,
        details TEXT NOT NULL,
        ip_address TEXT DEFAULT '127.0.0.1'
    )
    """)

    # Journal Entries table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS journal_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_number TEXT NOT NULL,
        date TEXT NOT NULL,
        account_name TEXT NOT NULL,
        account_type TEXT NOT NULL, -- 'Asset', 'Liability', 'Equity', 'Revenue', 'Expense'
        debit REAL DEFAULT 0,
        credit REAL DEFAULT 0,
        description TEXT NOT NULL,
        created_by TEXT DEFAULT 'alex',
        created_by_role TEXT DEFAULT 'Admin'
    )
    """)

    # Migration check: Ensure ownership columns exist in journal_entries
    cursor.execute("PRAGMA table_info(journal_entries)")
    je_cols = [c[1] for c in cursor.fetchall()]
    for col_name, col_def in [
        ('created_by', "TEXT DEFAULT 'alex'"),
        ('created_by_role', "TEXT DEFAULT 'Admin'")
    ]:
        if col_name not in je_cols:
            cursor.execute(f"ALTER TABLE journal_entries ADD COLUMN {col_name} {col_def}")

    # Role-targeted Notifications table (User -> Accounting Staff & Confirmation back to User)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_role TEXT NOT NULL,
        target_username TEXT,
        notif_type TEXT NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        record_kind TEXT,
        record_id INTEGER,
        ref_number TEXT,
        created_by_name TEXT,
        is_read INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """)

    # Users table for Login Validation & Account Management
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        created_by TEXT DEFAULT 'Self-Registered (Portal)',
        token TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Migration check: Ensure created_by column exists in users & normalize legacy roles to 3-role RBAC
    cursor.execute("PRAGMA table_info(users)")
    user_cols = [c[1] for c in cursor.fetchall()]
    if 'created_by' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN created_by TEXT DEFAULT 'Self-Registered (Portal)'")

    cursor.execute("UPDATE users SET role = 'Admin' WHERE role = 'Chief Financial Officer'")
    cursor.execute("UPDATE users SET role = 'Accounting Staff' WHERE role IN ('Financial Analyst', 'Student / Accounting Staff')")
    cursor.execute("UPDATE users SET role = 'User' WHERE role = 'Auditor & Treasury Officer'")
    cursor.execute("UPDATE users SET created_by = 'System Default' WHERE username = 'alex' AND (created_by IS NULL OR created_by = 'Self-Registered (Portal)')")
    cursor.execute("UPDATE users SET created_by = 'Self-Registered (Portal)' WHERE created_by IS NULL")

    conn.commit()

    # Keep financial tables clean unless explicitly seeded; only ensure at least one login account exists.
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    if user_count == 0:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        INSERT INTO users (username, email, password_hash, full_name, role, created_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "alex",
            "alex.rivera@acmeglobal.com",
            generate_password_hash("password123"),
            "Alex Rivera",
            "Admin",
            "System Default",
            now_str
        ))
        conn.commit()

    conn.close()

def seed_data(cursor):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Seed Invoices matching picture exactly
    invoices_data = [
        (
            "#INV-2024-001",
            "Apex Cloud Technologies",
            "billing@apexcloud.io",
            "2024-10-01",
            "Oct 25, 2024",
            0,
            48000.00,
            0.0,
            48000.00,
            48000.00,
            0.00,
            "Paid",
            "Enterprise Multi-Cloud Infrastructure Consulting - Q4 retainer",
            now_str
        ),
        (
            "#INV-2024-002",
            "Vanguard Financial Partners",
            "ap@vanguardpartners.com",
            "2024-10-05",
            "Oct 28, 2024",
            0,
            125000.00,
            0.0,
            125000.00,
            0.00,
            125000.00,
            "Sent",
            "High-frequency algorithmic risk management module implementation",
            now_str
        ),
        (
            "#INV-2024-003",
            "Horizon Robotics Corp",
            "finance@horizonrobotics.ai",
            "2024-09-15",
            "Oct 13, 2024",
            1,
            25000.00,
            0.0,
            25000.00,
            0.00,
            25000.00,
            "Overdue",
            "Computer Vision & Sensor Fusion Subsystem Verification",
            now_str
        ),
        (
            "#INV-2024-004",
            "Nexus AI Research Lab",
            "accounts@nexusresearch.org",
            "2024-10-02",
            "Nov 01, 2024",
            0,
            80000.00,
            0.0,
            80000.00,
            50000.00,
            30000.00,
            "Partial",
            "Foundational LLM Fine-Tuning Pipeline Architecture",
            now_str
        ),
        (
            "#INV-2024-005",
            "Sovereign Logistics International",
            "treasury@sovereignlog.com",
            "2024-10-10",
            "Nov 02, 2024",
            0,
            64500.00,
            0.0,
            64500.00,
            0.00,
            64500.00,
            "Sent",
            "Global Freight Dispatch Optimization & Fleet Tracking API",
            now_str
        ),
        # Extra realistic invoices to match total 42 invoices and full total ₱842,500.00
        (
            "#INV-2024-006",
            "AeroDynamics Defense Systems",
            "procure@aerodynamics.mil",
            "2024-10-12",
            "Nov 08, 2024",
            0,
            150000.00,
            0.0,
            150000.00,
            0.00,
            150000.00,
            "Sent",
            "Secure Telemetry & Embedded Flight Guidance Firmware",
            now_str
        ),
        (
            "#INV-2024-007",
            "HyperScale Data Centers",
            "payables@hyperscaledc.net",
            "2024-10-14",
            "Nov 15, 2024",
            0,
            110000.00,
            0.0,
            110000.00,
            0.00,
            110000.00,
            "Sent",
            "Liquid Cooling Energy Efficiency Analytics Suite",
            now_str
        ),
        (
            "#INV-2024-008",
            "Quantum Capital Strategies",
            "invoicing@quantumcap.fund",
            "2024-10-16",
            "Nov 18, 2024",
            0,
            240000.00,
            0.0,
            240000.00,
            0.00,
            240000.00,
            "Sent",
            "Realtime Liquidity Execution & Risk Arb Engine",
            now_str
        ),
        (
            "#INV-2024-009",
            "Synthetix BioPharma Corp",
            "billing@synthetixbio.com",
            "2024-10-17",
            "Nov 20, 2024",
            0,
            98000.00,
            0.0,
            98000.00,
            0.00,
            98000.00,
            "Sent",
            "Computational Drug Discovery Grid Infrastructure",
            now_str
        )
    ]

    for inv in invoices_data:
        cursor.execute("""
        INSERT INTO invoices (
            invoice_number, client_name, client_email, issue_date, due_date,
            is_overdue, subtotal, tax, total_amount, paid_amount, balance_due,
            status, notes, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, inv)
        inv_id = cursor.lastrowid

        # Insert line items
        cursor.execute("""
        INSERT INTO invoice_items (invoice_id, description, quantity, unit_price, total)
        VALUES (?, ?, ?, ?, ?)
        """, (inv_id, inv[12], 1, inv[8], inv[8]))

    # Seed payment for #INV-2024-001 (₱48,000 paid)
    cursor.execute("""
    INSERT INTO payments (invoice_id, payment_date, amount, payment_method, reference_no, notes, created_at)
    VALUES (1, '2024-10-24', 48000.00, 'Wire Transfer', 'WT-99382104-FED', 'Full invoice settlement received via FedWire', ?)
    """, (now_str,))

    # Seed payment for #INV-2024-004 (₱50,000 partial paid)
    cursor.execute("""
    INSERT INTO payments (invoice_id, payment_date, amount, payment_method, reference_no, notes, created_at)
    VALUES (4, '2024-10-20', 50000.00, 'ACH Direct Debit', 'ACH-7821033', 'Milestone 1 progress payment', ?)
    """, (now_str,))

    # Seed Bills (Accounts Payable - 18 due)
    bills_data = [
        ("BILL-2024-101", "AWS Cloud Infrastructure", "Cloud & Hosting", "Nov 05, 2024", 42150.00, "Due"),
        ("BILL-2024-102", "Silicon Valley Law Group", "Legal & Compliance", "Nov 07, 2024", 18500.00, "Due"),
        ("BILL-2024-103", "Datadog Observability", "DevOps & Tooling", "Nov 10, 2024", 12300.00, "Due"),
        ("BILL-2024-104", "Snowflake Data Cloud", "Data Warehousing", "Nov 12, 2024", 31200.00, "Due"),
        ("BILL-2024-105", "Equinix Colocation DC-6", "Infrastructure", "Nov 14, 2024", 28000.00, "Pending Approval"),
        ("BILL-2024-106", "KPMG Audit & Tax Advisory", "Professional Services", "Nov 20, 2024", 65000.00, "Scheduled"),
        ("BILL-2024-107", "Slack Technologies / Salesforce", "SaaS Subscriptions", "Nov 22, 2024", 8400.00, "Due"),
        ("BILL-2024-108", "Google Workspace & GCP", "Enterprise Services", "Nov 25, 2024", 16800.00, "Due"),
    ]
    for b in bills_data:
        cursor.execute("""
        INSERT INTO bills (bill_number, vendor_name, category, due_date, amount, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (b[0], b[1], b[2], b[3], b[4], b[5], now_str))

    # Seed Audit Trail
    audit_events = [
        ("2024-10-24 14:32:10", "PAYMENT_RECORDED", "Alex Rivera (CFO)", "Recorded payment of ₱48,000.00 for #INV-2024-001 from Apex Cloud"),
        ("2024-10-20 09:15:44", "PARTIAL_PAYMENT", "Alex Rivera (CFO)", "Received milestone payment ₱50,000.00 for #INV-2024-004"),
        ("2024-10-18 11:00:22", "OVERDUE_FLAGGED", "Automated Velocity Engine", "Invoice #INV-2024-003 flagged overdue (₱25,000.00)"),
        ("2024-10-16 16:40:05", "INVOICE_GENERATED", "Alex Rivera (CFO)", "Generated invoice #INV-2024-008 to Quantum Capital Strategies"),
        ("2024-10-15 08:00:00", "FIFO_MATCH_EXECUTED", "Velocity Engine", "FIFO Automated Match reconciled 3 bank deposits with open receivables")
    ]
    for a in audit_events:
        cursor.execute("""
        INSERT INTO audit_trail (timestamp, action, user_name, details)
        VALUES (?, ?, ?, ?)
        """, a)

    # Seed Journal Entries (General Ledger)
    journal_data = [
        ("JE-2024-8801", "2024-10-24", "1010 - Operating Cash (Silicon Valley Bank)", "Asset", 48000.00, 0.00, "Payment receipt for #INV-2024-001"),
        ("JE-2024-8801", "2024-10-24", "1200 - Accounts Receivable", "Asset", 0.00, 48000.00, "Relieve AR for #INV-2024-001"),
        ("JE-2024-8802", "2024-10-20", "1010 - Operating Cash (Silicon Valley Bank)", "Asset", 50000.00, 0.00, "Partial payment for #INV-2024-004"),
        ("JE-2024-8802", "2024-10-20", "1200 - Accounts Receivable", "Asset", 0.00, 50000.00, "Partial relief of AR for #INV-2024-004"),
        ("JE-2024-8803", "2024-10-16", "1200 - Accounts Receivable", "Asset", 240000.00, 0.00, "Billing Quantum Capital Strategies"),
        ("JE-2024-8803", "2024-10-16", "4010 - Enterprise Software & Consulting Revenue", "Revenue", 0.00, 240000.00, "Recognize revenue #INV-2024-008")
    ]
    for j in journal_data:
        cursor.execute("""
        INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, j)

    # Seed Users for Login Validation & Verification Process
    cursor.execute("""
    INSERT INTO users (username, email, password_hash, full_name, role, created_by, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "alex",
        "alex.rivera@acmeglobal.com",
        generate_password_hash("password123"),
        "Alex Rivera",
        "Admin",
        "System Default",
        now_str
    ))

if __name__ == "__main__":
    init_db()
    print("LedgerCraft PRO database initialized successfully.")
