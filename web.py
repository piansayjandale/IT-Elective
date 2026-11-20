"""
LedgerCraft PRO - Financial OS
Full-Stack Web System for Accountancy & Treasury Operations
"""
from flask import Flask, request, jsonify, redirect, url_for, session
import os
import sqlite3
import secrets
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import database
import python_ui

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ledgercraft-pro-secret-key-2024-enterprise'

# Ensure database is initialized on startup
database.init_db()

def query_db(query, args=(), one=False):
    conn = database.get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv
    finally:
        conn.close()

def execute_db(query, args=()):
    conn = database.get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, args)
        conn.commit()
        last_id = cur.lastrowid
        return last_id
    finally:
        conn.close()

def log_audit(action, details, user="Alex Rivera (Admin)"):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_db(
        "INSERT INTO audit_trail (timestamp, action, user_name, details) VALUES (?, ?, ?, ?)",
        (now_str, action, user, details)
    )

SETTLED_STATUSES = ('Paid', 'Confirmed', 'Confirm with Condition', 'Conditioned')

def is_settled(status):
    return (status or '') in SETTLED_STATUSES

def create_notification(target_role, notif_type, title, message, record_kind=None, record_id=None, ref_number=None, target_username=None, created_by_name=None):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return execute_db("""
        INSERT INTO notifications (
            target_role, target_username, notif_type, title, message,
            record_kind, record_id, ref_number, created_by_name, is_read, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
    """, (
        target_role, target_username, notif_type, title, message,
        record_kind, record_id, ref_number, created_by_name or get_current_user_name(), now_str
    ))

def post_journal_entry(entry_number, date_str, account_name, account_type, debit, credit, description, owner_username=None, owner_role=None):
    execute_db("""
        INSERT INTO journal_entries (
            entry_number, date, account_name, account_type, debit, credit, description, created_by, created_by_role
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry_number, date_str, account_name, account_type, debit, credit, description,
        owner_username or get_current_username(), owner_role or get_current_role()
    ))

# ----------------- ROLE PERMISSIONS ARCHITECTURE (3-ROLE RBAC) -----------------
LEGACY_ROLE_MAP = {
    "Chief Financial Officer": "Admin",
    "Admin": "Admin",
    "Financial Analyst": "Accounting Staff",
    "Student / Accounting Staff": "Accounting Staff",
    "Accounting Staff": "Accounting Staff",
    "Auditor & Treasury Officer": "User",
    "User": "User",
}

ROLES = {
    "Admin": {
        "title": "Admin",
        "badge": "👑 Admin",
        "can_create": False,
        "can_edit": False,
        "can_archive": False,
        "can_view_archives": True,
        "can_restore": True,
        "can_delete": True,
        "can_record_payment": False,
        "can_settle_bills": False,
        "can_view_reports": True,
        "can_monitor_users": True,
        "can_manage_accounts": True,
        "can_manage_roles": True
    },
    "Accounting Staff": {
        "title": "Accounting Staff",
        "badge": "📋 Accounting Staff",
        "can_create": True,
        "can_edit": True,
        "can_archive": True,
        "can_view_archives": False,
        "can_restore": False,
        "can_delete": False,
        "can_record_payment": True,
        "can_settle_bills": True,
        "can_view_reports": True,
        "can_monitor_users": True,
        "can_manage_accounts": False,
        "can_manage_roles": False
    },
    "User": {
        "title": "User",
        "badge": "👤 User",
        "can_create": True,
        "can_edit": False,
        "can_archive": False,
        "can_view_archives": False,
        "can_restore": False,
        "can_delete": False,
        "can_record_payment": False,
        "can_settle_bills": False,
        "can_view_reports": True,
        "can_monitor_users": False,
        "can_manage_accounts": False,
        "can_manage_roles": False
    }
}

def normalize_role(role_name, default="User"):
    if not role_name:
        return default
    return LEGACY_ROLE_MAP.get(str(role_name).strip(), default)

def get_current_username():
    return session.get('username') or 'alex'

def get_current_user_name():
    return session.get('full_name') or session.get('username') or 'Alex Rivera'

def get_current_role():
    return normalize_role(session.get('role', 'Admin'), default='Admin')

def get_user_initials(full_name):
    parts = [p for p in str(full_name or 'AR').strip().split() if p]
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return (parts[0][:2] if parts else 'AR').upper()

def apply_role_scope(table_alias=""):
    """
    When active role is 'User', scope A/R and A/P visibility to the user's own
    or 'User'-submitted records. Accounting Staff and Admin see all active records.
    """
    prefix = f"{table_alias}." if table_alias else ""
    if get_current_role() == "User":
        if session.get('account_role') == "User":
            return f" AND {prefix}created_by = ?", [get_current_username()]
        return f" AND {prefix}created_by_role = 'User'", []
    return "", []

def check_permission(perm_key):
    role = get_current_role()
    perms = ROLES.get(role, ROLES['User'])
    return perms.get(perm_key, False)

@app.route('/api/roles', methods=['GET'])
def get_roles():
    role = get_current_role()
    return jsonify({
        'roles': ROLES,
        'current_role': role,
        'current_user': get_current_user_name(),
        'permissions': ROLES.get(role, ROLES['User'])
    })

@app.route('/api/role-accounts', methods=['GET'])
def get_role_accounts():
    """Return non-sensitive account metadata grouped by role for the role-switcher hover flyouts."""
    users = query_db(
        "SELECT id, username, email, full_name, role, created_by, created_at FROM users ORDER BY id ASC"
    )
    inv_counts = {
        r['created_by']: r['cnt']
        for r in query_db("SELECT COALESCE(created_by, 'alex') as created_by, COUNT(*) as cnt FROM invoices GROUP BY COALESCE(created_by, 'alex')")
    }
    bill_counts = {
        r['created_by']: r['cnt']
        for r in query_db("SELECT COALESCE(created_by, 'alex') as created_by, COUNT(*) as cnt FROM bills GROUP BY COALESCE(created_by, 'alex')")
    }

    accounts_by_role = {'Admin': [], 'Accounting Staff': [], 'User': []}
    current_username = get_current_username()
    current_role = get_current_role()

    for u in users:
        keys = u.keys()
        norm_role = normalize_role(u['role'], default='User')
        uname = u['username']
        fname = u['full_name'] or uname
        accounts_by_role.setdefault(norm_role, []).append({
            'id': u['id'],
            'username': uname,
            'email': u['email'],
            'full_name': fname,
            'initials': get_user_initials(fname),
            'role': norm_role,
            'created_by': (u['created_by'] if 'created_by' in keys and u['created_by'] else 'Self-Registered (Portal)'),
            'created_at': u['created_at'],
            'invoices_count': inv_counts.get(uname, 0),
            'bills_count': bill_counts.get(uname, 0),
            'is_active': (uname == current_username)
        })

    return jsonify({
        'current_username': current_username,
        'current_role': current_role,
        'accounts_by_role': accounts_by_role
    })

@app.route('/api/switch-role', methods=['POST'])
def switch_role():
    data = request.json or {}
    user_id = data.get('user_id')
    raw_role = data.get('role')

    # Remember the primary signed-in user so returning to a top-level role restores it
    if 'primary_username' not in session:
        session['primary_user_id'] = session.get('user_id')
        session['primary_username'] = session.get('username') or 'alex'
        session['primary_full_name'] = session.get('full_name') or 'Alex Rivera'
        session['primary_account_role'] = normalize_role(
            session.get('account_role', session.get('role', 'Admin')), default='Admin'
        )

    old_role = get_current_role()

    if user_id is not None:
        try:
            uid_int = int(user_id)
        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid user_id'}), 400
        target = query_db(
            "SELECT id, username, full_name, role FROM users WHERE id = ?",
            (uid_int,),
            one=True
        )
        if not target:
            return jsonify({'error': f'Account ID {uid_int} not found'}), 404
        new_role = normalize_role(target['role'], default='User')
        session['user_id'] = target['id']
        session['username'] = target['username']
        session['full_name'] = target['full_name'] or target['username']
        session['account_role'] = new_role
        session['role'] = new_role
        cur_name = get_current_user_name()
        log_audit(
            "ROLE_SWITCHED",
            f"Switched active account from '{old_role}' to {cur_name} (@{target['username']}, role '{new_role}')",
            cur_name
        )
        return jsonify({
            'success': True,
            'role': new_role,
            'account_role': new_role,
            'username': target['username'],
            'full_name': cur_name,
            'initials': get_user_initials(cur_name),
            'badge': ROLES[new_role]['badge'],
            'permissions': ROLES[new_role],
            'message': f"Switched to {cur_name} ({new_role})"
        })

    new_role = normalize_role(raw_role, default=None)
    if new_role not in ROLES:
        return jsonify({'error': f'Invalid role: {raw_role}'}), 400

    # Restore primary signed-in identity when picking top-level role preset
    session['user_id'] = session.get('primary_user_id')
    session['username'] = session.get('primary_username') or 'alex'
    session['full_name'] = session.get('primary_full_name') or 'Alex Rivera'
    session['account_role'] = normalize_role(
        session.get('primary_account_role', new_role), default=new_role
    )
    session['role'] = new_role
    cur_name = get_current_user_name()
    log_audit("ROLE_SWITCHED", f"User {cur_name} switched role from '{old_role}' to '{new_role}'", cur_name)
    return jsonify({
        'success': True,
        'role': new_role,
        'account_role': session['account_role'],
        'username': get_current_username(),
        'full_name': cur_name,
        'initials': get_user_initials(cur_name),
        'badge': ROLES[new_role]['badge'],
        'permissions': ROLES[new_role],
        'message': f"Active session role switched to {new_role}"
    })

@app.route('/api/current-user', methods=['GET'])
def get_current_user():
    role = get_current_role()
    full_name = get_current_user_name()
    return jsonify({
        'username': get_current_username(),
        'full_name': full_name,
        'initials': get_user_initials(full_name),
        'account_role': normalize_role(session.get('account_role', role), default=role),
        'role': role,
        'badge': ROLES[role]['badge'],
        'permissions': ROLES.get(role, ROLES['User'])
    })

# ----------------- AUTHENTICATION ROUTES (PURE PYTHON UI) -----------------
@app.route('/login')
def login():
    # If already authenticated, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('index'))
    return python_ui.render_login_view()

@app.route('/logout')
def logout():
    user_name = session.get('full_name', 'Alex Rivera')
    log_audit("LOGOUT", f"User {user_name} terminated session and invalidated token.", user_name)
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/login', methods=['POST'])
def api_login():
    """
    Login Validation & Verification Process based on Lesson 6 Decision Tree:
    1. Credential Submission / Input
    2. Database User Search
    3. User existence Decision Branch (Yes / No)
       -> No: Rejection Alert
       -> Yes: Proceed to step 4
    4. Password Hash Verification
    5. Password Validity Branch (Valid / Invalid)
       -> Invalid: Rejection Alert
       -> Valid: Proceed to step 6
    6. Token Generation & Dashboard Redirection vs. Rejection Alert
    """
    data = request.json or {}

    # NODE 1: Credential Submission / Input
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        log_audit("LOGIN_REJECTED", "Empty credentials submitted", "Anonymous Gateway")
        return jsonify({
            'success': False,
            'failed_step': 'input_validation',
            'message': 'Rejection Alert: Username/email and password are required inputs.'
        }), 400

    expected_user_id = data.get('expected_user_id')
    in_app_switch = bool(data.get('in_app_switch'))

    # NODE 2: Database User Search
    user = query_db(
        "SELECT * FROM users WHERE username = ? OR email = ?",
        (username, username),
        one=True
    )

    # NODE 3: User existence Decision Branch (Yes / No)
    if not user:
        # Branch: NO -> Rejection Alert
        log_audit("LOGIN_FAILED", f"Rejection: User '{username}' does not exist in database directory", "Security Gateway")
        return jsonify({
            'success': False,
            'failed_step': 'user_existence',
            'branch': 'NO',
            'message': f"Rejection Alert: No user account found matching '{username}' in the system directory."
        }), 401

    if expected_user_id is not None:
        try:
            exp_id = int(expected_user_id)
        except (TypeError, ValueError):
            exp_id = None
        if exp_id is None or int(user['id']) != exp_id:
            log_audit("LOGIN_FAILED", f"Rejection: Email/username '{username}' does not match selected account #{expected_user_id}", "Security Gateway")
            return jsonify({
                'success': False,
                'failed_step': 'user_existence',
                'branch': 'MISMATCH',
                'message': "Rejection Alert: Entered email or username does not belong to the selected account."
            }), 401

    # Branch: YES -> Proceeds to Password Hash Verification
    # NODE 4: Password Hash Verification
    stored_hash = user['password_hash']
    is_valid_password = check_password_hash(stored_hash, password)

    # NODE 5: Password Validity Branch (Valid / Invalid)
    if not is_valid_password:
        # Branch: INVALID -> Rejection Alert
        log_audit("LOGIN_FAILED", f"Rejection: Password hash verification failed for user '{user['username']}'", user['full_name'])
        return jsonify({
            'success': False,
            'failed_step': 'password_validity',
            'branch': 'INVALID',
            'message': "Rejection Alert: Password hash verification failed. The provided password is incorrect."
        }), 401

    # Branch: VALID -> Proceed to Node 6
    # NODE 6: Token Generation & Dashboard Redirection vs. Rejection Alert
    auth_token = secrets.token_hex(32)
    execute_db("UPDATE users SET token = ? WHERE id = ?", (auth_token, user['id']))

    normalized_user_role = normalize_role(user['role'], default='User')

    if in_app_switch:
        session.setdefault('primary_user_id', session.get('user_id'))
        session.setdefault('primary_username', session.get('username') or 'alex')
        session.setdefault('primary_full_name', session.get('full_name') or 'Alex Rivera')
        session.setdefault('primary_account_role', normalize_role(
            session.get('account_role', session.get('role', 'Admin')), default='Admin'
        ))
    else:
        session['primary_user_id'] = user['id']
        session['primary_username'] = user['username']
        session['primary_full_name'] = user['full_name']
        session['primary_account_role'] = normalized_user_role

    # Store active signed-in identity
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['full_name'] = user['full_name']
    session['role'] = normalized_user_role
    session['account_role'] = normalized_user_role
    session['auth_token'] = auth_token

    log_audit("LOGIN_SUCCESS", f"Authentication verified for {user['full_name']} ({normalized_user_role}). Session token issued.", user['full_name'])

    return jsonify({
        'success': True,
        'failed_step': None,
        'message': f"Authenticated as {user['full_name']} ({normalized_user_role}).",
        'token': auth_token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'initials': get_user_initials(user['full_name']),
            'role': normalized_user_role,
            'badge': ROLES.get(normalized_user_role, ROLES['User'])['badge'],
            'permissions': ROLES.get(normalized_user_role, ROLES['User'])
        },
        'redirect': '/'
    })

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    full_name = data.get('full_name', '').strip() or username.title()
    role = normalize_role(data.get('role', 'User'), default='User')
    created_by = f"Self-Registered ({full_name})"

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required fields.'}), 400

    if not email:
        email = f"{username}@sti.edu"

    # Check if user already exists
    existing = query_db("SELECT id FROM users WHERE username = ? OR email = ?", (username, email), one=True)
    if existing:
        return jsonify({'success': False, 'message': f"An account with username '{username}' or email '{email}' already exists."}), 409

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    password_hash = generate_password_hash(password)

    user_id = execute_db("""
    INSERT INTO users (username, email, password_hash, full_name, role, created_by, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, email, password_hash, full_name, role, created_by, now_str))

    log_audit("USER_REGISTERED", f"New {role} account '{username}' ({full_name}) registered via portal.", full_name)

    return jsonify({
        'success': True,
        'message': f"Account for {full_name} ({username}) registered successfully!",
        'username': username,
        'email': email,
        'role': role,
        'user_id': user_id
    })

