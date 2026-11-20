# -*- coding: utf-8 -*-
"""
LedgerCraft PRO - Pure Python UI (Template-Free Architecture)
Replaces all HTML templates with pure Python code.
Contains complete frontend views, RBAC role interfaces, reactive controls,
CRUD dialogs, and real-time synchronization controllers.
"""
from ui_login import render_login_view, LOGIN_HTML
from ui_dashboard import render_dashboard_view, DASHBOARD_HTML

def get_base_styles() -> str:
    return """
        body { font-family: 'Inter', system-ui, -apple-system, sans-serif; background-color: #F8FAFC; }
        .modal-backdrop { background-color: rgba(15, 23, 42, 0.65); backdrop-filter: blur(4px); }
    """

__all__ = ["render_login_view", "render_dashboard_view", "LOGIN_HTML", "DASHBOARD_HTML", "get_base_styles"]
