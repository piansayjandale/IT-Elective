# LedgerCraft PRO - Financial OS (100% Pure Python Architecture)

An Enterprise Full-Stack Accounting & Treasury Web System built **100% in pure Python** with **Reflex State Architecture**, **SQLite**, and **Flask**, with **all HTML template files removed and replaced by modular Python components**.

---

## 🌟 Key Features

### 1. 100% Pure Python UI & Reflex Architecture (Zero HTML Files)
* **Template-Free Pure Python**: All HTML files (`templates/`) have been completely removed and replaced by:
  * [`python_ui.py`](file:///c:/Users/mesco/Documents/IT%20Elective/python_ui.py): Modular Python UI generator and view components.
  * [`ledgercraft_app.py`](file:///c:/Users/mesco/Documents/IT%20Elective/ledgercraft_app.py) & [`rxconfig.py`](file:///c:/Users/mesco/Documents/IT%20Elective/rxconfig.py): Native pure Python Reflex application.
  * [`reflex_state.py`](file:///c:/Users/mesco/Documents/IT%20Elective/reflex_state.py): Clean Reflex reactive state architecture with `@rx.var` computed properties.

### 2. Fully Functional Role Permissions (RBAC)
* **Chief Financial Officer (Admin)**: Full administrative CRUD privileges (Create, Edit, Archive, Restore, Delete, Settle Bills, Record Payments).
* **Financial Analyst**: Operations-level control (Create, Edit, Archive, Record Payments).
* **Auditor & Treasury Officer**: Strict Read-Only compliance view (Attempting mutating operations returns `403 Forbidden` and surfaces an RBAC access restricted modal).
* **Student / Accounting Staff**: Trainee access with Draft review routing.
* **Header Role Switcher**: Quick-switch dropdown in the top navigation bar to test role permissions instantly.

### 3. Complete CRUD with Invoices Table Archive Icon
* **Create (C)**: New invoice modal with dynamic reactive multi-item cart.
* **Read (R)**: Real-time searchable and filterable invoice ledger with pagination, status filters (including `Status: Archived`), and official tax invoice voucher preview.
* **Update (U)**: Edit modal with dynamic line items, real-time recalculation of subtotals, 12% VAT, and grand totals.
* **Delete / Archive / Restore (D/A/R)**:
  * **Archive Icon (🗄️)**: Directly rendered in the `ACTION` column of every active invoice row.
  * **Restore**: One-click restore button on archived rows bringing invoices back to the active ledger.
  * **Delete**: CFO-only permanent purge.

### 4. Real-Time Reactive Cart & Live Admin Sync
* **Philippine Peso (₱)**: All monetary figures across status cards, invoices, carts, vouchers, and bills use `₱` (PHP).
* **Reactive Cart Engine**: Live recalculations for quantities, unit rates, 12% Philippine VAT, and grand totals.
* **Live Admin Sync**: Heartbeat sync (`/api/admin/sync`) polls every 8s with an animated pulsing indicator in the header.

### 5. Accounts Payable & General Ledger
* **Bills Ledger**: One-click "Pay Bill" for vendor liabilities.
* **FIFO Auto-Match Engine**: Intelligently reconciles incoming unallocated bank feeds with oldest receivables.
* **Double-Entry Journal Entries**: Debits = Credits verified.
* **Immutable Audit Trail**: Chronological event log tracking all financial operations.

---

## 🚀 How to Run

### Option 1: Standard Pure Python Server
```bash
python web.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000/?guest=1
```

### Option 2: Pure Python Reflex Application
```bash
reflex run
```
Open your browser and navigate to:
```
http://localhost:3000
```

---

## 📁 Pure Python Project Structure
```
IT Elective/
├── web.py                 # Pure Python web server and RESTful API endpoints
├── python_ui.py           # Pure Python UI generator (replaces all HTML templates)
├── ledgercraft_app.py     # Native Reflex pure Python application
├── reflex_state.py        # Clean Reflex reactive state architecture (RBAC, CRUD, Cart)
├── rxconfig.py            # Reflex configuration
├── database.py            # SQLite schema, migrations, and seed data
├── ledgercraft.db         # Persistent SQLite database
├── static/                # Brand logos & media assets
└── README.md              # Project documentation
```
*(Notice: ZERO `.html` files in the repository)*