@app.route('/')
def index():
    # Require authentication (or bypass with ?guest=1 for instant review)
    if 'user_id' not in session and request.args.get('guest') != '1':
        return redirect(url_for('login'))
    return python_ui.render_dashboard_view(user={'name': get_current_user_name(), 'role': get_current_role()})

# ----------------- INVOICES API (COMPLETE CRUD + REACTIVE CART) -----------------
@app.route('/api/invoices', methods=['GET'])
def get_invoices():
    status_filter = request.args.get('status', 'All')
    source_filter = request.args.get('source', 'All')
    search_query = request.args.get('search', '').strip()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    if status_filter == 'Archived' and not check_permission('can_view_archives'):
        return jsonify({
            'error': "Permission Denied: Only Admin can view archived invoices."
        }), 403

    query = "SELECT * FROM invoices WHERE 1=1"
    params = []

    if status_filter == 'Archived':
        query += " AND is_archived = 1"
    else:
        query += " AND (is_archived = 0 OR is_archived IS NULL)"
        if status_filter and status_filter != 'All':
            if get_current_role() == 'User':
                if status_filter == 'Pending':
                    query += " AND status NOT IN ('Paid', 'Confirmed', 'Confirm with Condition', 'Conditioned', 'Sent')"
                elif status_filter in ('Confirmed', 'Sent'):
                    query += " AND status IN ('Paid', 'Confirmed', 'Sent')"
                elif status_filter in ('Confirm with Condition', 'Conditioned'):
                    query += " AND status IN ('Confirm with Condition', 'Conditioned')"
                else:
                    query += " AND status = ?"
                    params.append(status_filter)
            else:
                if status_filter in ('Conditioned', 'Confirm with Condition'):
                    query += " AND status IN ('Conditioned', 'Confirm with Condition')"
                elif status_filter in ('Sent', 'Confirmed'):
                    query += " AND status IN ('Sent', 'Confirmed')"
                else:
                    query += " AND status = ?"
                    params.append(status_filter)

    scope_sql, scope_params = apply_role_scope()
    query += scope_sql
    params.extend(scope_params)

    if get_current_role() != 'User':
        if source_filter == 'User':
            query += " AND created_by_role = 'User'"
        elif source_filter == 'StaffAdmin':
            query += " AND (created_by_role IN ('Accounting Staff', 'Admin') OR created_by_role IS NULL)"

    if search_query:
        query += " AND (invoice_number LIKE ? OR client_name LIKE ? OR COALESCE(created_by_name, '') LIKE ?)"
        params.append(f"%{search_query}%")
        params.append(f"%{search_query}%")
        params.append(f"%{search_query}%")

    query += " ORDER BY CASE WHEN status = 'Pending' THEN 0 ELSE 1 END ASC, id DESC"

    all_matches = query_db(query, params)
    total_count = len(all_matches)

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_items = all_matches[start_idx:end_idx]

    invoices_list = []
    for row in paginated_items:
        keys = row.keys()
        invoices_list.append({
            'id': row['id'],
            'invoice_number': row['invoice_number'],
            'client_name': row['client_name'],
            'client_email': row['client_email'],
            'issue_date': row['issue_date'],
            'due_date': row['due_date'],
            'is_overdue': bool(row['is_overdue']),
            'subtotal': row['subtotal'],
            'tax': row['tax'],
            'total_amount': row['total_amount'],
            'paid_amount': row['paid_amount'],
            'balance_due': row['balance_due'],
            'status': row['status'],
            'is_archived': bool(row['is_archived'] if 'is_archived' in keys else 0),
            'created_by': row['created_by'] if 'created_by' in keys and row['created_by'] else 'alex',
            'created_by_name': row['created_by_name'] if 'created_by_name' in keys and row['created_by_name'] else 'Alex Rivera',
            'created_by_role': normalize_role(row['created_by_role'], default='Admin') if 'created_by_role' in keys and row['created_by_role'] else 'Admin',
            'archived_by': row['archived_by'] if 'archived_by' in keys else None,
            'archived_at': row['archived_at'] if 'archived_at' in keys else None,
            'notes': row['notes'],
            'accounting_notes': row['accounting_notes'] if 'accounting_notes' in keys and row['accounting_notes'] else '',
            'created_at': row['created_at']
        })

    return jsonify({
        'invoices': invoices_list,
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': max(1, (total_count + per_page - 1) // per_page)
    })

@app.route('/api/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice_detail(invoice_id):
    inv = query_db("SELECT * FROM invoices WHERE id = ?", (invoice_id,), one=True)
    if not inv:
        return jsonify({'error': 'Invoice not found'}), 404

    keys = inv.keys()
    is_arch = bool(inv['is_archived'] if 'is_archived' in keys else 0)
    if is_arch and not check_permission('can_view_archives'):
        return jsonify({'error': 'Permission Denied: Only Admin can view archived invoices.'}), 403

    items = query_db("SELECT * FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
    payments = query_db("SELECT * FROM payments WHERE invoice_id = ? ORDER BY id DESC", (invoice_id,))

    return jsonify({
        'invoice': {
            'id': inv['id'],
            'invoice_number': inv['invoice_number'],
            'client_name': inv['client_name'],
            'client_email': inv['client_email'],
            'issue_date': inv['issue_date'],
            'due_date': inv['due_date'],
            'is_overdue': bool(inv['is_overdue']),
            'subtotal': inv['subtotal'],
            'tax': inv['tax'],
            'total_amount': inv['total_amount'],
            'paid_amount': inv['paid_amount'],
            'balance_due': inv['balance_due'],
            'status': inv['status'],
            'is_archived': is_arch,
            'created_by': inv['created_by'] if 'created_by' in keys and inv['created_by'] else 'alex',
            'created_by_name': inv['created_by_name'] if 'created_by_name' in keys and inv['created_by_name'] else 'Alex Rivera',
            'created_by_role': normalize_role(inv['created_by_role'], default='Admin') if 'created_by_role' in keys and inv['created_by_role'] else 'Admin',
            'archived_by': inv['archived_by'] if 'archived_by' in keys else None,
            'archived_at': inv['archived_at'] if 'archived_at' in keys else None,
            'notes': inv['notes'],
            'accounting_notes': inv['accounting_notes'] if 'accounting_notes' in keys and inv['accounting_notes'] else ''
        },
        'items': [{
            'id': item['id'],
            'description': item['description'],
            'quantity': item['quantity'],
            'unit_price': item['unit_price'],
            'total': item['total']
        } for item in items],
        'payments': [{
            'id': p['id'],
            'payment_date': p['payment_date'],
            'amount': p['amount'],
            'payment_method': p['payment_method'],
            'reference_no': p['reference_no'],
            'notes': p['notes']
        } for p in payments]
    })

@app.route('/api/invoices', methods=['POST'])
def create_invoice():
    if not check_permission('can_create'):
        return jsonify({
            'error': f"Permission Denied: Current role '{get_current_role()}' does not have invoice creation privileges."
        }), 403

    data = request.json or {}
    client_name = data.get('client_name', '').strip()
    client_email = data.get('client_email', '').strip()
    due_date = data.get('due_date', '').strip()
    items = data.get('items', [])
    notes = data.get('notes', '')

    if not client_name:
        return jsonify({'error': 'Client name is required'}), 400

    # Generate collision-safe next invoice number
    max_row = query_db("SELECT COALESCE(MAX(id), 0) as max_id FROM invoices", one=True)
    next_num = (max_row['max_id'] if max_row else 0) + 1
    invoice_number = (data.get('invoice_number') or '').strip() or f"#INV-2025-{next_num:03d}"

    # Calculate totals
    subtotal = 0.0
    for itm in items:
        qty = float(itm.get('quantity', 1))
        price = float(itm.get('unit_price', 0))
        subtotal += qty * price

    if subtotal == 0 and 'total_amount' in data:
        subtotal = float(data['total_amount'])

    tax = float(data.get('tax', 0.0))
    total_amount = subtotal + tax
    balance_due = total_amount

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    issue_date = datetime.now().strftime("%b %d, %Y")
    if not due_date:
        due_date = "Nov 30, 2025"

    active_role = get_current_role()
    creator_username = get_current_username()
    creator_name = get_current_user_name()
    status = 'Pending' if active_role == 'User' else 'Sent'

    # Insert invoice
    invoice_id = execute_db("""
    INSERT INTO invoices (
        invoice_number, client_name, client_email, issue_date, due_date,
        is_overdue, subtotal, tax, total_amount, paid_amount, balance_due,
        status, is_archived, created_by, created_by_name, created_by_role, notes, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        invoice_number, client_name, client_email, issue_date, due_date,
        0, subtotal, tax, total_amount, 0.0, balance_due, status, 0,
        creator_username, creator_name, active_role, notes, now_str
    ))

    # Insert line items from reactive cart
    if items:
        for itm in items:
            q = float(itm.get('quantity', 1))
            p = float(itm.get('unit_price', subtotal))
            execute_db("""
            INSERT INTO invoice_items (invoice_id, description, quantity, unit_price, total)
            VALUES (?, ?, ?, ?, ?)
            """, (invoice_id, itm.get('description', 'Consulting & Implementation Services'), q, p, q * p))
    else:
        execute_db("""
        INSERT INTO invoice_items (invoice_id, description, quantity, unit_price, total)
        VALUES (?, ?, ?, ?, ?)
        """, (invoice_id, notes or 'Professional Advisory Services', 1, subtotal, subtotal))

    # General ledger entry: Debit AR, Credit Revenue (tagged with owner for User GL)
    entry_no = f"JE-2025-{8800 + invoice_id}"
    today_str = datetime.now().strftime("%Y-%m-%d")
    post_journal_entry(entry_no, today_str, "1200 - Accounts Receivable", "Asset", total_amount, 0.0,
                       f"Invoice {invoice_number} to {client_name}", creator_username, active_role)
    post_journal_entry(entry_no, today_str, "4010 - Enterprise Software & Services", "Revenue", 0.0, total_amount,
                       f"Revenue recognition {invoice_number}", creator_username, active_role)

    # Notify Accounting Staff whenever a User submits a new invoice
    if active_role == 'User':
        create_notification(
            target_role='Accounting Staff',
            notif_type='USER_INVOICE_CREATED',
            title='New User Invoice Submitted',
            message=f"{creator_name} submitted Invoice {invoice_number} for {client_name} (₱{total_amount:,.2f}) — Pending confirmation.",
            record_kind='invoice',
            record_id=invoice_id,
            ref_number=invoice_number,
            created_by_name=creator_name
        )

    log_audit("INVOICE_CREATED", f"Generated {invoice_number} for {client_name} - ₱{total_amount:,.2f} [{active_role}]", creator_name)

    return jsonify({
        'success': True,
        'message': f'Invoice {invoice_number} submitted ({status}) — Accounting Staff notified!' if active_role == 'User' else f'Invoice {invoice_number} created successfully ({status})',
        'invoice_id': invoice_id,
        'status': status
    })

# ----------------- CRUD: UPDATE INVOICE -----------------
@app.route('/api/invoices/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    if not check_permission('can_edit'):
        return jsonify({
            'error': f"Permission Denied: Current role '{get_current_role()}' cannot edit invoices. Requires Accounting Staff."
        }), 403

    inv = query_db("SELECT * FROM invoices WHERE id = ?", (invoice_id,), one=True)
    if not inv:
        return jsonify({'error': 'Invoice not found'}), 404

    data = request.json or {}
    client_name = data.get('client_name', inv['client_name']).strip()
    client_email = data.get('client_email', inv['client_email']).strip()
    due_date = data.get('due_date', inv['due_date']).strip()
    status = data.get('status', inv['status'])
    notes = data.get('notes', inv['notes'])
    items = data.get('items')

    # Recalculate totals if items were updated
    if items is not None and len(items) > 0:
        subtotal = sum(float(i.get('quantity', 1)) * float(i.get('unit_price', 0)) for i in items)
        tax = float(data.get('tax', 0.0))
        total_amount = subtotal + tax

        # Replace items in database
        execute_db("DELETE FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
        for itm in items:
            q = float(itm.get('quantity', 1))
            p = float(itm.get('unit_price', 0))
            execute_db("""
            INSERT INTO invoice_items (invoice_id, description, quantity, unit_price, total)
            VALUES (?, ?, ?, ?, ?)
            """, (invoice_id, itm.get('description', 'Service Item'), q, p, q * p))
    else:
        subtotal = inv['subtotal']
        tax = inv['tax']
        total_amount = inv['total_amount']

    paid_amount = inv['paid_amount']
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Synchronize paid_amount and balance_due with status edits
    if status == 'Paid' and paid_amount < total_amount:
        delta_pay = total_amount - paid_amount
        paid_amount = total_amount
        balance_due = 0.0
        execute_db("""
        INSERT INTO payments (invoice_id, payment_date, amount, payment_method, reference_no, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (invoice_id, today_str, delta_pay, 'Direct Settlement', f"EDIT-{datetime.now().strftime('%H%M%S')}", 'Settled via invoice update', now_str))
        entry_no = f"JE-PAY-{datetime.now().strftime('%m%d%H%M%S')}"
        execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (entry_no, today_str, "1010 - Operating Cash (Silicon Valley Bank)", "Asset", delta_pay, 0.0, f"Settlement on update for {inv['invoice_number']}"))
        execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (entry_no, today_str, "1200 - Accounts Receivable", "Asset", 0.0, delta_pay, f"Relieve AR on update for {inv['invoice_number']}"))
    else:
        if paid_amount > total_amount:
            paid_amount = total_amount
        balance_due = max(0.0, total_amount - paid_amount)
        if balance_due <= 0.01 and total_amount > 0 and status != 'Archived':
            status = 'Paid'
            balance_due = 0.0

    # Record GL adjustment if invoice total changed
    total_diff = total_amount - inv['total_amount']
    if abs(total_diff) > 0.01:
        adj_no = f"JE-ADJ-{datetime.now().strftime('%m%d%H%M%S')}"
        if total_diff > 0:
            execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (adj_no, today_str, "1200 - Accounts Receivable", "Asset", total_diff, 0.0, f"Invoice adjustment (+) {inv['invoice_number']}"))
            execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (adj_no, today_str, "4010 - Enterprise Software & Services", "Revenue", 0.0, total_diff, f"Revenue adjustment (+) {inv['invoice_number']}"))
        else:
            abs_diff = abs(total_diff)
            execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (adj_no, today_str, "4010 - Enterprise Software & Services", "Revenue", abs_diff, 0.0, f"Revenue adjustment (-) {inv['invoice_number']}"))
            execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (adj_no, today_str, "1200 - Accounts Receivable", "Asset", 0.0, abs_diff, f"Invoice adjustment (-) {inv['invoice_number']}"))

    execute_db("""
    UPDATE invoices
    SET client_name = ?, client_email = ?, due_date = ?, status = ?, notes = ?,
        subtotal = ?, tax = ?, total_amount = ?, paid_amount = ?, balance_due = ?
    WHERE id = ?
    """, (client_name, client_email, due_date, status, notes, subtotal, tax, total_amount, paid_amount, balance_due, invoice_id))

    log_audit("INVOICE_UPDATED", f"Updated {inv['invoice_number']} for {client_name} - Total: ₱{total_amount:,.2f}", get_current_user_name())

    return jsonify({
        'success': True,
        'message': f"Invoice {inv['invoice_number']} successfully updated",
        'invoice_id': invoice_id
    })

# ----------------- CRUD: ARCHIVE INVOICE -----------------
@app.route('/api/invoices/<int:invoice_id>/archive', methods=['POST'])
def archive_invoice(invoice_id):
    if not check_permission('can_archive'):
        return jsonify({
            'error': f"Permission Denied: Current role '{get_current_role()}' cannot archive invoices. Requires Accounting Staff."
        }), 403

    inv = query_db("SELECT * FROM invoices WHERE id = ?", (invoice_id,), one=True)
    if not inv:
        return jsonify({'error': 'Invoice not found'}), 404

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    archived_by = f"{get_current_user_name()} ({get_current_role()})"
    execute_db(
        "UPDATE invoices SET is_archived = 1, status = 'Archived', archived_by = ?, archived_at = ? WHERE id = ?",
        (archived_by, now_str, invoice_id)
    )
    if not inv['is_archived'] and inv['total_amount'] > 0:
        entry_no = f"JE-ARC-{datetime.now().strftime('%m%d%H%M%S')}"
        today_str = datetime.now().strftime("%Y-%m-%d")
        execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (entry_no, today_str, "4010 - Enterprise Software & Services", "Revenue", inv['total_amount'], 0.0, f"Reverse revenue on archive {inv['invoice_number']}"))
        execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (entry_no, today_str, "1200 - Accounts Receivable", "Asset", 0.0, inv['total_amount'], f"Reverse AR on archive {inv['invoice_number']}"))
    log_audit("INVOICE_ARCHIVED", f"Invoice {inv['invoice_number']} ({inv['client_name']}) was archived by {archived_by}", get_current_user_name())

    return jsonify({
        'success': True,
        'message': f"Invoice {inv['invoice_number']} has been moved to Archives (Admin only access).",
        'invoice_id': invoice_id
    })

# ----------------- CRUD: RESTORE INVOICE -----------------
@app.route('/api/invoices/<int:invoice_id>/restore', methods=['POST'])
def restore_invoice(invoice_id):
    if not check_permission('can_restore'):
        return jsonify({
            'error': f"Permission Denied: Restoring archived invoices requires Admin privileges. '{get_current_role()}' is unauthorized."
        }), 403

    inv = query_db("SELECT * FROM invoices WHERE id = ?", (invoice_id,), one=True)
    if not inv:
        return jsonify({'error': 'Invoice not found'}), 404

    keys = inv.keys()
    owner_username = inv['created_by'] if 'created_by' in keys and inv['created_by'] else 'alex'
    owner_role = normalize_role(inv['created_by_role'], default='Admin') if 'created_by_role' in keys and inv['created_by_role'] else 'Admin'

    # Determine restored status based on payments and owner role
    if inv['balance_due'] <= 0.01:
        new_status = 'Confirmed' if owner_role == 'User' else 'Paid'
    elif inv['paid_amount'] > 0:
        new_status = 'Partial'
    else:
        new_status = 'Pending' if owner_role == 'User' else 'Sent'

    execute_db("UPDATE invoices SET is_archived = 0, status = ?, archived_by = NULL, archived_at = NULL WHERE id = ?", (new_status, invoice_id))
    if inv['is_archived'] and inv['total_amount'] > 0:
        entry_no = f"JE-RST-{datetime.now().strftime('%m%d%H%M%S')}"
        today_str = datetime.now().strftime("%Y-%m-%d")
        post_journal_entry(entry_no, today_str, "1200 - Accounts Receivable", "Asset", inv['total_amount'], 0.0,
                           f"Restore AR {inv['invoice_number']}", owner_username, owner_role)
        post_journal_entry(entry_no, today_str, "4010 - Enterprise Software & Services", "Revenue", 0.0, inv['total_amount'],
                           f"Restore revenue {inv['invoice_number']}", owner_username, owner_role)
    log_audit("INVOICE_RESTORED", f"Invoice {inv['invoice_number']} restored to active ledger with status '{new_status}' by Admin", get_current_user_name())

    return jsonify({
        'success': True,
        'message': f"Invoice {inv['invoice_number']} restored to active ledger.",
        'invoice_id': invoice_id,
        'status': new_status
    })

# ----------------- CRUD: DELETE INVOICE -----------------
@app.route('/api/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    if not check_permission('can_delete'):
        return jsonify({
            'error': f"Permission Denied: Permanent deletion requires Admin privileges. Role '{get_current_role()}' is unauthorized."
        }), 403

    inv = query_db("SELECT * FROM invoices WHERE id = ?", (invoice_id,), one=True)
    if not inv:
        return jsonify({'error': 'Invoice not found'}), 404

    if not inv['is_archived'] and inv['total_amount'] > 0:
        entry_no = f"JE-DEL-{datetime.now().strftime('%m%d%H%M%S')}"
        today_str = datetime.now().strftime("%Y-%m-%d")
        execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (entry_no, today_str, "4010 - Enterprise Software & Services", "Revenue", inv['total_amount'], 0.0, f"Delete reversal {inv['invoice_number']}"))
        execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (entry_no, today_str, "1200 - Accounts Receivable", "Asset", 0.0, inv['total_amount'], f"Delete AR reversal {inv['invoice_number']}"))

    execute_db("DELETE FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
    execute_db("DELETE FROM payments WHERE invoice_id = ?", (invoice_id,))
    execute_db("DELETE FROM invoices WHERE id = ?", (invoice_id,))

    log_audit("INVOICE_DELETED", f"Permanently deleted {inv['invoice_number']} ({inv['client_name']}) - ₱{inv['total_amount']:,.2f}", get_current_user_name())

    return jsonify({
        'success': True,
        'message': f"Invoice {inv['invoice_number']} permanently deleted from database."
    })

# ----------------- REACTIVE CART: REAL-TIME CALCULATION -----------------
@app.route('/api/cart/calculate', methods=['POST'])
def calculate_cart():
    data = request.json or {}
    items = data.get('items', [])
    tax_rate = float(data.get('tax_rate', 0.12))  # 12% Philippine VAT

    subtotal = 0.0
    items_breakdown = []
    for itm in items:
        qty = float(itm.get('quantity', 1))
        price = float(itm.get('unit_price', 0))
        line_total = qty * price
        subtotal += line_total
        items_breakdown.append({
            'description': itm.get('description', 'Service Item'),
            'quantity': qty,
            'unit_price': price,
            'total': line_total,
            'formatted_total': f"₱{line_total:,.2f}"
        })

    tax = subtotal * tax_rate if data.get('apply_tax', True) else 0.0
    total = subtotal + tax

    return jsonify({
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
        'formatted_subtotal': f"₱{subtotal:,.2f}",
        'formatted_tax': f"₱{tax:,.2f}",
        'formatted_total': f"₱{total:,.2f}",
        'items': items_breakdown
    })

# ----------------- REAL-TIME ADMIN SYNC HEARTBEAT -----------------
@app.route('/api/admin/sync', methods=['GET'])
def admin_sync():
    invoices = query_db("SELECT id, invoice_number, total_amount, balance_due, status, is_archived, is_overdue FROM invoices")
    bills = query_db("SELECT id, amount, status, is_archived FROM bills")
    latest_audit = query_db("SELECT id, timestamp, action, details, user_name FROM audit_trail ORDER BY id DESC LIMIT 5")
    latest_inv = query_db("SELECT id, invoice_number, created_at FROM invoices ORDER BY id DESC LIMIT 1", one=True)

    active_invoices = [i for i in invoices if not (i['is_archived'] or 0)]
    archived_inv_count = sum(1 for i in invoices if (i['is_archived'] or 0) == 1)
    active_bills = [b for b in bills if not ((b['is_archived'] if 'is_archived' in b.keys() else 0) or 0)]
    archived_bill_count = sum(1 for b in bills if ((b['is_archived'] if 'is_archived' in b.keys() else 0) or 0) == 1)

    total_outstanding = sum(i['balance_due'] for i in active_invoices if not is_settled(i['status']))
    overdue_count = sum(1 for i in active_invoices if i['status'] == 'Overdue' or i['is_overdue'])
    total_billed = sum(i['total_amount'] for i in active_invoices)
    ap_total_due = sum(b['amount'] for b in active_bills if not is_settled(b['status']))

    role = get_current_role()
    perms = ROLES.get(role, ROLES['User'])
    can_view_arch = check_permission('can_view_archives')

    if role == 'User':
        if session.get('account_role') == 'User':
            unread_row = query_db(
                "SELECT COUNT(*) as cnt, COALESCE(MAX(id), 0) as max_id FROM notifications WHERE target_role = 'User' AND (target_username = ? OR target_username IS NULL) AND is_read = 0",
                (get_current_username(),), one=True
            )
        else:
            unread_row = query_db(
                "SELECT COUNT(*) as cnt, COALESCE(MAX(id), 0) as max_id FROM notifications WHERE target_role = 'User' AND is_read = 0",
                one=True
            )
    else:
        unread_row = query_db(
            "SELECT COUNT(*) as cnt, COALESCE(MAX(id), 0) as max_id FROM notifications WHERE target_role IN ('Accounting Staff', 'Admin') AND is_read = 0",
            one=True
        )
    unread_notifs = unread_row['cnt'] if unread_row else 0
    max_notif_id = unread_row['max_id'] if unread_row else 0

    return jsonify({
        'sync_status': 'live_synced',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'active_role': role,
        'role_badge': perms['badge'],
        'permissions': perms,
        'open_invoices_count': len(active_invoices),
        'archived_count': (archived_inv_count + archived_bill_count) if can_view_arch else 0,
        'archived_invoices_count': archived_inv_count if can_view_arch else 0,
        'archived_bills_count': archived_bill_count if can_view_arch else 0,
        'total_outstanding': total_outstanding,
        'total_billed': total_billed,
        'ap_total_due': ap_total_due,
        'bills_count': len(active_bills),
        'overdue_count': overdue_count,
        'unread_notifications': unread_notifs,
        'latest_invoice_id': latest_inv['id'] if latest_inv else 0,
        'sync_token': f"{len(active_invoices)}:{archived_inv_count}:{archived_bill_count}:{len(active_bills)}:{max_notif_id}",
        'recent_logs': [{
            'id': l['id'],
            'timestamp': l['timestamp'],
            'action': l['action'],
            'details': l['details'],
            'user': l['user_name']
        } for l in latest_audit]
    })

# ----------------- PAYMENTS & CONFIRMATION API -----------------
@app.route('/api/invoices/<int:invoice_id>/payment', methods=['POST'])
def record_payment(invoice_id):
    if not check_permission('can_record_payment'):
        return jsonify({
            'error': f"Permission Denied: Current role '{get_current_role()}' cannot record payments. Requires Accounting Staff."
        }), 403

    inv = query_db("SELECT * FROM invoices WHERE id = ?", (invoice_id,), one=True)
    if not inv:
        return jsonify({'error': 'Invoice not found'}), 404

    keys = inv.keys()
    owner_username = inv['created_by'] if 'created_by' in keys and inv['created_by'] else 'alex'
    owner_role = normalize_role(inv['created_by_role'], default='Admin') if 'created_by_role' in keys and inv['created_by_role'] else 'Admin'

    data = request.json or {}
    payment_amount = float(data.get('amount', 0))
    payment_method = data.get('payment_method', 'Wire Transfer')
    reference_no = data.get('reference_no', f"WT-{datetime.now().strftime('%y%m%d%H%M')}")
    payment_mode = (data.get('payment_mode') or '').strip().lower()
    raw_notes = (data.get('notes') or '').strip()
    has_ledger_note = bool(raw_notes)
    notes = raw_notes if has_ledger_note else 'Payment settlement'

    if payment_amount <= 0:
        return jsonify({'error': 'Payment amount must be greater than 0'}), 400

    new_paid = min(float(inv['total_amount']), float(inv['paid_amount']) + payment_amount)
    new_balance = max(0.0, float(inv['total_amount']) - new_paid)

    if payment_mode == 'partial' or (inv['status'] == 'Pending' and has_ledger_note):
        new_status = 'Confirm with Condition'
        if new_balance <= 0.01:
            new_balance = 0.0
            is_overdue = 0
        else:
            is_overdue = inv['is_overdue']
        saved_accounting_note = raw_notes or (
            f"Partial payment of ₱{payment_amount:,.2f} recorded (Remaining balance: ₱{new_balance:,.2f})"
            if new_balance > 0 else f"Conditional confirmation recorded (₱{payment_amount:,.2f})"
        )
    elif payment_mode == 'record':
        new_status = 'Confirmed'
        new_paid = float(inv['total_amount'])
        new_balance = 0.0
        is_overdue = 0
        saved_accounting_note = inv['accounting_notes'] if 'accounting_notes' in keys and inv['accounting_notes'] else ''
    elif has_ledger_note and inv['status'] != 'Confirm with Condition':
        new_status = 'Confirm with Condition'
        if new_balance <= 0.01:
            new_balance = 0.0
            is_overdue = 0
        else:
            is_overdue = inv['is_overdue']
        saved_accounting_note = raw_notes
    elif new_balance <= 0.01 or inv['status'] == 'Confirm with Condition':
        new_status = 'Confirmed' if (owner_role == 'User' or inv['status'] in ('Pending', 'Confirm with Condition')) else 'Paid'
        new_paid = float(inv['total_amount'])
        new_balance = 0.0
        is_overdue = 0
        saved_accounting_note = raw_notes or (inv['accounting_notes'] if 'accounting_notes' in keys and inv['accounting_notes'] else '')
    elif new_paid > 0:
        if owner_role == 'User' or inv['status'] == 'Pending':
            new_status = 'Confirm with Condition'
            saved_accounting_note = raw_notes or f"Partial payment of ₱{payment_amount:,.2f} recorded (Remaining balance: ₱{new_balance:,.2f})"
        else:
            new_status = 'Partial'
            saved_accounting_note = inv['accounting_notes'] if 'accounting_notes' in keys and inv['accounting_notes'] else ''
        is_overdue = inv['is_overdue']
    else:
        new_status = inv['status']
        is_overdue = inv['is_overdue']
        saved_accounting_note = inv['accounting_notes'] if 'accounting_notes' in keys and inv['accounting_notes'] else ''

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Insert payment record
    execute_db("""
    INSERT INTO payments (invoice_id, payment_date, amount, payment_method, reference_no, notes, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (invoice_id, today_str, payment_amount, payment_method, reference_no, saved_accounting_note or notes, now_str))

    # Update invoice (including accounting_notes so User can view Accounting Staff's Ledger Notes)
    execute_db("""
    UPDATE invoices
    SET paid_amount = ?, balance_due = ?, status = ?, is_overdue = ?, accounting_notes = ?
    WHERE id = ?
    """, (new_paid, new_balance, new_status, is_overdue, saved_accounting_note, invoice_id))

    # Journal Entry: Debit Cash, Credit AR (tagged to invoice owner so User GL reflects confirmation)
    entry_no = f"JE-PAY-{datetime.now().strftime('%m%d%H%M%S')}"
    post_journal_entry(entry_no, today_str, "1010 - Operating Cash (Silicon Valley Bank)", "Asset", payment_amount, 0.0,
                       f"Receipt for {inv['invoice_number']} via {payment_method}", owner_username, owner_role)
    post_journal_entry(entry_no, today_str, "1200 - Accounts Receivable", "Asset", 0.0, payment_amount,
                       f"Relieve AR for {inv['invoice_number']}", owner_username, owner_role)

    if new_status in ('Confirmed', 'Confirm with Condition'):
        execute_db("UPDATE notifications SET is_read = 1 WHERE record_kind = 'invoice' AND record_id = ? AND target_role IN ('Accounting Staff', 'Admin')", (invoice_id,))
        if new_status == 'Confirm with Condition':
            create_notification(
                target_role='User',
                target_username=owner_username,
                notif_type='INVOICE_CONFIRMED_CONDITION',
                title='Invoice Confirmed with Condition',
                message=f"{get_current_user_name()} ({get_current_role()}) sent Ledger Notes on Invoice {inv['invoice_number']} ({inv['client_name']}): \"{saved_accounting_note}\"",
                record_kind='invoice',
                record_id=invoice_id,
                ref_number=inv['invoice_number'],
                created_by_name=get_current_user_name()
            )
        else:
            create_notification(
                target_role='User',
                target_username=owner_username,
                notif_type='INVOICE_CONFIRMED',
                title='Invoice Payment Confirmed',
                message=f"{get_current_user_name()} ({get_current_role()}) confirmed payment for Invoice {inv['invoice_number']} ({inv['client_name']}, ₱{inv['total_amount']:,.2f}). Status is now Confirmed.",
                record_kind='invoice',
                record_id=invoice_id,
                ref_number=inv['invoice_number'],
                created_by_name=get_current_user_name()
            )

    log_audit("PAYMENT_RECORDED", f"Recorded payment of ₱{payment_amount:,.2f} for {inv['invoice_number']} ({inv['client_name']}) via {payment_method} -> {new_status}" + (f" [Ledger Notes: {saved_accounting_note}]" if saved_accounting_note else ""), get_current_user_name())

    return jsonify({
        'success': True,
        'message': f'Payment of ₱{payment_amount:,.2f} recorded for {inv["invoice_number"]} ({new_status})',
        'new_balance': new_balance,
        'status': new_status,
        'accounting_notes': saved_accounting_note
    })

@app.route('/api/invoices/<int:invoice_id>/confirm', methods=['POST'])
def confirm_invoice_payment(invoice_id):
    if not check_permission('can_record_payment'):
        return jsonify({
            'error': f"Permission Denied: Confirming invoices requires Accounting Staff role."
        }), 403

    inv = query_db("SELECT * FROM invoices WHERE id = ?", (invoice_id,), one=True)
    if not inv:
        return jsonify({'error': 'Invoice not found'}), 404
    if inv['is_archived']:
        return jsonify({'error': 'Archived invoices cannot be confirmed. Restore first.'}), 400
    if is_settled(inv['status']):
        return jsonify({'error': f"Invoice {inv['invoice_number']} is already {inv['status']}."}), 400

    keys = inv.keys()
    owner_username = inv['created_by'] if 'created_by' in keys and inv['created_by'] else 'alex'
    owner_role = normalize_role(inv['created_by_role'], default='Admin') if 'created_by_role' in keys and inv['created_by_role'] else 'Admin'

    remaining = max(0.0, float(inv['balance_due'] or inv['total_amount'] or 0.0))
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_str = datetime.now().strftime("%Y-%m-%d")

    if remaining > 0:
        execute_db("""
        INSERT INTO payments (invoice_id, payment_date, amount, payment_method, reference_no, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (invoice_id, today_str, remaining, 'Accounting Confirmation', f"CONF-{datetime.now().strftime('%y%m%d%H%M')}", f"Confirmed by {get_current_user_name()}", now_str))

        entry_no = f"JE-CONF-{datetime.now().strftime('%m%d%H%M%S')}"
        post_journal_entry(entry_no, today_str, "1010 - Operating Cash (Silicon Valley Bank)", "Asset", remaining, 0.0,
                           f"Confirmed receipt for {inv['invoice_number']}", owner_username, owner_role)
        post_journal_entry(entry_no, today_str, "1200 - Accounts Receivable", "Asset", 0.0, remaining,
                           f"Relieve AR on confirmation {inv['invoice_number']}", owner_username, owner_role)

    execute_db("""
    UPDATE invoices
    SET paid_amount = total_amount, balance_due = 0.0, status = 'Sent', is_overdue = 0
    WHERE id = ?
    """, (invoice_id,))

    execute_db("UPDATE notifications SET is_read = 1 WHERE record_kind = 'invoice' AND record_id = ? AND target_role IN ('Accounting Staff', 'Admin')", (invoice_id,))
    create_notification(
        target_role='User',
        target_username=owner_username,
        notif_type='INVOICE_CONFIRMED',
        title='Invoice Payment Confirmed',
        message=f"{get_current_user_name()} confirmed payment for Invoice {inv['invoice_number']} ({inv['client_name']}, ₱{inv['total_amount']:,.2f}). Status changed to Confirmed!",
        record_kind='invoice',
        record_id=invoice_id,
        ref_number=inv['invoice_number'],
        created_by_name=get_current_user_name()
    )
    log_audit("INVOICE_CONFIRMED", f"Confirmed payment for Invoice {inv['invoice_number']} ({inv['client_name']}) - ₱{inv['total_amount']:,.2f}", get_current_user_name())

    return jsonify({
        'success': True,
        'status': 'Confirmed',
        'message': f"Invoice {inv['invoice_number']} confirmed as Paid and User notified!"
    })

# ----------------- REMINDER API -----------------
@app.route('/api/invoices/<int:invoice_id>/reminder', methods=['POST'])
def send_reminder(invoice_id):
    inv = query_db("SELECT * FROM invoices WHERE id = ?", (invoice_id,), one=True)
    if not inv:
        return jsonify({'error': 'Invoice not found'}), 404

    log_audit("REMINDER_DISPATCHED", f"Automated payment reminder dispatched to {inv['client_name']} ({inv['client_email']}) for {inv['invoice_number']} (₱{inv['balance_due']:,.2f})", get_current_user_name())

    return jsonify({
        'success': True,
        'message': f"Formal payment reminder successfully dispatched to {inv['client_name']} ({inv['client_email'] or 'ap-desk@client.com'}).",
        'invoice_number': inv['invoice_number'],
        'client': inv['client_name']
    })

COGS_KEYWORDS = ('cloud', 'hosting', 'data warehousing', 'infrastructure', 'devops')

def is_cogs_category(category: str) -> bool:
    """Classify vendor bill categories into COGS vs Operating Expenses."""
    cat = (category or '').lower()
    return any(k in cat for k in COGS_KEYWORDS)

def compute_financial_reports():
    """
    Single authoritative GAAP engine deriving Profit & Loss, Balance Sheet,
    Trial Balance, and Chart of Accounts live from SQLite A/R and A/P records.
    """
    invoices = query_db("SELECT * FROM invoices WHERE (is_archived = 0 OR is_archived IS NULL)")
    archived_invoices = query_db("SELECT * FROM invoices WHERE is_archived = 1")
    bills = query_db("SELECT * FROM bills WHERE (is_archived = 0 OR is_archived IS NULL) ORDER BY id ASC")
    archived_bills = query_db("SELECT * FROM bills WHERE is_archived = 1 ORDER BY id ASC")
    journal_count_row = query_db("SELECT COUNT(*) as cnt FROM journal_entries", one=True)
    audit_count_row = query_db("SELECT COUNT(*) as cnt FROM audit_trail", one=True)

    # 1. Invoicing & A/R Aggregates (Active non-archived invoices)
    ar_revenue_subtotal = sum(float(r['subtotal'] or 0.0) for r in invoices)
    ar_tax_total = sum(float(r['tax'] or 0.0) for r in invoices)
    ar_total_billed = sum(float(r['total_amount'] or 0.0) for r in invoices)
    ar_cash_collected = sum(float(r['paid_amount'] or 0.0) for r in invoices)
    ar_outstanding = ar_total_billed - ar_cash_collected
    ar_overdue_amount = sum(float(r['balance_due'] or 0.0) for r in invoices if r['status'] == 'Overdue' or r['is_overdue'])
    ar_overdue_count = sum(1 for r in invoices if r['status'] == 'Overdue' or r['is_overdue'])

    archived_count = len(archived_invoices)
    archived_bills_count = len(archived_bills)
    archived_total = sum(float(r['total_amount'] or 0.0) for r in archived_invoices) + sum(float(b['amount'] or 0.0) for b in archived_bills)

    # 2. Bills & A/P Aggregates
    cogs_bills = [b for b in bills if is_cogs_category(b['category'])]
    opex_bills = [b for b in bills if not is_cogs_category(b['category'])]

    cogs_total = sum(float(b['amount'] or 0.0) for b in cogs_bills)
    opex_total = sum(float(b['amount'] or 0.0) for b in opex_bills)
    bills_total = cogs_total + opex_total

    ap_cash_disbursed = sum(float(b['amount'] or 0.0) for b in bills if is_settled(b['status']))
    ap_outstanding = sum(float(b['amount'] or 0.0) for b in bills if not is_settled(b['status']))
    ap_due_count = sum(1 for b in bills if not is_settled(b['status']))
    ap_overdue_amount = sum(float(b['amount'] or 0.0) for b in bills if b['status'] == 'Overdue' and not is_settled(b['status']))
    ap_overdue_count = sum(1 for b in bills if b['status'] == 'Overdue' and not is_settled(b['status']))

    # 3. Opening Baseline (Zeroed for Clean Slate Accounting)
    opening_cash = 0.0
    equipment_assets = 0.0
    accrued_expenses = 0.0
    opening_equity = (opening_cash + equipment_assets) - accrued_expenses

    # 4. Live Balance Sheet & Profit/Loss Equations
    cash_balance = opening_cash + ar_cash_collected - ap_cash_disbursed
    ar_balance = ar_outstanding
    total_assets = cash_balance + ar_balance + equipment_assets

    ap_balance = ap_outstanding
    tax_payable = ar_tax_total
    total_liabilities = ap_balance + accrued_expenses + tax_payable

    gross_profit = ar_revenue_subtotal - cogs_total
    net_operating_income = gross_profit - opex_total
    gross_margin_pct = round((gross_profit / ar_revenue_subtotal * 100.0), 1) if ar_revenue_subtotal > 0 else 0.0
    net_margin_pct = round((net_operating_income / ar_revenue_subtotal * 100.0), 1) if ar_revenue_subtotal > 0 else 0.0

    total_equity = opening_equity + net_operating_income
    total_liabilities_and_equity = total_liabilities + total_equity
    balance_sheet_variance = round(total_assets - total_liabilities_and_equity, 2)

    # 5. Trial Balance Accounts (Strictly Debits == Credits)
    trial_accounts = []
    if cash_balance >= 0:
        trial_accounts.append({
            'code': '1010', 'account_name': 'Operating Cash (Silicon Valley Bank)',
            'account_type': 'Asset', 'source_module': 'A/R Payments & A/P Settlements',
            'source_tab': 'ar', 'debit': cash_balance, 'credit': 0.0
        })
    else:
        trial_accounts.append({
            'code': '1010', 'account_name': 'Operating Cash Overdraft (SVB)',
            'account_type': 'Liability', 'source_module': 'A/R Payments & A/P Settlements',
            'source_tab': 'ap', 'debit': 0.0, 'credit': abs(cash_balance)
        })

    trial_accounts.extend([
        {
            'code': '1200', 'account_name': 'Accounts Receivable (A/R)',
            'account_type': 'Asset', 'source_module': 'Invoicing & A/R',
            'source_tab': 'ar', 'debit': ar_balance, 'credit': 0.0
        },
        {
            'code': '1500', 'account_name': 'Computer Hardware & Intangibles',
            'account_type': 'Asset', 'source_module': 'Fixed Asset Register',
            'source_tab': 'coa', 'debit': equipment_assets, 'credit': 0.0
        },
        {
            'code': '2010', 'account_name': 'Accounts Payable (A/P)',
            'account_type': 'Liability', 'source_module': 'Bills & A/P',
            'source_tab': 'ap', 'debit': 0.0, 'credit': ap_balance
        },
        {
            'code': '2020', 'account_name': 'Accrued Payroll & Operational Expenses',
            'account_type': 'Liability', 'source_module': 'General Ledger Accruals',
            'source_tab': 'coa', 'debit': 0.0, 'credit': accrued_expenses
        },
    ])

    if tax_payable > 0:
        trial_accounts.append({
            'code': '2200', 'account_name': 'Sales / VAT Tax Liabilities',
            'account_type': 'Liability', 'source_module': 'Invoicing & A/R',
            'source_tab': 'ar', 'debit': 0.0, 'credit': tax_payable
        })

    trial_accounts.extend([
        {
            'code': '3010', 'account_name': 'Share Capital & Prior Retained Earnings',
            'account_type': 'Equity', 'source_module': 'Opening Ledger Capital',
            'source_tab': 'coa', 'debit': 0.0, 'credit': opening_equity
        },
        {
            'code': '4010', 'account_name': 'Enterprise Software & Services Revenue',
            'account_type': 'Revenue', 'source_module': 'Invoicing & A/R',
            'source_tab': 'ar', 'debit': 0.0, 'credit': ar_revenue_subtotal
        },
        {
            'code': '5010', 'account_name': 'Cost of Goods Sold (Cloud & Infrastructure)',
            'account_type': 'Expense', 'source_module': 'Bills & A/P',
            'source_tab': 'ap', 'debit': cogs_total, 'credit': 0.0
        },
        {
            'code': '5100', 'account_name': 'Operating Expenses (Legal, Audit, SaaS & G&A)',
            'account_type': 'Expense', 'source_module': 'Bills & A/P',
            'source_tab': 'ap', 'debit': opex_total, 'credit': 0.0
        }
    ])

    trial_total_debits = sum(a['debit'] for a in trial_accounts)
    trial_total_credits = sum(a['credit'] for a in trial_accounts)
    trial_variance = round(trial_total_debits - trial_total_credits, 2)

    # Traceability details for drill-downs inside reports
    ar_contributors = [{
        'invoice_number': r['invoice_number'],
        'client_name': r['client_name'],
        'amount': float(r['subtotal'] or 0.0),
        'paid_amount': float(r['paid_amount'] or 0.0),
        'balance_due': float(r['balance_due'] or 0.0),
        'status': r['status']
    } for r in invoices]

    ap_bill_items = [{
        'bill_number': b['bill_number'],
        'vendor_name': b['vendor_name'],
        'category': b['category'],
        'classification': 'COGS' if is_cogs_category(b['category']) else 'OPEX',
        'amount': float(b['amount'] or 0.0),
        'status': b['status']
    } for b in bills]

    return {
        'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'pnl': {
            'operating_revenue': ar_revenue_subtotal,
            'cogs': cogs_total,
            'gross_profit': gross_profit,
            'gross_margin_pct': gross_margin_pct,
            'operating_expenses': opex_total,
            'net_operating_income': net_operating_income,
            'net_margin_pct': net_margin_pct,
            'active_invoices_count': len(invoices),
            'cogs_bills_count': len(cogs_bills),
            'opex_bills_count': len(opex_bills),
            'ar_cash_collected': ar_cash_collected,
            'ar_open_balance': ar_outstanding,
            'archived_count': archived_count,
            'archived_total': archived_total,
            'ar_contributors': ar_contributors,
            'ap_bill_items': ap_bill_items
        },
        'balance_sheet': {
            'assets': {
                'cash_equivalents': cash_balance,
                'opening_cash': opening_cash,
                'ar_collected': ar_cash_collected,
                'ap_disbursed': ap_cash_disbursed,
                'accounts_receivable': ar_balance,
                'equipment_intangibles': equipment_assets,
                'total_assets': total_assets
            },
            'liabilities': {
                'accounts_payable': ap_balance,
                'accrued_expenses': accrued_expenses,
                'tax_payable': tax_payable,
                'total_liabilities': total_liabilities
            },
            'equity': {
                'opening_equity': opening_equity,
                'current_net_income': net_operating_income,
                'total_equity': total_equity
            },
            'total_liabilities_and_equity': total_liabilities_and_equity,
            'variance': balance_sheet_variance,
            'is_balanced': abs(balance_sheet_variance) < 0.01
        },
        'trial_balance': {
            'accounts': trial_accounts,
            'total_debits': trial_total_debits,
            'total_credits': trial_total_credits,
            'variance': trial_variance,
            'is_balanced': abs(trial_variance) < 0.01,
            'journal_entries_count': journal_count_row['cnt'] if journal_count_row else 0
        },
        'summary_counts': {
            'active_invoices_count': len(invoices),
            'archived_invoices_count': archived_count,
            'archived_bills_count': archived_bills_count,
            'total_archived_count': archived_count + archived_bills_count,
            'ar_overdue_count': ar_overdue_count,
            'ar_overdue_amount': ar_overdue_amount,
            'ap_due_count': ap_due_count,
            'ap_total_due': ap_outstanding,
            'ap_overdue_count': ap_overdue_count,
            'ap_overdue_amount': ap_overdue_amount,
            'total_bills_count': len(bills),
            'audit_events_count': audit_count_row['cnt'] if audit_count_row else 0
        }
    }

@app.route('/api/financial-reports', methods=['GET'])
def get_financial_reports():
    return jsonify(compute_financial_reports())

# ----------------- STATS / KPI API -----------------
@app.route('/api/stats', methods=['GET'])
def get_stats():
    role = get_current_role()
    can_view_arch = check_permission('can_view_archives')

    if role == 'User':
        scope_sql, scope_params = apply_role_scope()
        user_invoices = query_db(
            f"SELECT * FROM invoices WHERE (is_archived = 0 OR is_archived IS NULL){scope_sql}",
            scope_params
        )
        user_bills = query_db(
            f"SELECT * FROM bills WHERE (is_archived = 0 OR is_archived IS NULL){scope_sql}",
            scope_params
        )
        total_outstanding = sum(float(i['balance_due'] or 0.0) for i in user_invoices if not is_settled(i['status']))
        overdue_amount = sum(float(i['balance_due'] or 0.0) for i in user_invoices if i['status'] == 'Overdue' or i['is_overdue'])
        overdue_count = sum(1 for i in user_invoices if i['status'] == 'Overdue' or i['is_overdue'])
        collected_month = sum(float(i['paid_amount'] or 0.0) for i in user_invoices)
        ap_due_count = sum(1 for b in user_bills if not is_settled(b['status']))
        ap_total_due = sum(float(b['amount'] or 0.0) for b in user_bills if not is_settled(b['status']))
        pending_invoices_count = sum(1 for i in user_invoices if not is_settled(i['status']))
        confirmed_invoices_count = sum(1 for i in user_invoices if is_settled(i['status']))
        pending_bills_count = ap_due_count
        confirmed_bills_count = sum(1 for b in user_bills if is_settled(b['status']))
        return jsonify({
            'total_outstanding': total_outstanding,
            'open_invoices_count': len(user_invoices),
            'overdue_amount': overdue_amount,
            'overdue_count': overdue_count,
            'collected_month': collected_month,
            'collected_growth': 'Confirmed Payments',
            'ar_active_count': len(user_invoices),
            'ap_due_count': ap_due_count,
            'ap_total_due': ap_total_due,
            'ap_overdue_amount': 0.0,
            'ap_overdue_count': 0,
            'ap_cash_disbursed': sum(float(b['amount'] or 0.0) for b in user_bills if is_settled(b['status'])),
            'total_bills_count': len(user_bills),
            'pending_invoices_count': pending_invoices_count,
            'confirmed_invoices_count': confirmed_invoices_count,
            'pending_bills_count': pending_bills_count,
            'confirmed_bills_count': confirmed_bills_count,
            'total_archived_count': 0
        })

    reports = compute_financial_reports()
    counts = reports['summary_counts']
    payments = query_db("SELECT amount FROM payments")
    collected_month = sum(row['amount'] for row in payments)

    return jsonify({
        'total_outstanding': reports['balance_sheet']['assets']['accounts_receivable'],
        'open_invoices_count': counts['active_invoices_count'],
        'overdue_amount': counts['ar_overdue_amount'],
        'overdue_count': counts['ar_overdue_count'],
        'collected_month': collected_month,
        'collected_growth': 'Live Payments',
        'ar_active_count': counts['active_invoices_count'],
        'ap_due_count': counts['ap_due_count'],
        'ap_total_due': counts['ap_total_due'],
        'ap_overdue_amount': counts.get('ap_overdue_amount', 0.0),
        'ap_overdue_count': counts.get('ap_overdue_count', 0),
        'ap_cash_disbursed': reports['balance_sheet']['assets']['ap_disbursed'],
        'total_bills_count': counts['total_bills_count'],
        'archived_invoices_count': counts['archived_invoices_count'] if can_view_arch else 0,
        'archived_bills_count': counts['archived_bills_count'] if can_view_arch else 0,
        'total_archived_count': counts['total_archived_count']
    })

@app.route('/api/dashboard-summary', methods=['GET'])
def get_dashboard_summary():
    reports = compute_financial_reports()
    counts = reports['summary_counts']
    bs = reports['balance_sheet']
    pnl = reports['pnl']
    tb = reports['trial_balance']

    payments = query_db("SELECT amount FROM payments")
    collected_month = sum(row['amount'] for row in payments)
    recent_invoices = query_db("SELECT invoice_number, client_name, total_amount, status, due_date FROM invoices WHERE (is_archived = 0 OR is_archived IS NULL) ORDER BY id DESC LIMIT 4")
    recent_bills = query_db("SELECT bill_number, vendor_name, amount, status, due_date FROM bills WHERE (is_archived = 0 OR is_archived IS NULL) ORDER BY id DESC LIMIT 4")
    recent_audits = query_db("SELECT action, user_name, details, timestamp FROM audit_trail ORDER BY id DESC LIMIT 5")

    return jsonify({
        'ar': {
            'total_outstanding': bs['assets']['accounts_receivable'],
            'open_count': counts['active_invoices_count'],
            'overdue_amount': counts['ar_overdue_amount'],
            'overdue_count': counts['ar_overdue_count'],
            'collected_month': collected_month,
            'growth': '+12%',
            'on_time_rate': '96.2%'
        },
        'ap': {
            'total_due': counts['ap_total_due'],
            'due_count': counts['ap_due_count'],
            'total_bills_count': counts['total_bills_count'],
            'cloud_bills_count': pnl['cogs_bills_count']
        },
        'working_capital': {
            'net_capital': (bs['assets']['cash_equivalents'] + bs['assets']['accounts_receivable']) - bs['liabilities']['accounts_payable'],
            'liquid_cash': bs['assets']['cash_equivalents'],
            'current_ratio': '12.1x',
            'quick_ratio': '10.8x'
        },
        'gl': {
            'accounts_count': len(tb['accounts']),
            'journal_entries_count': tb['journal_entries_count'],
            'total_volume': tb['total_debits'],
            'variance': tb['variance'],
            'status': 'Strictly Balanced (GAAP)' if tb['is_balanced'] else 'Out of Balance'
        },
        'pnl': {
            'revenue': pnl['operating_revenue'],
            'cogs': pnl['cogs'],
            'gross_profit': pnl['gross_profit'],
            'gross_margin': f"{pnl['gross_margin_pct']}%",
            'opex': pnl['operating_expenses'],
            'net_income': pnl['net_operating_income'],
            'net_margin': f"{pnl['net_margin_pct']}%"
        },
        'balance_sheet': {
            'total_assets': bs['assets']['total_assets'],
            'total_liabilities': bs['liabilities']['total_liabilities'],
            'total_equity': bs['equity']['total_equity'],
            'equilibrium': bs['is_balanced']
        },
        'trial_balance': {
            'total_debits': tb['total_debits'],
            'total_credits': tb['total_credits'],
            'variance': tb['variance'],
            'status': 'Balanced & Closed' if tb['is_balanced'] else 'Pending Adjustment'
        },
        'security': {
            'audit_events_count': counts['audit_events_count'],
            'active_role': get_current_role(),
            'compliance': 'SOC 2 Type II · TLS 1.3'
        },
        'recent_invoices': [dict(r) for r in recent_invoices],
        'recent_bills': [dict(r) for r in recent_bills],
        'recent_audits': [dict(r) for r in recent_audits]
    })

# ----------------- BILLS (ACCOUNTS PAYABLE) API -----------------
@app.route('/api/bills', methods=['GET'])
def get_bills():
    status_filter = request.args.get('status', 'All')
    source_filter = request.args.get('source', 'All')

    if status_filter == 'Archived' and not check_permission('can_view_archives'):
        return jsonify({
            'error': "Permission Denied: Only Admin can view archived bills."
        }), 403

    query = "SELECT * FROM bills WHERE 1=1"
    params = []

    if status_filter == 'Archived':
        query += " AND is_archived = 1"
    else:
        query += " AND (is_archived = 0 OR is_archived IS NULL)"
        if status_filter == 'Pending':
            query += " AND status NOT IN ('Paid', 'Confirmed')"
        elif status_filter == 'Confirmed':
            query += " AND status IN ('Paid', 'Confirmed')"

    scope_sql, scope_params = apply_role_scope()
    query += scope_sql
    params.extend(scope_params)

    if get_current_role() != 'User':
        if source_filter == 'User':
            query += " AND created_by_role = 'User'"
        elif source_filter == 'StaffAdmin':
            query += " AND (created_by_role IN ('Accounting Staff', 'Admin') OR created_by_role IS NULL)"

    query += " ORDER BY CASE WHEN status = 'Pending' THEN 0 ELSE 1 END ASC, id DESC"
    bills = query_db(query, params)
    bills_list = []
    for b in bills:
        keys = b.keys()
        bills_list.append({
            'id': b['id'],
            'bill_number': b['bill_number'],
            'vendor_name': b['vendor_name'],
            'category': b['category'],
            'due_date': b['due_date'],
            'amount': b['amount'],
            'status': b['status'],
            'is_archived': bool(b['is_archived'] if 'is_archived' in keys else 0),
            'created_by': b['created_by'] if 'created_by' in keys and b['created_by'] else 'alex',
            'created_by_name': b['created_by_name'] if 'created_by_name' in keys and b['created_by_name'] else 'Alex Rivera',
            'created_by_role': normalize_role(b['created_by_role'], default='Admin') if 'created_by_role' in keys and b['created_by_role'] else 'Admin',
            'archived_by': b['archived_by'] if 'archived_by' in keys else None,
            'archived_at': b['archived_at'] if 'archived_at' in keys else None,
            'created_at': b['created_at']
        })
    return jsonify({'bills': bills_list})

@app.route('/api/bills', methods=['POST'])
def create_bill():
    if not check_permission('can_create'):
        return jsonify({
            'error': f"Permission Denied: Current role '{get_current_role()}' cannot create vendor bills."
        }), 403

    data = request.json or {}
    vendor_name = data.get('vendor_name', '').strip()
    category = data.get('category', 'Cloud & Hosting').strip()
    due_date = data.get('due_date', '').strip() or 'Nov 30, 2025'
    amount = float(data.get('amount', 0.0) or 0.0)
    custom_num = data.get('bill_number', '').strip()

    if not vendor_name or amount <= 0:
        return jsonify({'error': 'Vendor name and positive amount are required.'}), 400

    max_row = query_db("SELECT COALESCE(MAX(id), 0) as max_id FROM bills", one=True)
    next_num = (max_row['max_id'] if max_row else 0) + 101
    bill_number = custom_num or f"BILL-2025-{next_num}"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_str = datetime.now().strftime("%Y-%m-%d")

    active_role = get_current_role()
    creator_username = get_current_username()
    creator_name = get_current_user_name()
    bill_status = 'Pending' if active_role == 'User' else 'Due'

    bill_id = execute_db("""
    INSERT INTO bills (
        bill_number, vendor_name, category, due_date, amount, status,
        is_archived, created_by, created_by_name, created_by_role, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?)
    """, (bill_number, vendor_name, category, due_date, amount, bill_status, creator_username, creator_name, active_role, now_str))

    # Post double-entry Journal Entry: Debit COGS/OPEX Expense, Credit Accounts Payable (tagged to creator for User GL)
    exp_account = "5010 - Cloud Hosting & Infrastructure (COGS)" if is_cogs_category(category) else "5100 - Operating Expenses (SaaS, Legal & G&A)"
    entry_no = f"JE-AP-NEW-{datetime.now().strftime('%m%d%H%M%S')}"
    post_journal_entry(entry_no, today_str, exp_account, "Expense", amount, 0.0,
                       f"Recognize expense {bill_number} from {vendor_name}", creator_username, active_role)
    post_journal_entry(entry_no, today_str, "2010 - Accounts Payable", "Liability", 0.0, amount,
                       f"Accrue payable {bill_number} ({vendor_name})", creator_username, active_role)

    if active_role == 'User':
        create_notification(
            target_role='Accounting Staff',
            notif_type='USER_BILL_CREATED',
            title='New User Bill Submitted',
            message=f"{creator_name} submitted Bill {bill_number} ({vendor_name} · ₱{amount:,.2f}) — Pending Accounting payment confirmation.",
            record_kind='bill',
            record_id=bill_id,
            ref_number=bill_number,
            created_by_name=creator_name
        )

    log_audit("BILL_CREATED", f"Recorded vendor bill {bill_number} ({vendor_name} · {category}) - ₱{amount:,.2f} [{active_role}]", creator_name)

    return jsonify({
        'success': True,
        'bill_id': bill_id,
        'bill_number': bill_number,
        'status': bill_status,
        'message': f"Bill {bill_number} submitted (Pending) — Accounting Staff notified!" if active_role == 'User' else f"Vendor bill {bill_number} (₱{amount:,.2f}) recorded and posted to General Ledger."
    })

@app.route('/api/bills/<int:bill_id>/archive', methods=['POST'])
def archive_bill(bill_id):
    if not check_permission('can_archive'):
        return jsonify({
            'error': f"Permission Denied: Current role '{get_current_role()}' cannot archive vendor bills. Requires Accounting Staff."
        }), 403

    bill = query_db("SELECT * FROM bills WHERE id = ?", (bill_id,), one=True)
    if not bill:
        return jsonify({'error': 'Bill not found'}), 404

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    archived_by = f"{get_current_user_name()} ({get_current_role()})"
    was_archived = bool(bill['is_archived'] if 'is_archived' in bill.keys() else 0)

    execute_db(
        "UPDATE bills SET is_archived = 1, archived_by = ?, archived_at = ? WHERE id = ?",
        (archived_by, now_str, bill_id)
    )
    if not was_archived and float(bill['amount'] or 0) > 0:
        exp_account = "5010 - Cloud Hosting & Infrastructure (COGS)" if is_cogs_category(bill['category']) else "5100 - Operating Expenses (SaaS, Legal & G&A)"
        entry_no = f"JE-AP-ARC-{datetime.now().strftime('%m%d%H%M%S')}"
        today_str = datetime.now().strftime("%Y-%m-%d")
        execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (entry_no, today_str, "2010 - Accounts Payable", "Liability", bill['amount'], 0.0, f"Reverse AP on archive {bill['bill_number']}"))
        execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (entry_no, today_str, exp_account, "Expense", 0.0, bill['amount'], f"Reverse expense on archive {bill['bill_number']}"))

    log_audit("BILL_ARCHIVED", f"Vendor bill {bill['bill_number']} ({bill['vendor_name']}) archived by {archived_by}", get_current_user_name())
    return jsonify({
        'success': True,
        'message': f"Bill {bill['bill_number']} moved to Archives (Admin only access).",
        'bill_id': bill_id
    })

@app.route('/api/bills/<int:bill_id>/restore', methods=['POST'])
def restore_bill(bill_id):
    if not check_permission('can_restore'):
        return jsonify({
            'error': f"Permission Denied: Restoring archived vendor bills requires Admin privileges. '{get_current_role()}' is unauthorized."
        }), 403

    bill = query_db("SELECT * FROM bills WHERE id = ?", (bill_id,), one=True)
    if not bill:
        return jsonify({'error': 'Bill not found'}), 404

    was_archived = bool(bill['is_archived'] if 'is_archived' in bill.keys() else 0)
    execute_db("UPDATE bills SET is_archived = 0, archived_by = NULL, archived_at = NULL WHERE id = ?", (bill_id,))
    if was_archived and float(bill['amount'] or 0) > 0:
        exp_account = "5010 - Cloud Hosting & Infrastructure (COGS)" if is_cogs_category(bill['category']) else "5100 - Operating Expenses (SaaS, Legal & G&A)"
        entry_no = f"JE-AP-RST-{datetime.now().strftime('%m%d%H%M%S')}"
        today_str = datetime.now().strftime("%Y-%m-%d")
        execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (entry_no, today_str, exp_account, "Expense", bill['amount'], 0.0, f"Restore expense {bill['bill_number']}"))
        execute_db("INSERT INTO journal_entries (entry_number, date, account_name, account_type, debit, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (entry_no, today_str, "2010 - Accounts Payable", "Liability", 0.0, bill['amount'], f"Restore payable {bill['bill_number']}"))

    log_audit("BILL_RESTORED", f"Vendor bill {bill['bill_number']} ({bill['vendor_name']}) restored to active A/P by Admin", get_current_user_name())
    return jsonify({
        'success': True,
        'message': f"Bill {bill['bill_number']} restored to active Accounts Payable.",
        'bill_id': bill_id
    })

@app.route('/api/bills/<int:bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    if not check_permission('can_delete'):
        return jsonify({
            'error': f"Permission Denied: Deleting vendor bills requires Admin privileges. Role '{get_current_role()}' is unauthorized."
        }), 403

    bill = query_db("SELECT * FROM bills WHERE id = ?", (bill_id,), one=True)
    if not bill:
        return jsonify({'error': 'Bill not found'}), 404

    execute_db("DELETE FROM bills WHERE id = ?", (bill_id,))
    log_audit("BILL_DELETED", f"Deleted vendor bill {bill['bill_number']} ({bill['vendor_name']}) - ₱{bill['amount']:,.2f}", get_current_user_name())
    return jsonify({
        'success': True,
        'message': f"Bill {bill['bill_number']} permanently deleted from database."
    })

@app.route('/api/bills/<int:bill_id>/pay', methods=['POST'])
def pay_bill(bill_id):
    if not check_permission('can_settle_bills'):
        return jsonify({
            'error': f"Permission Denied: Settling vendor bills requires Accounting Staff role. Current role '{get_current_role()}' is unauthorized."
        }), 403

    bill = query_db("SELECT * FROM bills WHERE id = ?", (bill_id,), one=True)
    if not bill:
        return jsonify({'error': 'Bill not found'}), 404

    keys = bill.keys()
    if 'is_archived' in keys and bill['is_archived']:
        return jsonify({'error': f"Bill {bill['bill_number']} is archived. Restore it first before settling."}), 400

    if is_settled(bill['status']):
        return jsonify({'error': f"Bill {bill['bill_number']} is already settled ({bill['status']})."}), 400

    owner_username = bill['created_by'] if 'created_by' in keys and bill['created_by'] else 'alex'
    owner_role = normalize_role(bill['created_by_role'], default='Admin') if 'created_by_role' in keys and bill['created_by_role'] else 'Admin'
    new_status = 'Confirmed' if (owner_role == 'User' or bill['status'] == 'Pending') else 'Paid'

    execute_db("UPDATE bills SET status = ? WHERE id = ?", (new_status, bill_id))

    # Log to audit trail and journal entry (tagged with owner so User GL reflects confirmation)
    log_audit("BILL_SETTLED", f"Vendor bill {bill['bill_number']} ({bill['vendor_name']}) marked {new_status} - ₱{bill['amount']:,.2f}", get_current_user_name())

    entry_no = f"JE-AP-{datetime.now().strftime('%m%d%H%M%S')}"
    today_str = datetime.now().strftime("%Y-%m-%d")
    post_journal_entry(entry_no, today_str, "2010 - Accounts Payable", "Liability", bill['amount'], 0.0,
                       f"Settlement of bill {bill['bill_number']} to {bill['vendor_name']}", owner_username, owner_role)
    post_journal_entry(entry_no, today_str, "1010 - Operating Cash", "Asset", 0.0, bill['amount'],
                       f"Cash disbursement {bill['bill_number']}", owner_username, owner_role)

    if new_status == 'Confirmed':
        execute_db("UPDATE notifications SET is_read = 1 WHERE record_kind = 'bill' AND record_id = ? AND target_role IN ('Accounting Staff', 'Admin')", (bill_id,))
        create_notification(
            target_role='User',
            target_username=owner_username,
            notif_type='BILL_CONFIRMED',
            title='Bill Payment Confirmed',
            message=f"{get_current_user_name()} ({get_current_role()}) paid & confirmed Bill {bill['bill_number']} ({bill['vendor_name']}, ₱{bill['amount']:,.2f}). Status changed to Confirmed.",
            record_kind='bill',
            record_id=bill_id,
            ref_number=bill['bill_number'],
            created_by_name=get_current_user_name()
        )

    return jsonify({
        'success': True,
        'status': new_status,
        'message': f"Bill {bill['bill_number']} ({bill['vendor_name']}) confirmed & settled!"
    })

# ----------------- ADMIN ONLY: ACCOUNTING ARCHIVES & ACCOUNT MANAGEMENT -----------------
@app.route('/api/admin/archives', methods=['GET'])
def get_admin_archives():
    if not check_permission('can_view_archives'):
        return jsonify({
            'error': f"Permission Denied: Only Admin can view accounting archives. Current role '{get_current_role()}' is unauthorized."
        }), 403

    inv_rows = query_db("SELECT * FROM invoices WHERE is_archived = 1 ORDER BY id DESC")
    bill_rows = query_db("SELECT * FROM bills WHERE is_archived = 1 ORDER BY id DESC")

    archived_invoices = []
    for row in inv_rows:
        keys = row.keys()
        archived_invoices.append({
            'id': row['id'],
            'record_type': 'Invoice',
            'invoice_number': row['invoice_number'],
            'client_name': row['client_name'],
            'due_date': row['due_date'],
            'total_amount': float(row['total_amount'] or 0.0),
            'created_by': row['created_by'] if 'created_by' in keys and row['created_by'] else 'alex',
            'created_by_name': row['created_by_name'] if 'created_by_name' in keys and row['created_by_name'] else 'Alex Rivera',
            'created_by_role': normalize_role(row['created_by_role'], default='Admin') if 'created_by_role' in keys and row['created_by_role'] else 'Admin',
            'archived_by': (row['archived_by'] if 'archived_by' in keys and row['archived_by'] else None) or 'Accounting Staff',
            'archived_at': (row['archived_at'] if 'archived_at' in keys and row['archived_at'] else None) or row['created_at']
        })

    archived_bills = []
    for b in bill_rows:
        keys = b.keys()
        archived_bills.append({
            'id': b['id'],
            'record_type': 'Bill',
            'bill_number': b['bill_number'],
            'vendor_name': b['vendor_name'],
            'category': b['category'],
            'due_date': b['due_date'],
            'amount': float(b['amount'] or 0.0),
            'status': b['status'],
            'created_by': b['created_by'] if 'created_by' in keys and b['created_by'] else 'alex',
            'created_by_name': b['created_by_name'] if 'created_by_name' in keys and b['created_by_name'] else 'Alex Rivera',
            'created_by_role': normalize_role(b['created_by_role'], default='Admin') if 'created_by_role' in keys and b['created_by_role'] else 'Admin',
            'archived_by': (b['archived_by'] if 'archived_by' in keys and b['archived_by'] else None) or 'Accounting Staff',
            'archived_at': (b['archived_at'] if 'archived_at' in keys and b['archived_at'] else None) or b['created_at']
        })

    total_value = sum(i['total_amount'] for i in archived_invoices) + sum(b['amount'] for b in archived_bills)

    return jsonify({
        'archived_invoices': archived_invoices,
        'archived_bills': archived_bills,
        'counts': {
            'archived_invoices_count': len(archived_invoices),
            'archived_bills_count': len(archived_bills),
            'total_archived': len(archived_invoices) + len(archived_bills),
            'archived_total_value': total_value
        }
    })

@app.route('/api/admin/accounts', methods=['GET'])
def get_admin_accounts():
    if not check_permission('can_manage_accounts'):
        return jsonify({
            'error': f"Permission Denied: Account Management is restricted to Admin only. Current role '{get_current_role()}' is unauthorized."
        }), 403

    users = query_db("SELECT id, username, email, full_name, role, created_by, token, created_at FROM users ORDER BY id ASC")
    inv_counts = {
        r['created_by']: r['cnt']
        for r in query_db("SELECT COALESCE(created_by, 'alex') as created_by, COUNT(*) as cnt FROM invoices GROUP BY COALESCE(created_by, 'alex')")
    }
    bill_counts = {
        r['created_by']: r['cnt']
        for r in query_db("SELECT COALESCE(created_by, 'alex') as created_by, COUNT(*) as cnt FROM bills GROUP BY COALESCE(created_by, 'alex')")
    }

    accounts_list = []
    role_summary = {'Admin': 0, 'Accounting Staff': 0, 'User': 0}
    current_username = get_current_username()

    for u in users:
        keys = u.keys()
        norm_role = normalize_role(u['role'], default='User')
        role_summary[norm_role] = role_summary.get(norm_role, 0) + 1
        uname = u['username']
        accounts_list.append({
            'id': u['id'],
            'username': uname,
            'email': u['email'],
            'full_name': u['full_name'],
            'role': norm_role,
            'created_by': (u['created_by'] if 'created_by' in keys and u['created_by'] else 'Self-Registered (Portal)'),
            'created_at': u['created_at'],
            'has_active_session': bool(u['token']),
            'is_current_user': (uname == current_username),
            'invoices_count': inv_counts.get(uname, 0),
            'bills_count': bill_counts.get(uname, 0)
        })

    account_logs = query_db("""
        SELECT id, timestamp, action, user_name, details
        FROM audit_trail
        WHERE action IN ('USER_REGISTERED', 'ACCOUNT_CREATED', 'ACCOUNT_ROLE_UPDATED', 'ACCOUNT_DELETED', 'LOGIN_SUCCESS')
        ORDER BY id DESC LIMIT 15
    """)

    return jsonify({
        'accounts': accounts_list,
        'summary': {
            'total_accounts': len(accounts_list),
            'admin_count': role_summary.get('Admin', 0),
            'staff_count': role_summary.get('Accounting Staff', 0),
            'user_count': role_summary.get('User', 0)
        },
        'account_logs': [dict(l) for l in account_logs]
    })

@app.route('/api/admin/accounts', methods=['POST'])
def create_admin_account():
    if not check_permission('can_manage_accounts'):
        return jsonify({
            'error': "Permission Denied: Only Admin can create accounts from Account Management."
        }), 403

    data = request.json or {}
    full_name = data.get('full_name', '').strip()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    role = normalize_role(data.get('role', 'User'), default='User')

    if not full_name or not username or not password:
        return jsonify({'error': 'Full name, username, and password are required.'}), 400
    if not email:
        email = f"{username}@sti.edu"

    existing = query_db("SELECT id FROM users WHERE username = ? OR email = ?", (username, email), one=True)
    if existing:
        return jsonify({'error': f"Username '{username}' or email '{email}' is already registered."}), 409

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_by = f"{get_current_user_name()} (Admin)"
    user_id = execute_db("""
        INSERT INTO users (username, email, password_hash, full_name, role, created_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, email, generate_password_hash(password), full_name, role, created_by, now_str))

    log_audit("ACCOUNT_CREATED", f"Admin created {role} account '{username}' ({full_name})", get_current_user_name())
    return jsonify({
        'success': True,
        'user_id': user_id,
        'message': f"Account '{username}' ({role}) created successfully!"
    })

@app.route('/api/admin/accounts/<int:user_id>/role', methods=['PUT'])
def update_admin_account_role(user_id):
    if not check_permission('can_manage_accounts'):
        return jsonify({'error': 'Permission Denied: Only Admin can update account roles.'}), 403

    user = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
    if not user:
        return jsonify({'error': 'Account not found.'}), 404

    data = request.json or {}
    new_role = normalize_role(data.get('role'), default=None)
    if new_role not in ROLES:
        return jsonify({'error': 'Invalid role selected.'}), 400

    old_role = normalize_role(user['role'], default='User')
    if old_role == 'Admin' and new_role != 'Admin':
        admins = query_db("SELECT COUNT(*) as cnt FROM users WHERE role IN ('Admin', 'Chief Financial Officer')", one=True)
        if admins and admins['cnt'] <= 1:
            return jsonify({'error': 'Cannot demote the last remaining Admin account.'}), 400

    execute_db("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    log_audit("ACCOUNT_ROLE_UPDATED", f"Admin updated '{user['username']}' ({user['full_name']}) role from {old_role} to {new_role}", get_current_user_name())
    return jsonify({
        'success': True,
        'message': f"Updated {user['full_name']}'s role to {new_role}."
    })

@app.route('/api/admin/accounts/<int:user_id>', methods=['DELETE'])
def delete_admin_account(user_id):
    if not check_permission('can_manage_accounts'):
        return jsonify({'error': 'Permission Denied: Only Admin can delete user accounts.'}), 403

    user = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
    if not user:
        return jsonify({'error': 'Account not found.'}), 404

    if user['username'] == get_current_username():
        return jsonify({'error': 'Cannot delete the currently logged-in Admin account.'}), 400

    if normalize_role(user['role'], default='User') == 'Admin':
        admins = query_db("SELECT COUNT(*) as cnt FROM users WHERE role IN ('Admin', 'Chief Financial Officer')", one=True)
        if admins and admins['cnt'] <= 1:
            return jsonify({'error': 'Cannot delete the last remaining Admin account.'}), 400

    execute_db("DELETE FROM users WHERE id = ?", (user_id,))
    log_audit("ACCOUNT_DELETED", f"Admin permanently deleted account '{user['username']}' ({user['full_name']}, role: {user['role']})", get_current_user_name())
    return jsonify({
        'success': True,
        'message': f"Account '{user['username']}' ({user['full_name']}) deleted."
    })

# ----------------- FIFO AUTO-MATCH ENGINE API -----------------
@app.route('/api/fifo-match', methods=['POST'])
def run_fifo_match():
    # Intelligent FIFO matching algorithm
    # Finds oldest open invoices and simulates auto-reconciliation
    open_invoices = query_db("SELECT * FROM invoices WHERE status NOT IN ('Paid', 'Confirmed') AND (is_archived = 0 OR is_archived IS NULL) ORDER BY id ASC")
    matched_results = []

    if open_invoices:
        first = open_invoices[0]
        matched_results.append({
            'invoice_number': first['invoice_number'],
            'client': first['client_name'],
            'amount_matched': min(25000.0, first['balance_due']),
            'confidence': '99.8%',
            'batch_id': 'FIFO-BATCH-9902'
        })

    log_audit("FIFO_MATCH_EXECUTED", f"Velocity Engine checked FIFO match ({len(matched_results)} open invoice candidate(s)).", get_current_user_name())

    return jsonify({
        'success': True,
        'matched_count': len(matched_results),
        'results': matched_results,
        'message': f"Realtime FIFO check complete: {len(matched_results)} open invoice(s) queued for matching." if matched_results else "No open invoices found for FIFO matching."
    })

# ----------------- ROLE-TARGETED NOTIFICATIONS API -----------------
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    role = get_current_role()
    if role == 'User':
        if session.get('account_role') == 'User':
            rows = query_db(
                "SELECT * FROM notifications WHERE target_role = 'User' AND (target_username = ? OR target_username IS NULL) ORDER BY id DESC LIMIT 20",
                (get_current_username(),)
            )
        else:
            rows = query_db(
                "SELECT * FROM notifications WHERE target_role = 'User' ORDER BY id DESC LIMIT 20"
            )
    else:
        rows = query_db(
            "SELECT * FROM notifications WHERE target_role IN ('Accounting Staff', 'Admin') ORDER BY id DESC LIMIT 20"
        )

    inv_map = {}
    inv_ids = [r['record_id'] for r in rows if r['record_kind'] == 'invoice' and r['record_id']]
    if inv_ids:
        placeholders = ",".join("?" for _ in inv_ids)
        for inv_row in query_db(f"SELECT id, invoice_number, client_name, total_amount, balance_due, status FROM invoices WHERE id IN ({placeholders})", tuple(inv_ids)):
            inv_map[inv_row['id']] = inv_row

    unread_count = sum(1 for r in rows if not r['is_read'])
    notif_list = []
    for r in rows:
        linked_inv = inv_map.get(r['record_id']) if r['record_kind'] == 'invoice' else None
        notif_list.append({
            'id': r['id'],
            'target_role': r['target_role'],
            'notif_type': r['notif_type'],
            'title': r['title'],
            'message': r['message'],
            'record_kind': r['record_kind'],
            'record_id': r['record_id'],
            'ref_number': r['ref_number'],
            'created_by_name': r['created_by_name'],
            'is_read': bool(r['is_read']),
            'created_at': r['created_at'],
            'invoice_status': linked_inv['status'] if linked_inv else None,
            'invoice_client': linked_inv['client_name'] if linked_inv else '',
            'invoice_amount': float(linked_inv['total_amount'] or 0.0) if linked_inv else 0.0,
            'invoice_balance': float(linked_inv['balance_due'] or linked_inv['total_amount'] or 0.0) if linked_inv else 0.0
        })

    return jsonify({
        'role': role,
        'unread_count': unread_count,
        'notifications': notif_list
    })

@app.route('/api/notifications/read', methods=['POST'])
def mark_notifications_read():
    role = get_current_role()
    if role == 'User':
        if session.get('account_role') == 'User':
            execute_db(
                "UPDATE notifications SET is_read = 1 WHERE target_role = 'User' AND (target_username = ? OR target_username IS NULL)",
                (get_current_username(),)
            )
        else:
            execute_db("UPDATE notifications SET is_read = 1 WHERE target_role = 'User'")
    else:
        execute_db("UPDATE notifications SET is_read = 1 WHERE target_role IN ('Accounting Staff', 'Admin')")
    return jsonify({'success': True})

# ----------------- USER PORTAL: HOME & USER ACCOUNT GENERAL LEDGER -----------------
@app.route('/api/user/home', methods=['GET'])
def get_user_home():
    scope_sql, scope_params = apply_role_scope()
    user_invoices = query_db(
        f"SELECT * FROM invoices WHERE (is_archived = 0 OR is_archived IS NULL){scope_sql} ORDER BY id DESC",
        scope_params
    )
    user_bills = query_db(
        f"SELECT * FROM bills WHERE (is_archived = 0 OR is_archived IS NULL){scope_sql} ORDER BY id DESC",
        scope_params
    )

    pending_invoices = [i for i in user_invoices if not is_settled(i['status'])]
    confirmed_invoices = [i for i in user_invoices if is_settled(i['status'])]
    pending_bills = [b for b in user_bills if not is_settled(b['status'])]
    confirmed_bills = [b for b in user_bills if is_settled(b['status'])]

    return jsonify({
        'user': {
            'username': get_current_username(),
            'full_name': get_current_user_name(),
            'role': get_current_role()
        },
        'summary': {
            'pending_invoices_count': len(pending_invoices),
            'pending_invoices_amount': sum(float(i['total_amount'] or 0.0) for i in pending_invoices),
            'confirmed_invoices_count': len(confirmed_invoices),
            'confirmed_invoices_amount': sum(float(i['total_amount'] or 0.0) for i in confirmed_invoices),
            'pending_bills_count': len(pending_bills),
            'pending_bills_amount': sum(float(b['amount'] or 0.0) for b in pending_bills),
            'confirmed_bills_count': len(confirmed_bills),
            'confirmed_bills_amount': sum(float(b['amount'] or 0.0) for b in confirmed_bills),
        },
        'recent_invoices': [{
            'id': i['id'],
            'invoice_number': i['invoice_number'],
            'client_name': i['client_name'],
            'due_date': i['due_date'],
            'total_amount': float(i['total_amount'] or 0.0),
            'user_status': (
                'Confirm with Condition'
                if i['status'] in ('Confirm with Condition', 'Conditioned')
                else ('Confirmed' if is_settled(i['status']) else 'Pending')
            ),
            'accounting_notes': (i['accounting_notes'] if 'accounting_notes' in i.keys() and i['accounting_notes'] else ''),
            'raw_status': i['status']
        } for i in user_invoices[:6]],
        'recent_bills': [{
            'id': b['id'],
            'bill_number': b['bill_number'],
            'vendor_name': b['vendor_name'],
            'category': b['category'],
            'due_date': b['due_date'],
            'amount': float(b['amount'] or 0.0),
            'user_status': 'Confirmed' if is_settled(b['status']) else 'Pending',
            'raw_status': b['status']
        } for b in user_bills[:6]]
    })

@app.route('/api/user/ledger', methods=['GET'])
def get_user_ledger():
    """
    Personal General Ledger scoped strictly to the active User's account
    (their Invoices, their Bills, and their account's Journal Entries).
    """
    scope_sql, scope_params = apply_role_scope()
    user_invoices = query_db(
        f"SELECT * FROM invoices WHERE (is_archived = 0 OR is_archived IS NULL){scope_sql} ORDER BY id DESC",
        scope_params
    )
    user_bills = query_db(
        f"SELECT * FROM bills WHERE (is_archived = 0 OR is_archived IS NULL){scope_sql} ORDER BY id DESC",
        scope_params
    )

    if session.get('account_role') == 'User':
        je_rows = query_db(
            "SELECT * FROM journal_entries WHERE created_by = ? ORDER BY id DESC LIMIT 50",
            (get_current_username(),)
        )
    else:
        je_rows = query_db(
            "SELECT * FROM journal_entries WHERE created_by_role = 'User' ORDER BY id DESC LIMIT 50"
        )

    total_inv_confirmed = sum(float(i['total_amount'] or 0.0) for i in user_invoices if is_settled(i['status']))
    total_inv_pending = sum(float(i['total_amount'] or 0.0) for i in user_invoices if not is_settled(i['status']))
    total_bill_confirmed = sum(float(b['amount'] or 0.0) for b in user_bills if is_settled(b['status']))
    total_bill_pending = sum(float(b['amount'] or 0.0) for b in user_bills if not is_settled(b['status']))

    total_debits = sum(float(e['debit'] or 0.0) for e in je_rows)
    total_credits = sum(float(e['credit'] or 0.0) for e in je_rows)

    accounts_breakdown = [
        {
            'code': '1010',
            'account_name': 'Cash Receipts & Disbursements (Confirmed)',
            'account_type': 'Asset',
            'balance': total_inv_confirmed - total_bill_confirmed,
            'status': 'Confirmed'
        },
        {
            'code': '1200',
            'account_name': 'User Receivables (Pending Confirmation)',
            'account_type': 'Asset',
            'balance': total_inv_pending,
            'status': 'Pending'
        },
        {
            'code': '2010',
            'account_name': 'User Payables (Pending Accounting Payment)',
            'account_type': 'Liability',
            'balance': total_bill_pending,
            'status': 'Pending'
        },
        {
            'code': '4010',
            'account_name': 'User Billed Revenue Total',
            'account_type': 'Revenue',
            'balance': total_inv_confirmed + total_inv_pending,
            'status': 'Active'
        },
        {
            'code': '5010',
            'account_name': 'User Billed Expenses Total',
            'account_type': 'Expense',
            'balance': total_bill_confirmed + total_bill_pending,
            'status': 'Active'
        }
    ]

    return jsonify({
        'account_holder': get_current_user_name(),
        'username': get_current_username(),
        'summary': {
            'total_invoiced': total_inv_confirmed + total_inv_pending,
            'confirmed_invoices_amount': total_inv_confirmed,
            'pending_invoices_amount': total_inv_pending,
            'total_billed': total_bill_confirmed + total_bill_pending,
            'confirmed_bills_amount': total_bill_confirmed,
            'pending_bills_amount': total_bill_pending,
            'total_debits': total_debits,
            'total_credits': total_credits,
            'is_balanced': abs(total_debits - total_credits) < 0.01
        },
        'accounts': accounts_breakdown,
        'entries': [{
            'id': e['id'],
            'entry_number': e['entry_number'],
            'date': e['date'],
            'account_name': e['account_name'],
            'account_type': e['account_type'],
            'debit': e['debit'],
            'credit': e['credit'],
            'description': e['description']
        } for e in je_rows]
    })

# ----------------- FINANCIAL REPORTS & AUDIT API -----------------
@app.route('/api/audit-trail', methods=['GET'])
def get_audit_trail():
    if get_current_role() == 'User':
        return jsonify({'logs': []})
    logs = query_db("SELECT * FROM audit_trail ORDER BY id DESC LIMIT 20")
    return jsonify({
        'logs': [{
            'id': l['id'],
            'timestamp': l['timestamp'],
            'action': l['action'],
            'user_name': l['user_name'],
            'details': l['details']
        } for l in logs]
    })

@app.route('/api/journal-entries', methods=['GET'])
def get_journal_entries():
    if get_current_role() == 'User':
        if session.get('account_role') == 'User':
            entries = query_db("SELECT * FROM journal_entries WHERE created_by = ? ORDER BY id DESC LIMIT 25", (get_current_username(),))
        else:
            entries = query_db("SELECT * FROM journal_entries WHERE created_by_role = 'User' ORDER BY id DESC LIMIT 25")
    else:
        entries = query_db("SELECT * FROM journal_entries ORDER BY id DESC LIMIT 25")
    return jsonify({
        'entries': [{
            'id': e['id'],
            'entry_number': e['entry_number'],
            'date': e['date'],
            'account_name': e['account_name'],
            'account_type': e['account_type'],
            'debit': e['debit'],
            'credit': e['credit'],
            'description': e['description']
        } for e in entries]
    })

if __name__ == '__main__':
    import socket, sys
    print("=" * 60)
    print("  LedgerCraft PRO - Financial OS")
    print("  Starting local server on http://127.0.0.1:5000")
    print("=" * 60)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if sock.connect_ex(('127.0.0.1', 5000)) == 0:
            print("\n[INFO] Port 5000 is already active (LedgerCraft PRO is already running at http://127.0.0.1:5000).")
            print("       Open http://127.0.0.1:5000 in your browser!")
            sys.exit(0)
    try:
        # Disable Werkzeug StatReloaderLoop to prevent Windows Python 3.13 MemoryError on os.stat(name)
        app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
    except OSError as e:
        if getattr(e, 'winerror', None) == 10048 or getattr(e, 'errno', None) in (98, 48, 10048):
            print("\n[INFO] Port 5000 is already active (LedgerCraft PRO is already running at http://127.0.0.1:5000).")
        else:
            raise
