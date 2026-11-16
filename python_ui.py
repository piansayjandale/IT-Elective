"""
LedgerCraft PRO - Pure Python UI Generator (Template-Free Architecture)
Replaces all HTML templates with modular, pure Python UI components.
Contains complete frontend views, RBAC role interfaces, reactive cart controls,
CRUD dialogs, and real-time synchronization controllers.
"""
import json
import os

def get_base_styles() -> str:
    return """
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: #F8FAFC;
        }
        .modal-backdrop {
            background-color: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(4px);
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 5px;
            height: 5px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #CBD5E1;
            border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: #F1F5F9;
        }
    """

def render_login_view() -> str:
    """Renders the high-velocity LedgerCraft Financial OS login portal in pure Python."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LedgerCraft PRO - Sign In (Financial OS)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        darknavy: {{
                            950: '#030712',
                            900: '#060B18',
                            850: '#080E21',
                            800: '#0B132B',
                            700: '#142045'
                        }}
                    }},
                    fontFamily: {{
                        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
                    }}
                }}
            }}
        }}
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', system-ui, sans-serif;
            background-color: #060B18;
        }}
        .modal-backdrop {{
            background-color: rgba(3, 7, 18, 0.75);
            backdrop-filter: blur(5px);
        }}
    </style>
</head>
<body class="min-h-screen text-slate-100 flex flex-col bg-[#060B18] antialiased overflow-x-hidden">

    <!-- TOP HEADER -->
    <header class="h-14 sm:h-16 px-4 sm:px-8 lg:px-12 xl:px-16 flex items-center justify-between bg-white border-b border-slate-200 z-20 flex-shrink-0 w-full text-slate-800 shadow-xs">
        <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-sm flex-shrink-0">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="7" y1="8" x2="17" y2="8"></line>
                    <line x1="7" y1="12" x2="17" y2="12"></line>
                    <line x1="7" y1="16" x2="13" y2="16"></line>
                </svg>
            </div>
            <span class="text-slate-900 font-extrabold text-lg sm:text-xl tracking-tight select-none">
                LedgerCraft
            </span>
        </div>

        <div class="flex items-center space-x-4 sm:space-x-7 text-xs sm:text-[13px]">
            <a href="#" onclick="openHelpdeskModal()" class="text-slate-700 hover:text-blue-600 font-medium transition cursor-pointer">
                Campus Helpdesk
            </a>
            <a href="#" onclick="openFaqModal()" class="text-slate-700 hover:text-blue-600 font-medium transition cursor-pointer">
                FAQ
            </a>
            <button type="button" onclick="openRegisterModal()" class="inline-flex items-center justify-center bg-[#007CB9] hover:bg-[#006A9F] text-white font-bold text-xs px-5 py-2 rounded-full transition shadow-sm cursor-pointer hover:shadow-md">
                Register
            </button>
        </div>
    </header>

    <!-- MAIN VIEWPORT -->
    <main class="flex-1 w-full grid grid-cols-1 lg:grid-cols-12 min-h-[calc(100vh-4rem)] p-0 m-0 border-0 bg-[#060B18]">
        
        <!-- LEFT COLUMN: HERO -->
        <div class="lg:col-span-7 xl:col-span-7 2xl:col-span-7 p-8 sm:p-12 lg:p-16 xl:p-20 2xl:p-24 flex flex-col justify-between relative overflow-hidden w-full text-slate-100 border-b lg:border-b-0 lg:border-r border-slate-800/80">
            
            <svg class="absolute inset-0 w-full h-full pointer-events-none opacity-45" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="grid-grad" x1="0" y1="0" x2="1" y2="1">
                        <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.18"/>
                        <stop offset="100%" stop-color="#1E3A8A" stop-opacity="0.02"/>
                    </linearGradient>
                </defs>
                <pattern id="chart-grid" width="48" height="48" patternUnits="userSpaceOnUse">
                    <path d="M 48 0 L 0 0 0 48" fill="none" stroke="rgba(59, 130, 246, 0.08)" stroke-width="1"/>
                </pattern>
                <rect width="100%" height="100%" fill="url(#chart-grid)"/>
                <path d="M-100 650 C 150 580, 280 620, 500 480 C 700 350, 900 420, 1200 280" fill="none" stroke="rgba(59, 130, 246, 0.35)" stroke-width="2.5" stroke-dasharray="6 4"/>
                <circle cx="500" cy="480" r="4.5" fill="#60A5FA"/>
                <circle cx="700" cy="350" r="4.5" fill="#3B82F6"/>
            </svg>

            <div class="relative z-10 space-y-6 max-w-xl">
                <div class="inline-flex items-center space-x-2 bg-blue-950/70 border border-blue-500/30 px-3.5 py-1.5 rounded-full text-[11px] font-bold text-blue-400 tracking-wider uppercase">
                    <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
                    <span>Treasury & Ledger Operations</span>
                </div>

                <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white leading-tight tracking-tight">
                    Smart financial orchestration for high-velocity teams.
                </h1>

                <p class="text-slate-400 text-sm sm:text-base leading-relaxed font-normal">
                    Unify journal reconciliations, real-time A/R tracking, and automated cashflows in one secure operating system.
                </p>
            </div>

            <!-- METRIC CARDS -->
            <div class="relative z-10 grid grid-cols-3 gap-3 sm:gap-4 mt-8 pt-6 border-t border-slate-800/80">
                <div class="bg-slate-900/80 p-3 sm:p-4 rounded-xl border border-slate-800 backdrop-blur-xs">
                    <span class="text-[10px] text-slate-400 uppercase font-bold tracking-wider block">Matched Invoices</span>
                    <span class="text-lg sm:text-xl font-extrabold text-white mt-1 block">99.8%</span>
                    <span class="text-[10px] text-blue-400 font-medium">Realtime FIFO match</span>
                </div>

                <div class="bg-slate-900/80 p-3 sm:p-4 rounded-xl border border-slate-800 backdrop-blur-xs">
                    <span class="text-[10px] text-slate-400 uppercase font-bold tracking-wider block">Ledger Velocity</span>
                    <span class="text-lg sm:text-xl font-extrabold text-white mt-1 block">&lt; 120ms</span>
                    <span class="text-[10px] text-emerald-400 font-medium">Sub-second posting</span>
                </div>

                <div class="bg-slate-900/80 p-3 sm:p-4 rounded-xl border border-slate-800 backdrop-blur-xs">
                    <span class="text-[10px] text-slate-400 uppercase font-bold tracking-wider block">Enterprise Ready</span>
                    <span class="text-lg sm:text-xl font-extrabold text-white mt-1 block">SOC 2</span>
                    <span class="text-[10px] text-slate-400 font-medium">Type II certified</span>
                </div>
            </div>
        </div>

        <!-- RIGHT COLUMN: LOGIN FORM -->
        <div class="lg:col-span-5 xl:col-span-5 2xl:col-span-5 p-6 sm:p-10 lg:p-12 xl:p-16 flex flex-col justify-center bg-[#070D1E] relative z-10">
            <div class="max-w-md w-full mx-auto space-y-6">
                
                <div>
                    <h2 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                        Welcome back
                    </h2>
                    <p class="text-xs sm:text-sm text-slate-400 mt-1">
                        Enter your credentials to access your Financial OS workspace.
                    </p>
                </div>

                <!-- ALERTS -->
                <div id="rejection-alert" class="hidden p-3.5 bg-red-950/60 border border-red-500/40 rounded-xl text-xs space-y-1">
                    <div class="flex items-center space-x-2 text-red-400 font-bold">
                        <span>⚠️</span>
                        <span id="alert-title">Access Denied</span>
                    </div>
                    <p id="alert-message" class="text-red-200/90 text-[11px]"></p>
                    <div id="alert-branch" class="text-[10px] text-red-400/80 font-mono mt-1 pt-1 border-t border-red-500/20"></div>
                </div>

                <div id="success-alert" class="hidden p-3.5 bg-emerald-950/60 border border-emerald-500/40 rounded-xl text-xs space-y-1">
                    <div class="flex items-center space-x-2 text-emerald-400 font-bold">
                        <span>✓</span>
                        <span>Authentication Successful</span>
                    </div>
                    <p id="success-message" class="text-emerald-200/90 text-[11px]"></p>
                </div>

                <!-- SSO BUTTON -->
                <button type="button" onclick="handleSsoClick()" class="w-full py-2.5 px-4 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700/80 rounded-xl text-xs font-semibold flex items-center justify-center space-x-2 transition cursor-pointer shadow-xs">
                    <svg class="w-4 h-4" viewBox="0 0 24 24">
                        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
                    </svg>
                    <span>Continue with Okta / SSO</span>
                </button>

                <div class="relative flex items-center justify-center my-4">
                    <div class="border-t border-slate-800 w-full"></div>
                    <span class="bg-[#070D1E] px-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider relative z-10">Or continue with email</span>
                </div>

                <!-- FORM -->
                <form id="form-login" onsubmit="handleLoginSubmit(event)" class="space-y-4">
                    <div>
                        <label class="block text-slate-300 text-xs font-semibold uppercase tracking-wider mb-1.5">
                            Work Email Address
                        </label>
                        <div class="relative">
                            <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500 text-xs">@</span>
                            <input type="text" id="input-username" required placeholder="alex or alex.rivera@acmeglobal.com" class="w-full pl-8 pr-3.5 py-2.5 bg-white text-slate-900 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-blue-500 focus:outline-none transition font-medium">
                        </div>
                    </div>

                    <div>
                        <div class="flex items-center justify-between mb-1.5">
                            <label class="block text-slate-300 text-xs font-semibold uppercase tracking-wider">
                                Password
                            </label>
                            <a href="#" onclick="showForgotPasswordAlert()" class="text-[11px] text-blue-400 hover:text-blue-300 transition">Forgot password?</a>
                        </div>
                        <div class="relative">
                            <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke-width="2"></rect>
                                    <path d="M7 11V7a5 5 0 0110 0v4" stroke-width="2"></path>
                                </svg>
                            </span>
                            <input type="password" id="input-password" required placeholder="••••••••••••" class="w-full pl-9 pr-10 py-2.5 bg-white text-slate-900 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-blue-500 focus:outline-none transition font-medium">
                            <button type="button" onclick="togglePasswordVisibility()" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 cursor-pointer">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div class="flex items-center">
                        <input type="checkbox" id="remember-me" checked class="w-4 h-4 text-blue-600 rounded border-slate-700 bg-slate-900 focus:ring-blue-500">
                        <label for="remember-me" class="ml-2 text-xs text-slate-400 select-none">Remember this workstation for 30 days</label>
                    </div>

                    <button type="submit" id="btn-submit" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-blue-600/30 flex items-center justify-center space-x-2 transition cursor-pointer">
                        <span id="btn-text">Sign In to Workspace →</span>
                        <svg id="btn-spinner" class="hidden animate-spin w-4 h-4 text-white" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    </button>
                </form>

                <div class="pt-4 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500">
                    <button type="button" onclick="fillDemoCredentials('alex', 'password123')" class="text-blue-400 hover:text-blue-300 font-semibold cursor-pointer">
                        ⚡ Quick Fill Demo: Alex Rivera
                    </button>
                    <button type="button" onclick="openProcessTreeModal()" class="text-emerald-400 hover:text-emerald-300 font-semibold cursor-pointer">
                        🌲 Lesson 6 Process Tree
                    </button>
                </div>
            </div>
        </div>
    </main>

    <!-- REGISTER MODAL -->
    <div id="modal-register" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="fixed inset-0 modal-backdrop" onclick="closeRegisterModal()"></div>
        <div class="relative bg-white text-slate-800 rounded-2xl shadow-2xl border border-slate-200 w-full max-w-md overflow-hidden z-10 m-4 flex flex-col">
            <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
                <div class="flex items-center space-x-2">
                    <div class="w-7 h-7 rounded-lg bg-[#007CB9] text-white flex items-center justify-center font-bold text-xs">
                        +
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-slate-900">Register Account</h3>
                        <p class="text-[11px] text-slate-500">Add user to LedgerCraft directory</p>
                    </div>
                </div>
                <button onclick="closeRegisterModal()" class="text-slate-400 hover:text-slate-600 p-1">✕</button>
            </div>
            
            <form onsubmit="handleRegisterSubmit(event)" class="p-6 space-y-3.5 text-xs">
                <div id="reg-error-box" class="hidden p-2.5 bg-red-50 border border-red-200 rounded-lg text-red-700"></div>

                <div>
                    <label class="block font-semibold text-slate-700 mb-1">Full Name *</label>
                    <input type="text" id="reg-fullname" required placeholder="e.g. Yana Brich Palmares" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 font-medium">
                </div>
                <div>
                    <label class="block font-semibold text-slate-700 mb-1">Username / Login ID *</label>
                    <input type="text" id="reg-username" required placeholder="e.g. Brichang123" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 font-medium">
                </div>
                <div>
                    <label class="block font-semibold text-slate-700 mb-1">Institutional Email</label>
                    <input type="email" id="reg-email" placeholder="e.g. name@institution.edu" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20">
                </div>
                <div>
                    <label class="block font-semibold text-slate-700 mb-1">Password *</label>
                    <input type="password" id="reg-password" required placeholder="Minimum 6 characters" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 font-medium">
                </div>
                <div>
                    <label class="block font-semibold text-slate-700 mb-1">Role Assignment</label>
                    <select id="reg-role" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 font-medium bg-white">
                        <option value="Student / Accounting Staff">Student / Accounting Staff (Trainee)</option>
                        <option value="Financial Analyst">Financial Analyst (Operations)</option>
                        <option value="Auditor & Treasury Officer">Auditor & Treasury Officer (Read-Only)</option>
                        <option value="Chief Financial Officer">Chief Financial Officer (Admin)</option>
                    </select>
                </div>

                <div class="pt-3 border-t border-slate-200 flex items-center justify-end space-x-2">
                    <button type="button" onclick="closeRegisterModal()" class="px-4 py-2 border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-50 font-medium">Cancel</button>
                    <button type="submit" id="btn-register-submit" class="px-5 py-2 bg-[#007CB9] hover:bg-[#006A9F] text-white rounded-lg font-bold shadow-sm">Register & Pre-fill</button>
                </div>
            </form>
        </div>
    </div>

    <!-- PROCESS TREE MODAL -->
    <div id="modal-process-tree" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="fixed inset-0 modal-backdrop" onclick="closeProcessTreeModal()"></div>
        <div class="relative bg-slate-900 text-slate-100 rounded-2xl shadow-2xl border border-slate-700 w-full max-w-xl overflow-hidden z-10 m-4 flex flex-col">
            <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950">
                <div class="flex items-center space-x-2">
                    <span class="text-emerald-400 font-bold">🌲</span>
                    <h3 class="text-base font-bold text-white">Lesson 6 Authentication Tree</h3>
                </div>
                <button onclick="closeProcessTreeModal()" class="text-slate-400 hover:text-white p-1">✕</button>
            </div>
            <div class="p-6 space-y-3 text-xs overflow-y-auto max-h-[70vh]">
                <div class="p-3 bg-slate-800/80 rounded-lg border border-slate-700 font-mono">
                    <div class="text-emerald-400 font-bold mb-1">Validation Decision Sequence:</div>
                    1. Input Presence Check (Email & Password non-empty)<br>
                    2. Format Validation (Length & Sanitization)<br>
                    3. User Existence Lookup in Database<br>
                    4. PBKDF2 Password Hash Verification<br>
                    5. Session Security Token Issuance & Role Attaching
                </div>
            </div>
        </div>
    </div>

    <script>
        function togglePasswordVisibility() {{
            const p = document.getElementById('input-password');
            p.type = p.type === 'password' ? 'text' : 'password';
        }}

        function fillDemoCredentials(u, p) {{
            document.getElementById('input-username').value = u;
            document.getElementById('input-password').value = p;
        }}

        function openRegisterModal() {{
            document.getElementById('modal-register').classList.remove('hidden');
        }}

        function closeRegisterModal() {{
            document.getElementById('modal-register').classList.add('hidden');
        }}

        function openProcessTreeModal() {{
            document.getElementById('modal-process-tree').classList.remove('hidden');
        }}

        function closeProcessTreeModal() {{
            document.getElementById('modal-process-tree').classList.add('hidden');
        }}

        function openHelpdeskModal() {{
            alert("LedgerCraft Campus Helpdesk\\n\\nPortal: https://one.sti.edu\\nEmail: helpdesk@institution.edu\\nHotline: (02) 8887-8447");
        }}

        function openFaqModal() {{
            alert("LedgerCraft FAQ:\\n\\n1. What is this portal?\\nOfficial LedgerCraft PRO Financial OS & IT Elective Treasury System.\\n\\n2. Demo Accounts:\\nalex / password123 (CFO)\\nBrichang123 / 123456789");
        }}

        function handleSsoClick() {{
            fillDemoCredentials('alex.rivera@acmeglobal.com', 'password123');
            alert("SSO simulation: Pre-filled Enterprise Okta credentials for Alex Rivera (CFO).");
        }}

        function showForgotPasswordAlert() {{
            alert("Contact Security Administrator: security@acmeglobal.com for password reset.");
        }}

        async function handleRegisterSubmit(e) {{
            e.preventDefault();
            const fullName = document.getElementById('reg-fullname').value.trim();
            const username = document.getElementById('reg-username').value.trim();
            const email = document.getElementById('reg-email').value.trim();
            const password = document.getElementById('reg-password').value;
            const role = document.getElementById('reg-role').value;
            const errBox = document.getElementById('reg-error-box');

            try {{
                const res = await fetch('/api/register', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ full_name: fullName, username, email, password, role }})
                }});
                const data = await res.json();
                if (!res.ok) {{
                    errBox.innerText = data.error || 'Registration failed.';
                    errBox.classList.remove('hidden');
                }} else {{
                    closeRegisterModal();
                    fillDemoCredentials(username, password);
                    alert(`Registration Successful!\\n\\nAccount registered:\\n• Name: ${{fullName}}\\n• Username: ${{username}}\\n• Role: ${{role}}\\n\\nCredentials pre-filled. Click 'Sign In to Workspace'.`);
                }}
            }} catch (err) {{
                errBox.innerText = 'Network error connecting to registration gateway.';
                errBox.classList.remove('hidden');
            }}
        }}

        async function handleLoginSubmit(e) {{
            e.preventDefault();
            const username = document.getElementById('input-username').value.trim();
            const password = document.getElementById('input-password').value;

            const btnText = document.getElementById('btn-text');
            const btnSpinner = document.getElementById('btn-spinner');
            const btnSubmit = document.getElementById('btn-submit');

            btnText.innerText = "Authenticating...";
            btnSpinner.classList.remove('hidden');
            btnSubmit.disabled = true;

            try {{
                const response = await fetch('/api/login', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ username, password }})
                }});

                const data = await response.json();

                if (!response.ok) {{
                    const alertBox = document.getElementById('rejection-alert');
                    document.getElementById('alert-title').innerText = "Rejection Alert: Access Denied";
                    document.getElementById('alert-message').innerText = data.message || "Invalid credentials.";
                    document.getElementById('alert-branch').innerText = "Validation Decision Node Failed";
                    alertBox.classList.remove('hidden');
                }} else {{
                    const successBox = document.getElementById('success-alert');
                    document.getElementById('success-message').innerText = `Welcome, ${{data.user.full_name}} (${{data.user.role}}). Token issued. Launching workspace...`;
                    successBox.classList.remove('hidden');

                    setTimeout(() => {{
                        window.location.href = data.redirect || '/';
                    }}, 600);
                }}
            }} catch (err) {{
                const alertBox = document.getElementById('rejection-alert');
                document.getElementById('alert-title').innerText = "Communication Failure";
                document.getElementById('alert-message').innerText = "Unable to connect to Treasury Gateway.";
                alertBox.classList.remove('hidden');
            }} finally {{
                btnSpinner.classList.add('hidden');
                btnSubmit.disabled = false;
                btnText.innerText = "Sign In to Workspace →";
            }}
        }}
    </script>
</body>
</html>
"""

def render_dashboard_view(user: dict = None, current_user: dict = None) -> str:
    """Renders the complete LedgerCraft PRO financial operating system with full side navigation."""
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    active_user = user or current_user
    user_name = active_user.get('name', 'Alex Rivera (CFO)') if active_user else 'Alex Rivera (CFO)'
    user_role = active_user.get('role', 'Chief Financial Officer') if active_user else 'Chief Financial Officer'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LedgerCraft PRO - Financial Operating System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        {get_base_styles()}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col font-sans">

    <!-- TOP HEADER -->
    <header class="h-16 px-6 bg-white border-b border-slate-200 flex items-center justify-between sticky top-0 z-30 shadow-xs">
        <!-- Left: Brand Logo & Workspace -->
        <div class="flex items-center space-x-3">
            <div class="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center text-white font-extrabold text-base shadow-sm">
                LC
            </div>
            <div>
                <div class="flex items-center space-x-2">
                    <span class="text-base font-extrabold text-slate-900 tracking-tight">LedgerCraft PRO</span>
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200">Financial OS</span>
                </div>
                <div class="text-[11px] text-slate-500 font-medium">Acme Global Inc. · Philippine Peso (PHP · ₱)</div>
            </div>
        </div>

        <!-- Right: Actions, Live Sync, Role Switcher, Notifications -->
        <div class="flex items-center space-x-4">
            
            <!-- Live Admin Sync Badge -->
            <div class="flex items-center space-x-1.5 bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full border border-emerald-200 text-xs font-semibold">
                <span id="live-sync-indicator" class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span id="sync-status-text">Live Sync</span>
            </div>

            <!-- Role Switcher (RBAC) -->
            <div class="relative">
                <button id="btn-role-switcher" onclick="toggleRoleDropdown()" class="flex items-center space-x-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold px-3 py-1.5 rounded-lg border border-slate-200 transition cursor-pointer">
                    <span id="header-role-badge">👑 CFO (Admin)</span>
                    <span class="text-[10px] text-slate-500">▾</span>
                </button>
                <div id="dropdown-roles" class="hidden absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-2xl border border-slate-200 z-50 p-2 text-xs">
                    <div class="px-2 py-1 text-[10px] font-bold uppercase text-slate-400 tracking-wider">Switch Active Role (RBAC)</div>
                    <button onclick="setSessionRole('Chief Financial Officer')" class="w-full text-left p-2 rounded-lg hover:bg-slate-50 font-semibold text-slate-800 flex items-center justify-between">
                        <span>👑 Chief Financial Officer</span>
                        <span class="text-[10px] text-emerald-600 font-bold">Full Access</span>
                    </button>
                    <button onclick="setSessionRole('Financial Analyst')" class="w-full text-left p-2 rounded-lg hover:bg-slate-50 font-semibold text-slate-800 flex items-center justify-between">
                        <span>📊 Financial Analyst</span>
                        <span class="text-[10px] text-blue-600 font-bold">Operations</span>
                    </button>
                    <button onclick="setSessionRole('Auditor & Treasury Officer')" class="w-full text-left p-2 rounded-lg hover:bg-slate-50 font-semibold text-slate-800 flex items-center justify-between">
                        <span>🔍 Auditor & Treasury Officer</span>
                        <span class="text-[10px] text-amber-600 font-bold">Read-Only</span>
                    </button>
                    <button onclick="setSessionRole('Student / Accounting Staff')" class="w-full text-left p-2 rounded-lg hover:bg-slate-50 font-semibold text-slate-800 flex items-center justify-between">
                        <span>🎓 Student / Accounting Staff</span>
                        <span class="text-[10px] text-slate-500 font-bold">Trainee</span>
                    </button>
                </div>
            </div>

            <!-- Global Search -->
            <div class="relative hidden sm:block">
                <input type="text" id="global-search" oninput="handleTableSearch(this.value)" placeholder="Search (Ctrl + K)..." class="w-48 lg:w-56 px-3.5 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20">
            </div>

            <!-- + New Invoice Button -->
            <button onclick="openNewInvoiceModal()" class="flex items-center space-x-1 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-4 py-2 rounded-lg shadow-sm shadow-blue-500/20 transition cursor-pointer">
                <span>+ New Invoice</span>
            </button>

            <!-- Notification Bell -->
            <div class="relative">
                <button id="btn-notifications" onclick="toggleNotificationDropdown()" class="p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition relative cursor-pointer">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
                    </svg>
                    <span id="notif-badge" class="absolute top-1.5 right-1.5 w-2 h-2 bg-blue-600 rounded-full"></span>
                </button>
                <div id="dropdown-notifications" class="hidden absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-2xl border border-slate-200 z-50 p-3 text-xs">
                    <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                        <span class="font-bold text-slate-900">Notifications</span>
                        <span class="text-[10px] text-blue-600 font-semibold cursor-pointer" onclick="clearNotifications()">Mark all read</span>
                    </div>
                    <div class="py-2 space-y-2 text-slate-600">
                        <div class="p-2 bg-slate-50 rounded border border-slate-100">
                            <span class="font-semibold text-slate-800">Auto-Reconciled</span> · FIFO match posted ₱48,000.00
                        </div>
                        <div class="p-2 bg-slate-50 rounded border border-slate-100">
                            <span class="font-semibold text-slate-800">Audit Alert</span> · Invoice #INV-2024-003 past due date
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sign Out -->
            <button onclick="handleLogout()" title="Sign Out" class="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition cursor-pointer">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                </svg>
            </button>
        </div>
    </header>

    <!-- MAIN BODY -->
    <div class="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">

        <!-- TAB NAVIGATION BAR -->
        <div class="flex items-center justify-between border-b border-slate-200 pb-3">
            <div class="flex space-x-2">
                <button id="tab-btn-ar" onclick="switchTab('ar')" class="px-4 py-2 bg-blue-600 text-white rounded-lg text-xs font-bold shadow-sm shadow-blue-500/20 transition">
                    Accounts Receivable (Invoices)
                </button>
                <button id="tab-btn-ap" onclick="switchTab('ap')" class="px-4 py-2 bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 rounded-lg text-xs font-semibold transition">
                    Accounts Payable (Bills)
                </button>
                <button onclick="showJournalEntries()" class="px-3.5 py-2 bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 rounded-lg text-xs font-semibold transition">
                    Journal Entries (GL)
                </button>
                <button onclick="showAuditTrail()" class="px-3.5 py-2 bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 rounded-lg text-xs font-semibold transition">
                    Audit Trail
                </button>
            </div>
            
            <button onclick="triggerFifoMatch()" class="px-3.5 py-2 bg-slate-900 hover:bg-black text-white rounded-lg text-xs font-bold flex items-center space-x-1.5 shadow-sm transition">
                <span>⚡ Realtime FIFO Auto-Match</span>
            </button>
        </div>

        <!-- 3 KPI METRIC CARDS (WHITE PADDED CARDS MATCHING REFERENCE) -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="p-6 bg-white rounded-2xl border border-slate-200/80 shadow-xs flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-slate-400">
                        <span>Total Outstanding</span>
                        <span class="w-7 h-7 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center font-bold">📄</span>
                    </div>
                    <div id="stat-outstanding" class="text-3xl font-extrabold text-slate-900 mt-3 tracking-tight">₱842,500.00</div>
                </div>
                <div class="text-xs text-slate-400 mt-2 font-medium">42 open invoices across active ledgers</div>
            </div>

            <div class="p-6 bg-white rounded-2xl border border-slate-200/80 shadow-xs flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-slate-400">
                        <span>Overdue</span>
                        <span class="w-7 h-7 rounded-lg bg-red-50 text-red-600 flex items-center justify-center font-bold">⚠️</span>
                    </div>
                    <div id="stat-overdue" class="text-3xl font-extrabold text-red-600 mt-3 tracking-tight">₱25,000.00</div>
                </div>
                <div class="text-xs text-slate-400 mt-2 font-medium">2 accounts requiring immediate dunning</div>
            </div>

            <div class="p-6 bg-white rounded-2xl border border-slate-200/80 shadow-xs flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-slate-400">
                        <span>Collected This Month</span>
                        <span class="w-7 h-7 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">✓</span>
                    </div>
                    <div id="stat-collected" class="text-3xl font-extrabold text-slate-900 mt-3 tracking-tight">₱381,600.00</div>
                </div>
                <div class="text-xs text-emerald-600 mt-2 font-semibold">+12% compared to last monthly cycle</div>
            </div>
        </div>

        <!-- VIEW: ACCOUNTS RECEIVABLE (INVOICES TABLE) -->
        <div id="view-ar-container" class="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
            
            <!-- Table Toolbar -->
            <div class="p-5 border-b border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <h3 class="text-base font-bold text-slate-900">Invoices & Receivables Ledger</h3>
                    <p class="text-xs text-slate-500">Real-time GAAP compliant billing ledger</p>
                </div>
                
                <div class="flex items-center space-x-3 w-full sm:w-auto">
                    <!-- Status Filter Dropdown -->
                    <select id="filter-status" onchange="handleFilterChange(this.value)" class="p-2 border border-slate-200 rounded-lg text-xs font-semibold text-slate-700 bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500/20">
                        <option value="All">Status: All Statuses</option>
                        <option value="Paid">Status: Paid</option>
                        <option value="Sent">Status: Sent</option>
                        <option value="Overdue">Status: Overdue</option>
                        <option value="Partial">Status: Partial</option>
                        <option value="Draft">Status: Draft</option>
                        <option value="Archived">Status: Archived (🗄️)</option>
                    </select>

                    <div class="relative sm:hidden w-full">
                        <input type="text" oninput="handleTableSearch(this.value)" placeholder="Search client or invoice #..." class="w-full p-2 border border-slate-200 rounded-lg text-xs bg-slate-50">
                    </div>
                </div>
            </div>

            <!-- INVOICES TABLE (WITH ARCHIVE ICON IN ACTION COLUMN) -->
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs">
                    <thead>
                        <tr class="bg-slate-50/80 text-slate-400 uppercase text-[10px] font-bold tracking-wider border-b border-slate-100">
                            <th class="py-3.5 px-6">INVOICE #</th>
                            <th class="py-3.5 px-6">CLIENT</th>
                            <th class="py-3.5 px-6">DUE DATE</th>
                            <th class="py-3.5 px-6">AMOUNT</th>
                            <th class="py-3.5 px-6">STATUS</th>
                            <th class="py-3.5 px-6 text-center">ACTION</th>
                        </tr>
                    </thead>
                    <tbody id="invoices-table-body" class="divide-y divide-slate-100 font-medium">
                        <!-- Dynamic Invoice Rows with Archive Icon -->
                    </tbody>
                </table>
            </div>

            <!-- Pagination Bar -->
            <div class="p-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span id="pagination-info">Showing 5 of 42 invoices</span>
                <div class="flex space-x-1">
                    <button id="btn-page-prev" onclick="changePage(currentPage - 1)" class="px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded text-slate-700 font-semibold disabled:opacity-40">Previous</button>
                    <button id="btn-page-next" onclick="changePage(currentPage + 1)" class="px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded text-slate-700 font-semibold disabled:opacity-40">Next</button>
                </div>
            </div>
        </div>

        <!-- VIEW: ACCOUNTS PAYABLE (BILLS) -->
        <div id="view-ap-container" class="hidden bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
            <div class="p-5 border-b border-slate-100">
                <h3 class="text-base font-bold text-slate-900">Accounts Payable (Vendor Bills)</h3>
                <p class="text-xs text-slate-500">Enterprise liabilities & automated disbursements</p>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs">
                    <thead>
                        <tr class="bg-slate-50 text-slate-400 uppercase text-[10px] font-bold border-b border-slate-100">
                            <th class="py-3.5 px-6">BILL #</th>
                            <th class="py-3.5 px-6">VENDOR</th>
                            <th class="py-3.5 px-6">CATEGORY</th>
                            <th class="py-3.5 px-6">DUE DATE</th>
                            <th class="py-3.5 px-6">AMOUNT</th>
                            <th class="py-3.5 px-6">STATUS</th>
                            <th class="py-3.5 px-6 text-center">ACTION</th>
                        </tr>
                    </thead>
                    <tbody id="bills-table-body" class="divide-y divide-slate-100 font-medium">
                        <!-- Dynamic Bill Rows -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- VIEW: REPORTS / AUDIT TRAIL / GL -->
        <div id="view-reports-container" class="hidden bg-white rounded-2xl border border-slate-200/80 shadow-xs p-6">
            <div id="reports-content-box"></div>
        </div>

    </div>

    <!-- MODAL 1: NEW INVOICE -->
    <div id="modal-new-invoice" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="fixed inset-0 modal-backdrop" onclick="closeModal('modal-new-invoice')"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-2xl overflow-hidden z-10 m-4 flex flex-col max-h-[90vh]">
            <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
                <h3 class="text-base font-bold text-slate-900">+ Create Accounts Receivable Invoice</h3>
                <button onclick="closeModal('modal-new-invoice')" class="text-slate-400 hover:text-slate-600 p-1">✕</button>
            </div>
            <form id="form-new-invoice" onsubmit="handleCreateInvoice(event)" class="p-6 overflow-y-auto space-y-4 text-xs">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1">Client Name *</label>
                        <input type="text" id="inv-client-name" required placeholder="e.g. Apex Cloud Technologies" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 font-medium">
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1">Client Billing Email</label>
                        <input type="email" id="inv-client-email" placeholder="accounting@client.com" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20">
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1">Due Date</label>
                        <input type="date" id="inv-due-date" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20">
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1">Custom Invoice # (Optional)</label>
                        <input type="text" id="inv-custom-num" placeholder="Auto-generated if blank" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20">
                    </div>
                </div>

                <!-- Dynamic Cart Line Items -->
                <div class="pt-2">
                    <div class="flex items-center justify-between mb-2">
                        <label class="font-bold text-slate-800 uppercase tracking-wider text-[10px]">Line Items (Reactive Cart)</label>
                        <button type="button" onclick="addNewLineItemRow()" class="text-blue-600 font-bold hover:text-blue-700 text-xs">+ Add Item</button>
                    </div>
                    <div class="border border-slate-200 rounded-xl overflow-hidden">
                        <table class="w-full text-left text-xs">
                            <thead class="bg-slate-50 text-slate-500 text-[10px] font-bold border-b border-slate-200">
                                <tr>
                                    <th class="p-2.5">Description</th>
                                    <th class="p-2.5 w-20 text-center">Qty</th>
                                    <th class="p-2.5 w-32 text-right">Price (₱)</th>
                                    <th class="p-2.5 w-10"></th>
                                </tr>
                            </thead>
                            <tbody id="new-invoice-items-tbody" class="divide-y divide-slate-100">
                                <tr>
                                    <td class="p-2"><input type="text" class="item-desc w-full p-1.5 border border-slate-200 rounded" value="Enterprise Ledger Analytics Engine" required></td>
                                    <td class="p-2"><input type="number" min="1" class="item-qty w-full p-1.5 border border-slate-200 rounded text-center" value="1" oninput="calculateNewInvoiceTotal()"></td>
                                    <td class="p-2"><input type="number" min="0" step="any" class="item-price w-full p-1.5 border border-slate-200 rounded text-right" value="48000" oninput="calculateNewInvoiceTotal()"></td>
                                    <td class="p-2 text-center"><button type="button" onclick="removeLineItem(this)" class="text-slate-400 hover:text-red-500 font-bold">✕</button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Cart Total Preview -->
                <div class="flex justify-end pt-2">
                    <div class="w-64 p-3 bg-slate-50 rounded-xl border border-slate-200 text-right space-y-1">
                        <div class="flex justify-between text-slate-600"><span>Subtotal:</span><span id="new-inv-subtotal">₱48,000.00</span></div>
                        <div class="flex justify-between text-slate-600"><span>12% VAT:</span><span id="new-inv-vat">₱5,760.00</span></div>
                        <div class="flex justify-between font-bold text-slate-900 border-t pt-1"><span>Grand Total:</span><span id="new-invoice-total-display" class="text-blue-600">₱53,760.00</span></div>
                    </div>
                </div>

                <div class="pt-4 border-t border-slate-200 flex justify-end space-x-2">
                    <button type="button" onclick="closeModal('modal-new-invoice')" class="px-4 py-2 border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-50">Cancel</button>
                    <button type="submit" class="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold shadow-sm">Issue Invoice</button>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL 2: EDIT INVOICE (CRUD UPDATE) -->
    <div id="modal-edit-invoice" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="fixed inset-0 modal-backdrop" onclick="closeModal('modal-edit-invoice')"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-2xl overflow-hidden z-10 m-4 flex flex-col max-h-[90vh]">
            <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-gradient-to-r from-blue-50 to-indigo-50">
                <div class="flex items-center space-x-2">
                    <span class="text-blue-600 font-bold text-base">✎</span>
                    <h3 class="text-base font-bold text-slate-900">Edit Invoice <span id="edit-invoice-number-badge" class="px-2 py-0.5 rounded-full text-xs font-mono font-bold bg-blue-100 text-blue-700">#INV-2024-001</span></h3>
                </div>
                <button onclick="closeModal('modal-edit-invoice')" class="text-slate-400 hover:text-slate-600 p-1">✕</button>
            </div>
            <form id="form-edit-invoice" onsubmit="handleUpdateInvoice(event)" class="p-6 overflow-y-auto space-y-4 text-xs">
                <input type="hidden" id="edit-invoice-id">
                
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1">Client Organization *</label>
                        <input type="text" id="edit-client-name" required class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 font-semibold text-slate-800">
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1">Billing Email</label>
                        <input type="email" id="edit-client-email" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 text-slate-700">
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1">Due Date</label>
                        <input type="date" id="edit-due-date" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20">
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1">Status</label>
                        <select id="edit-status" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 font-semibold text-slate-800">
                            <option value="Draft">Draft</option>
                            <option value="Sent">Sent</option>
                            <option value="Partial">Partial</option>
                            <option value="Paid">Paid</option>
                            <option value="Overdue">Overdue</option>
                        </select>
                    </div>
                </div>

                <!-- Edit Line Items -->
                <div class="pt-2">
                    <div class="flex items-center justify-between mb-2">
                        <label class="font-bold text-slate-800 uppercase tracking-wider text-[10px]">Line Items (Reactive Cart)</label>
                        <button type="button" onclick="addEditLineItem()" class="text-blue-600 font-bold hover:text-blue-700 text-xs">+ Add Item</button>
                    </div>
                    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-xs">
                        <table class="w-full text-left text-xs">
                            <thead class="bg-slate-50 text-slate-500 text-[10px] font-bold border-b border-slate-200">
                                <tr>
                                    <th class="py-2.5 px-3">Description</th>
                                    <th class="py-2.5 px-3 w-20 text-center">Qty</th>
                                    <th class="py-2.5 px-3 w-32 text-right">Price (₱)</th>
                                    <th class="py-2.5 px-3 w-28 text-right">Total (₱)</th>
                                    <th class="py-2.5 px-2 w-10"></th>
                                </tr>
                            </thead>
                            <tbody id="edit-items-tbody" class="divide-y divide-slate-100"></tbody>
                        </table>
                    </div>
                </div>

                <div>
                    <label class="block text-slate-700 font-semibold mb-1">Internal Notes</label>
                    <textarea id="edit-notes" rows="2" class="w-full p-2.5 border border-slate-300 rounded-lg text-xs" placeholder="Optional audit memo..."></textarea>
                </div>

                <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex flex-col items-end space-y-1 text-xs">
                    <div class="flex justify-between w-64 text-slate-600"><span>Subtotal:</span><span id="edit-subtotal-display" class="font-semibold text-slate-800">₱0.00</span></div>
                    <div class="flex justify-between w-64 text-slate-600"><span>Philippine VAT (12%):</span><span id="edit-vat-display" class="font-semibold text-slate-800">₱0.00</span></div>
                    <div class="flex justify-between w-64 text-slate-900 font-extrabold text-sm pt-1 border-t border-slate-200"><span>Grand Total:</span><span id="edit-grand-total-display" class="text-blue-600">₱0.00</span></div>
                </div>

                <div class="pt-4 border-t border-slate-200 flex items-center justify-between">
                    <button type="button" onclick="handleArchiveFromEditModal()" class="px-3.5 py-2 bg-amber-50 hover:bg-amber-100 text-amber-700 border border-amber-200 rounded-lg font-semibold flex items-center space-x-1.5 transition">
                        <span>🗄️</span><span>Archive Invoice</span>
                    </button>
                    <div class="flex items-center space-x-2">
                        <button type="button" onclick="closeModal('modal-edit-invoice')" class="px-4 py-2 border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-50">Cancel</button>
                        <button type="submit" class="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold shadow-sm">Save Changes</button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL 3: RECORD PAYMENT -->
    <div id="modal-record-payment" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="fixed inset-0 modal-backdrop" onclick="closeModal('modal-record-payment')"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-md overflow-hidden z-10 m-4 flex flex-col">
            <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-emerald-50">
                <h3 class="text-base font-bold text-slate-900">Record Settlement Payment</h3>
                <button onclick="closeModal('modal-record-payment')" class="text-slate-400 hover:text-slate-600 p-1">✕</button>
            </div>
            <form onsubmit="handleRecordPaymentSubmit(event)" class="p-6 space-y-3.5 text-xs">
                <input type="hidden" id="pay-invoice-id">
                <div>
                    <label class="block text-slate-700 font-semibold mb-1">Invoice Reference</label>
                    <input type="text" id="pay-invoice-num" readonly class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg font-semibold text-slate-800">
                </div>
                <div>
                    <label class="block text-slate-700 font-semibold mb-1">Payment Amount (₱) *</label>
                    <input type="number" id="pay-amount" step="any" required class="w-full p-2.5 border border-slate-300 rounded-lg font-bold text-slate-900 focus:ring-2 focus:ring-blue-500/20">
                </div>
                <div>
                    <label class="block text-slate-700 font-semibold mb-1">Payment Method</label>
                    <select id="pay-method" class="w-full p-2.5 border border-slate-300 rounded-lg font-medium">
                        <option value="Wire Transfer">Wire Transfer (FedWire / SWIFT)</option>
                        <option value="ACH Direct Debit">ACH Direct Debit</option>
                        <option value="Corporate Check">Corporate Check</option>
                        <option value="Credit Card">Credit Card</option>
                    </select>
                </div>
                <div>
                    <label class="block text-slate-700 font-semibold mb-1">Transaction Reference #</label>
                    <input type="text" id="pay-ref" required placeholder="e.g. WIRE-TX-89214" class="w-full p-2.5 border border-slate-300 rounded-lg">
                </div>
                <div class="pt-3 border-t border-slate-200 flex justify-end space-x-2">
                    <button type="button" onclick="closeModal('modal-record-payment')" class="px-4 py-2 border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-50">Cancel</button>
                    <button type="submit" class="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-bold shadow-sm">Confirm Payment</button>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL 4: VIEW INVOICE VOUCHER -->
    <div id="modal-view-details" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="fixed inset-0 modal-backdrop" onclick="closeModal('modal-view-details')"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-2xl overflow-hidden z-10 m-4 flex flex-col max-h-[90vh]">
            <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
                <div class="flex items-center space-x-2">
                    <span id="detail-invoice-badge" class="px-2.5 py-0.5 rounded-full font-bold text-xs bg-blue-100 text-blue-700">#INV-2024-001</span>
                    <span class="text-xs text-slate-400">· Official Tax Invoice Voucher</span>
                </div>
                <button onclick="closeModal('modal-view-details')" class="text-slate-400 hover:text-slate-600 p-1">✕</button>
            </div>
            <div id="detail-modal-body" class="p-6 overflow-y-auto space-y-4 text-xs"></div>
        </div>
    </div>

    <!-- MODAL 5: ROLE PERMISSION DENIED (RBAC) -->
    <div id="modal-permission-denied" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="fixed inset-0 modal-backdrop" onclick="closeModal('modal-permission-denied')"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl border border-red-200 w-full max-w-md overflow-hidden z-10 m-4 flex flex-col">
            <div class="p-6 text-center space-y-4">
                <div class="w-14 h-14 mx-auto rounded-full bg-red-100 text-red-600 flex items-center justify-center text-2xl font-bold border-2 border-red-200">
                    🔒
                </div>
                <div>
                    <h3 class="text-lg font-extrabold text-slate-900">Access Restricted (RBAC)</h3>
                    <p class="text-xs text-slate-500 mt-1">Your current active role lacks permission for this operation.</p>
                </div>
                <div class="p-3 bg-red-50 border border-red-200 rounded-xl text-left text-xs space-y-1.5">
                    <div class="flex justify-between"><span class="text-slate-500">Attempted Action:</span><span id="perm-denied-action" class="font-bold text-red-700">Action</span></div>
                    <div class="flex justify-between"><span class="text-slate-500">Active Role:</span><span id="perm-denied-current-role" class="font-bold text-slate-800">Role</span></div>
                    <div class="flex justify-between"><span class="text-slate-500">Required Role:</span><span id="perm-denied-required-role" class="font-bold text-emerald-700">CFO</span></div>
                </div>
                <div class="pt-2 flex flex-col space-y-2">
                    <button onclick="setSessionRole('Chief Financial Officer'); closeModal('modal-permission-denied');" class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md transition">
                        Switch to Chief Financial Officer (Full Access)
                    </button>
                    <button onclick="closeModal('modal-permission-denied')" class="w-full py-2 bg-slate-100 hover:bg-slate-200 text-slate-600 font-semibold text-xs rounded-xl transition">
                        Dismiss
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL 6: SEND OVERDUE NOTICE -->
    <div id="modal-send-reminder" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="fixed inset-0 modal-backdrop" onclick="closeModal('modal-send-reminder')"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-md overflow-hidden z-10 m-4 flex flex-col">
            <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-red-50">
                <h3 class="text-base font-bold text-slate-900">Dispatch Dunning Notice</h3>
                <button onclick="closeModal('modal-send-reminder')" class="text-slate-400 hover:text-slate-600 p-1">✕</button>
            </div>
            <div class="p-6 space-y-3.5 text-xs">
                <input type="hidden" id="reminder-invoice-id">
                <div>
                    <label class="block text-slate-700 font-semibold mb-1">Client</label>
                    <input type="text" id="reminder-client-name" readonly class="w-full p-2 bg-slate-50 border border-slate-200 rounded font-semibold text-slate-800">
                </div>
                <div>
                    <label class="block text-slate-700 font-semibold mb-1">Pre-composed Notice</label>
                    <textarea id="reminder-body-preview" rows="4" class="w-full p-2.5 border border-slate-300 rounded font-mono text-slate-700"></textarea>
                </div>
                <div class="pt-3 border-t border-slate-200 flex justify-end space-x-2">
                    <button onclick="closeModal('modal-send-reminder')" class="px-4 py-2 border border-slate-200 text-slate-600 rounded">Cancel</button>
                    <button onclick="executeSendReminder()" class="px-5 py-2 bg-red-600 hover:bg-red-700 text-white rounded font-bold">Send Notice</button>
                </div>
            </div>
        </div>
    </div>

    <!-- TOAST NOTIFICATION CONTAINER -->
    <div id="toast-container" class="fixed bottom-6 right-6 z-50 flex flex-col space-y-2 pointer-events-none"></div>

    <!-- PURE JAVASCRIPT CONTROLLERS -->
    <script>
        let currentTab = 'ar';
        let currentStatusFilter = 'All';
        let currentSearchQuery = '';
        let currentPage = 1;
        let totalPages = 1;
        let currentUserRole = "{user_role}";
        let userPermissions = {{}};

        document.addEventListener('DOMContentLoaded', () => {{
            fetchStats();
            loadInvoices();
            loadBills();
            fetchCurrentUser();
            setInterval(syncAdminState, 8000);
        }});

        function formatCurrency(val) {{
            const num = parseFloat(val) || 0;
            return '₱' + num.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
        }}

        function openModal(id) {{ document.getElementById(id).classList.remove('hidden'); }}
        function closeModal(id) {{ document.getElementById(id).classList.add('hidden'); }}

        function toggleRoleDropdown() {{
            const el = document.getElementById('dropdown-roles');
            if (el) el.classList.toggle('hidden');
        }}

        function toggleNotificationDropdown() {{
            const el = document.getElementById('dropdown-notifications');
            if (el) el.classList.toggle('hidden');
        }}

        function clearNotifications() {{
            const badge = document.getElementById('notif-badge');
            if (badge) badge.classList.add('hidden');
            showToast("Notifications marked as read", "success");
        }}

        document.addEventListener('click', (e) => {{
            const rDrop = document.getElementById('dropdown-roles');
            const rBtn = document.getElementById('btn-role-switcher');
            if (rDrop && !rDrop.classList.contains('hidden')) {{
                if (rBtn && !rBtn.contains(e.target) && !rDrop.contains(e.target)) rDrop.classList.add('hidden');
            }}
            const nDrop = document.getElementById('dropdown-notifications');
            const nBtn = document.getElementById('btn-notifications');
            if (nDrop && !nDrop.classList.contains('hidden')) {{
                if (nBtn && !nBtn.contains(e.target) && !nDrop.contains(e.target)) nDrop.classList.add('hidden');
            }}
        }});

        async function fetchCurrentUser() {{
            try {{
                const res = await fetch('/api/current-user');
                const data = await res.json();
                currentUserRole = data.role;
                userPermissions = data.permissions;
                const badge = document.getElementById('header-role-badge');
                if (badge && data.permissions && data.permissions.badge) {{
                    badge.innerText = data.permissions.badge;
                }}
            }} catch (e) {{ console.error("Current user error", e); }}
        }}

        async function setSessionRole(newRole) {{
            try {{
                const res = await fetch('/api/switch-role', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ role: newRole }})
                }});
                const data = await res.json();
                if (data.success) {{
                    currentUserRole = data.role;
                    userPermissions = data.permissions;
                    const badge = document.getElementById('header-role-badge');
                    if (badge && data.permissions && data.permissions.badge) badge.innerText = data.permissions.badge;
                    const el = document.getElementById('dropdown-roles');
                    if (el) el.classList.add('hidden');
                    showToast(`Active role: ${{data.role}}`, "success");
                    loadInvoices();
                    loadBills();
                    fetchStats();
                }}
            }} catch (e) {{ showToast("Role switch error", "error"); }}
        }}

        function showPermissionAlert(action, requiredRole) {{
            document.getElementById('perm-denied-action').innerText = action;
            document.getElementById('perm-denied-current-role').innerText = currentUserRole;
            document.getElementById('perm-denied-required-role').innerText = requiredRole;
            openModal('modal-permission-denied');
        }}

        async function fetchStats() {{
            try {{
                const res = await fetch('/api/stats');
                const data = await res.json();
                document.getElementById('stat-outstanding').innerText = formatCurrency(data.total_outstanding);
                document.getElementById('stat-overdue').innerText = formatCurrency(data.overdue_amount);
                document.getElementById('stat-collected').innerText = formatCurrency(data.collected_this_month);
            }} catch (e) {{ console.error("Stats error", e); }}
        }}

        async function loadInvoices() {{
            try {{
                const url = `/api/invoices?status=${{encodeURIComponent(currentStatusFilter)}}&search=${{encodeURIComponent(currentSearchQuery)}}&page=${{currentPage}}&per_page=5`;
                const res = await fetch(url);
                const data = await res.json();

                const tbody = document.getElementById('invoices-table-body');
                tbody.innerHTML = '';
                totalPages = data.total_pages || 1;
                const totalInvs = data.total !== undefined ? data.total : (data.total_count || data.invoices.length);
                document.getElementById('pagination-info').innerText = `Showing ${{data.invoices.length}} of ${{totalInvs}} invoices`;
                document.getElementById('btn-page-prev').disabled = currentPage <= 1;
                document.getElementById('btn-page-next').disabled = currentPage >= totalPages;

                if (!data.invoices || data.invoices.length === 0) {{
                    tbody.innerHTML = `<tr><td colspan="6" class="text-center py-8 text-slate-400">No invoices found matching current filter.</td></tr>`;
                    return;
                }}

                data.invoices.forEach(inv => {{
                    const tr = document.createElement('tr');
                    tr.className = "hover:bg-slate-50 transition border-b border-slate-100";

                    let statusBadge = '';
                    if (inv.is_archived || inv.status === 'Archived') {{
                        statusBadge = `<span class="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold bg-amber-100 text-amber-800 border border-amber-300"><span class="mr-1">🗄️</span>Archived</span>`;
                    }} else if (inv.status === 'Paid') {{
                        statusBadge = `<span class="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold bg-[#0B2E1E] text-[#10B981] border border-[#10B981]/30"><span class="w-1.5 h-1.5 rounded-full bg-[#10B981] mr-1.5"></span>Paid</span>`;
                    }} else if (inv.status === 'Overdue') {{
                        statusBadge = `<span class="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold bg-red-100 text-red-700 border border-red-200">⚠️ Overdue</span>`;
                    }} else if (inv.status === 'Partial') {{
                        statusBadge = `<span class="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold bg-sky-100 text-sky-800 border border-sky-200">⏱ Partial (₱${{Math.round(inv.balance_due/1000)}}k due)</span>`;
                    }} else if (inv.status === 'Draft') {{
                        statusBadge = `<span class="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold bg-slate-100 text-slate-700 border border-slate-300">📄 Draft</span>`;
                    }} else {{
                        statusBadge = `<span class="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200">✉ Sent</span>`;
                    }}

                    let actionControls = '';
                    if (inv.is_archived) {{
                        actionControls = `
                            <div class="inline-flex items-center justify-center space-x-1">
                                <button onclick="restoreInvoice(${{inv.id}}, '${{inv.invoice_number}}')" title="Restore to Active Ledger" class="px-2.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold text-xs transition cursor-pointer">
                                    Restore
                                </button>
                                <button onclick="deleteInvoicePermanent(${{inv.id}}, '${{inv.invoice_number}}')" title="Permanently Delete (CFO Only)" class="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition cursor-pointer">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                </button>
                            </div>
                        `;
                    }} else {{
                        let btn = '';
                        if (inv.status === 'Paid') {{
                            btn = `<button onclick="openInvoiceDetails(${{inv.id}})" class="px-3 py-1.5 bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 rounded-lg font-semibold text-xs transition cursor-pointer">View Details</button>`;
                        }} else if (inv.status === 'Overdue') {{
                            btn = `<button onclick="openReminderModal(${{inv.id}}, '${{inv.invoice_number}}', '${{inv.client_name}}', '${{inv.due_date}}', ${{inv.balance_due}})" class="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold text-xs shadow-sm shadow-red-500/20 transition cursor-pointer">Send Reminder</button>`;
                        }} else {{
                            btn = `<button onclick="openRecordPaymentModal(${{inv.id}}, '${{inv.invoice_number}}', '${{inv.client_name}}', ${{inv.balance_due}})" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold text-xs shadow-sm shadow-blue-500/20 transition cursor-pointer">Record Payment</button>`;
                        }}

                        actionControls = `
                            <div class="inline-flex items-center justify-center space-x-1">
                                ${{btn}}
                                <button onclick="openEditInvoiceModal(${{inv.id}})" title="Edit Invoice (CRUD)" class="p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition cursor-pointer">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                                </button>
                                <button onclick="archiveInvoice(${{inv.id}}, '${{inv.invoice_number}}')" title="Archive Invoice" class="p-1.5 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition cursor-pointer">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"></path></svg>
                                </button>
                            </div>
                        `;
                    }}

                    tr.innerHTML = `
                        <td class="py-4 px-6 font-bold text-slate-800 cursor-pointer hover:text-blue-600" onclick="openInvoiceDetails(${{inv.id}})">${{inv.invoice_number}}</td>
                        <td class="py-4 px-6 text-slate-900 font-semibold">${{inv.client_name}}</td>
                        <td class="py-4 px-6 text-slate-600">${{inv.due_date}}</td>
                        <td class="py-4 px-6 font-bold text-slate-900">${{formatCurrency(inv.total_amount)}}</td>
                        <td class="py-4 px-6">${{statusBadge}}</td>
                        <td class="py-4 px-6 text-center">${{actionControls}}</td>
                    `;
                    tbody.appendChild(tr);
                }});
            }} catch (e) {{ console.error("Load invoices error", e); }}
        }}

        function handleFilterChange(val) {{ currentStatusFilter = val; currentPage = 1; loadInvoices(); }}
        function handleTableSearch(val) {{ currentSearchQuery = val; currentPage = 1; loadInvoices(); }}
        function changePage(p) {{ if (p >= 1 && p <= totalPages) {{ currentPage = p; loadInvoices(); }} }}

        async function archiveInvoice(id, invNumber) {{
            try {{
                const res = await fetch(`/api/invoices/${{id}}/archive`, {{ method: 'POST' }});
                const data = await res.json();
                if (res.status === 403) {{ showPermissionAlert("Archive Invoice", "Financial Analyst or CFO"); return; }}
                if (data.success) {{ showToast(`Invoice ${{invNumber}} moved to archives.`, "warning"); loadInvoices(); fetchStats(); }}
            }} catch (e) {{ showToast("Network error archiving invoice", "error"); }}
        }}

        async function restoreInvoice(id, invNumber) {{
            try {{
                const res = await fetch(`/api/invoices/${{id}}/restore`, {{ method: 'POST' }});
                const data = await res.json();
                if (res.status === 403) {{ showPermissionAlert("Restore Invoice", "Chief Financial Officer"); return; }}
                if (data.success) {{ showToast(`Invoice ${{invNumber}} restored to active ledger.`, "success"); loadInvoices(); fetchStats(); }}
            }} catch (e) {{ showToast("Network error restoring invoice", "error"); }}
        }}

        async function deleteInvoicePermanent(id, invNumber) {{
            if (!confirm(`Permanently delete ${{invNumber}}?`)) return;
            try {{
                const res = await fetch(`/api/invoices/${{id}}`, {{ method: 'DELETE' }});
                const data = await res.json();
                if (res.status === 403) {{ showPermissionAlert("Permanent Delete", "Chief Financial Officer"); return; }}
                if (data.success) {{ showToast(data.message, "success"); loadInvoices(); fetchStats(); }}
            }} catch (e) {{ showToast("Network error deleting invoice", "error"); }}
        }}

        async function openEditInvoiceModal(id) {{
            if (userPermissions && userPermissions.can_edit === false) {{
                showPermissionAlert("Edit Invoice", "Financial Analyst or Chief Financial Officer");
                return;
            }}
            try {{
                const res = await fetch(`/api/invoices/${{id}}`);
                const data = await res.json();
                const inv = data.invoice;
                const items = data.items;

                document.getElementById('edit-invoice-id').value = inv.id;
                document.getElementById('edit-invoice-number-badge').innerText = inv.invoice_number;
                document.getElementById('edit-client-name').value = inv.client_name;
                document.getElementById('edit-client-email').value = inv.client_email || '';
                document.getElementById('edit-due-date').value = inv.due_date;
                document.getElementById('edit-status').value = inv.status;
                document.getElementById('edit-notes').value = inv.notes || '';

                const tbody = document.getElementById('edit-items-tbody');
                tbody.innerHTML = '';
                if (items && items.length > 0) {{
                    items.forEach(it => addEditLineItem(it.description, it.quantity, it.unit_price));
                }} else {{
                    addEditLineItem('General Services', 1, inv.total_amount || 0);
                }}

                calculateEditInvoiceTotal();
                openModal('modal-edit-invoice');
            }} catch (e) {{ showToast("Could not load invoice for editing", "error"); }}
        }}

        function addEditLineItem(desc = '', qty = 1, price = 0) {{
            const tbody = document.getElementById('edit-items-tbody');
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="py-2 px-3"><input type="text" class="edit-item-desc w-full p-1.5 border border-slate-200 rounded text-xs" value="${{desc}}" required></td>
                <td class="py-2 px-3"><input type="number" min="1" class="edit-item-qty w-full p-1.5 border border-slate-200 rounded text-center text-xs" value="${{qty}}" oninput="calculateEditInvoiceTotal()"></td>
                <td class="py-2 px-3"><input type="number" min="0" step="any" class="edit-item-price w-full p-1.5 border border-slate-200 rounded text-right text-xs" value="${{price}}" oninput="calculateEditInvoiceTotal()"></td>
                <td class="py-2 px-3 text-right font-bold text-slate-900 edit-item-total">${{formatCurrency(qty * price)}}</td>
                <td class="py-2 px-2 text-center"><button type="button" onclick="removeEditLineItem(this)" class="text-slate-400 hover:text-red-500 font-bold">×</button></td>
            `;
            tbody.appendChild(tr);
            calculateEditInvoiceTotal();
        }}

        function removeEditLineItem(btn) {{
            const tbody = document.getElementById('edit-items-tbody');
            if (tbody.querySelectorAll('tr').length <= 1) return;
            btn.closest('tr').remove();
            calculateEditInvoiceTotal();
        }}

        function calculateEditInvoiceTotal() {{
            const descs = document.querySelectorAll('.edit-item-desc');
            const qtys = document.querySelectorAll('.edit-item-qty');
            const prices = document.querySelectorAll('.edit-item-price');
            const totals = document.querySelectorAll('.edit-item-total');

            let subtotal = 0;
            for (let i = 0; i < descs.length; i++) {{
                const q = parseFloat(qtys[i].value) || 0;
                const p = parseFloat(prices[i].value) || 0;
                const t = q * p;
                if (totals[i]) totals[i].innerText = formatCurrency(t);
                subtotal += t;
            }}
            const vat = subtotal * 0.12;
            const grand = subtotal + vat;
            document.getElementById('edit-subtotal-display').innerText = formatCurrency(subtotal);
            document.getElementById('edit-vat-display').innerText = formatCurrency(vat);
            document.getElementById('edit-grand-total-display').innerText = formatCurrency(grand);
        }}

        async function handleUpdateInvoice(e) {{
            e.preventDefault();
            const id = document.getElementById('edit-invoice-id').value;
            const clientName = document.getElementById('edit-client-name').value;
            const clientEmail = document.getElementById('edit-client-email').value;
            const dueDate = document.getElementById('edit-due-date').value;
            const status = document.getElementById('edit-status').value;
            const notes = document.getElementById('edit-notes').value;

            const descs = document.querySelectorAll('.edit-item-desc');
            const qtys = document.querySelectorAll('.edit-item-qty');
            const prices = document.querySelectorAll('.edit-item-price');
            const items = [];
            for (let i = 0; i < descs.length; i++) {{
                items.push({{ description: descs[i].value, quantity: parseFloat(qtys[i].value) || 1, unit_price: parseFloat(prices[i].value) || 0 }});
            }}

            try {{
                const res = await fetch(`/api/invoices/${{id}}`, {{
                    method: 'PUT',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ client_name: clientName, client_email: clientEmail, due_date: dueDate, status, notes, items }})
                }});
                const data = await res.json();
                if (res.status === 403) {{ showPermissionAlert("Edit Invoice", "CFO or Financial Analyst"); return; }}
                if (data.success) {{
                    showToast("Invoice updated successfully", "success");
                    closeModal('modal-edit-invoice');
                    loadInvoices();
                    fetchStats();
                }}
            }} catch (err) {{ showToast("Network error updating invoice", "error"); }}
        }}

        function handleArchiveFromEditModal() {{
            const id = document.getElementById('edit-invoice-id').value;
            const num = document.getElementById('edit-invoice-number-badge').innerText;
            closeModal('modal-edit-invoice');
            archiveInvoice(id, num);
        }}

        // Dynamic New Invoice Cart Calculation
        function addNewLineItemRow() {{
            const tbody = document.getElementById('new-invoice-items-tbody');
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="p-2"><input type="text" class="item-desc w-full p-1.5 border border-slate-200 rounded" placeholder="Item description" required></td>
                <td class="p-2"><input type="number" min="1" class="item-qty w-full p-1.5 border border-slate-200 rounded text-center" value="1" oninput="calculateNewInvoiceTotal()"></td>
                <td class="p-2"><input type="number" min="0" step="any" class="item-price w-full p-1.5 border border-slate-200 rounded text-right" value="0" oninput="calculateNewInvoiceTotal()"></td>
                <td class="p-2 text-center"><button type="button" onclick="removeLineItem(this)" class="text-slate-400 hover:text-red-500 font-bold">✕</button></td>
            `;
            tbody.appendChild(tr);
            calculateNewInvoiceTotal();
        }}

        function removeLineItem(btn) {{
            const tbody = document.getElementById('new-invoice-items-tbody');
            if (tbody.querySelectorAll('tr').length <= 1) return;
            btn.closest('tr').remove();
            calculateNewInvoiceTotal();
        }}

        function calculateNewInvoiceTotal() {{
            const descs = document.querySelectorAll('.item-desc');
            const qtys = document.querySelectorAll('.item-qty');
            const prices = document.querySelectorAll('.item-price');
            let sum = 0;
            for (let i = 0; i < descs.length; i++) {{
                sum += (parseFloat(qtys[i].value) || 0) * (parseFloat(prices[i].value) || 0);
            }}
            const vat = sum * 0.12;
            document.getElementById('new-inv-subtotal').innerText = formatCurrency(sum);
            document.getElementById('new-inv-vat').innerText = formatCurrency(vat);
            document.getElementById('new-invoice-total-display').innerText = formatCurrency(sum + vat);
        }}

        async function handleCreateInvoice(e) {{
            e.preventDefault();
            const clientName = document.getElementById('inv-client-name').value;
            const clientEmail = document.getElementById('inv-client-email').value;
            const dueDate = document.getElementById('inv-due-date').value;
            const customNum = document.getElementById('inv-custom-num').value;

            const descs = document.querySelectorAll('.item-desc');
            const qtys = document.querySelectorAll('.item-qty');
            const prices = document.querySelectorAll('.item-price');
            const items = [];
            for (let i = 0; i < descs.length; i++) {{
                items.push({{ description: descs[i].value, quantity: parseFloat(qtys[i].value) || 1, unit_price: parseFloat(prices[i].value) || 0 }});
            }}

            try {{
                const res = await fetch('/api/invoices', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ client_name: clientName, client_email: clientEmail, due_date: dueDate, invoice_number: customNum, items }})
                }});
                const data = await res.json();
                if (res.status === 403) {{ showPermissionAlert("Create Invoice", "Accounting Staff or CFO"); return; }}
                if (data.success) {{
                    showToast(data.message, "success");
                    closeModal('modal-new-invoice');
                    document.getElementById('form-new-invoice').reset();
                    loadInvoices();
                    fetchStats();
                }}
            }} catch (err) {{ showToast("Network error creating invoice", "error"); }}
        }}

        function openNewInvoiceModal() {{
            if (userPermissions && userPermissions.can_create === false) {{
                showPermissionAlert("Create New Invoice", "Student Staff, Financial Analyst, or Chief Financial Officer");
                return;
            }}
            openModal('modal-new-invoice');
        }}

        function openRecordPaymentModal(id, num, client, balance) {{
            if (userPermissions && userPermissions.can_record_payment === false) {{
                showPermissionAlert("Record Payment", "Financial Analyst or Chief Financial Officer");
                return;
            }}
            document.getElementById('pay-invoice-id').value = id;
            document.getElementById('pay-invoice-num').value = `${{client}} (${{num}})`;
            document.getElementById('pay-amount').value = balance;
            openModal('modal-record-payment');
        }}

        async function handleRecordPaymentSubmit(e) {{
            e.preventDefault();
            const id = document.getElementById('pay-invoice-id').value;
            const amount = parseFloat(document.getElementById('pay-amount').value);
            const method = document.getElementById('pay-method').value;
            const ref = document.getElementById('pay-ref').value;

            try {{
                const res = await fetch(`/api/invoices/${{id}}/payment`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ amount, payment_method: method, reference_no: ref }})
                }});
                const data = await res.json();
                if (res.status === 403) {{ showPermissionAlert("Record Payment", "Financial Analyst or CFO"); return; }}
                if (data.success) {{
                    showToast(data.message, "success");
                    closeModal('modal-record-payment');
                    loadInvoices();
                    fetchStats();
                }}
            }} catch (err) {{ showToast("Error recording payment", "error"); }}
        }}

        function openReminderModal(id, num, client, due, balance) {{
            document.getElementById('reminder-invoice-id').value = id;
            document.getElementById('reminder-client-name').value = `${{client}} (${{num}})`;
            document.getElementById('reminder-body-preview').value = `Formal Collection Notice\\n\\nDear Finance Desk at ${{client}},\\n\\nThis notice concerns Invoice ${{num}} for ${{formatCurrency(balance)}} due on ${{due}}.\\nKindly arrange prompt wire transfer.\\n\\nAlex Rivera, CFO\\nAcme Global Inc.`;
            openModal('modal-send-reminder');
        }}

        async function executeSendReminder() {{
            const id = document.getElementById('reminder-invoice-id').value;
            try {{
                const res = await fetch(`/api/invoices/${{id}}/reminder`, {{ method: 'POST' }});
                const data = await res.json();
                if (data.success) {{
                    showToast(data.message, "success");
                    closeModal('modal-send-reminder');
                }}
            }} catch (e) {{ showToast("Failed to dispatch notice", "error"); }}
        }}

        async function openInvoiceDetails(id) {{
            try {{
                const res = await fetch(`/api/invoices/${{id}}`);
                const data = await res.json();
                const inv = data.invoice;
                const items = data.items;

                document.getElementById('detail-invoice-badge').innerText = inv.invoice_number;
                let rowsHtml = items.map(it => `
                    <tr class="border-b border-slate-100">
                        <td class="py-2">${{it.description}}</td>
                        <td class="py-2 text-center">${{it.quantity}}</td>
                        <td class="py-2 text-right">${{formatCurrency(it.unit_price)}}</td>
                        <td class="py-2 text-right font-bold">${{formatCurrency(it.total)}}</td>
                    </tr>
                `).join('');

                document.getElementById('detail-modal-body').innerHTML = `
                    <div class="flex justify-between border-b pb-3">
                        <div><h2 class="text-lg font-extrabold text-blue-600">LedgerCraft PRO Voucher</h2><p class="text-[10px] text-slate-500">Delaware Reg #492810 · GAAP Certified</p></div>
                        <div class="text-right font-bold">${{inv.invoice_number}}<p class="text-slate-500 text-[10px]">Due: ${{inv.due_date}}</p></div>
                    </div>
                    <div class="py-2">
                        <span class="text-[10px] uppercase font-bold text-slate-400">Billed To:</span>
                        <h4 class="font-bold text-slate-800">${{inv.client_name}}</h4>
                    </div>
                    <table class="w-full text-left text-xs border-t border-b border-slate-200 mt-2">
                        <thead class="text-slate-400 text-[10px] uppercase font-bold"><tr><th>Item</th><th class="text-center">Qty</th><th class="text-right">Price</th><th class="text-right">Total</th></tr></thead>
                        <tbody>${{rowsHtml}}</tbody>
                    </table>
                    <div class="flex justify-end pt-2 text-right space-y-1">
                        <div>
                            <div class="text-slate-600">Subtotal: ${{formatCurrency(inv.subtotal)}}</div>
                            <div class="text-slate-600">VAT (12%): ${{formatCurrency(inv.tax || inv.subtotal*0.12)}}</div>
                            <div class="text-blue-600 font-extrabold text-sm pt-1 border-t">Total: ${{formatCurrency(inv.total_amount)}}</div>
                            <div class="text-emerald-600 font-semibold">Settled: ${{formatCurrency(inv.paid_amount)}}</div>
                            <div class="text-red-600 font-bold">Balance: ${{formatCurrency(inv.balance_due)}}</div>
                        </div>
                    </div>
                    <div class="mt-4 pt-3 border-t border-slate-200 flex justify-between">
                        <div class="space-x-1">
                            <button onclick="closeModal('modal-view-details'); openEditInvoiceModal(${{inv.id}})" class="px-3 py-1.5 bg-blue-50 text-blue-700 rounded font-semibold text-xs">✎ Edit</button>
                            <button onclick="closeModal('modal-view-details'); archiveInvoice(${{inv.id}}, '${{inv.invoice_number}}')" class="px-3 py-1.5 bg-amber-50 text-amber-700 rounded font-semibold text-xs">🗄️ Archive</button>
                        </div>
                        <div class="space-x-1">
                            <button onclick="window.print()" class="px-3 py-1.5 bg-slate-100 text-slate-700 rounded text-xs font-semibold">Print PDF</button>
                            <button onclick="closeModal('modal-view-details')" class="px-3 py-1.5 bg-slate-900 text-white rounded text-xs font-bold">Done</button>
                        </div>
                    </div>
                `;
                openModal('modal-view-details');
            }} catch (e) {{ showToast("Could not load voucher", "error"); }}
        }}

        async function triggerFifoMatch() {{
            try {{
                const res = await fetch('/api/fifo-match', {{ method: 'POST' }});
                const data = await res.json();
                showToast("⚡ FIFO Auto-match engine reconciled outstanding receivables!", "success");
                loadInvoices();
                fetchStats();
            }} catch (e) {{ showToast("Reconciliation engine error", "error"); }}
        }}

        async function loadBills() {{
            try {{
                const res = await fetch('/api/bills');
                const data = await res.json();
                const tbody = document.getElementById('bills-table-body');
                tbody.innerHTML = '';
                data.bills.forEach(b => {{
                    const tr = document.createElement('tr');
                    tr.className = "hover:bg-slate-50 border-b border-slate-100";
                    tr.innerHTML = `
                        <td class="py-3 px-6 font-bold text-slate-800">${{b.bill_number}}</td>
                        <td class="py-3 px-6 font-semibold">${{b.vendor_name}}</td>
                        <td class="py-3 px-6 text-slate-600">${{b.category}}</td>
                        <td class="py-3 px-6 text-slate-600">${{b.due_date}}</td>
                        <td class="py-3 px-6 font-bold text-slate-900">${{formatCurrency(b.amount)}}</td>
                        <td class="py-3 px-6"><span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${{b.status==='Paid'?'bg-emerald-100 text-emerald-800':'bg-amber-100 text-amber-800'}}">${{b.status}}</span></td>
                        <td class="py-3 px-6 text-center">${{b.status==='Unpaid'?`<button onclick="payBill(${{b.id}},'${{b.bill_number}}')" class="px-3 py-1 bg-blue-600 text-white rounded text-xs font-semibold">Pay Bill</button>`:'<span class="text-slate-400 font-bold">Settled</span>'}}</td>
                    `;
                    tbody.appendChild(tr);
                }});
            }} catch (e) {{ console.error("Bills error", e); }}
        }}

        async function payBill(id, num) {{
            try {{
                const res = await fetch(`/api/bills/${{id}}/pay`, {{ method: 'POST' }});
                const data = await res.json();
                if (res.status === 403) {{ showPermissionAlert("Pay Bill", "Chief Financial Officer"); return; }}
                if (data.success) {{ showToast(`Disbursed ${{num}}`, "success"); loadBills(); }}
            }} catch (e) {{ showToast("Error paying bill", "error"); }}
        }}

        function switchTab(t) {{
            currentTab = t;
            const ar = document.getElementById('view-ar-container');
            const ap = document.getElementById('view-ap-container');
            const rep = document.getElementById('view-reports-container');
            const btnAr = document.getElementById('tab-btn-ar');
            const btnAp = document.getElementById('tab-btn-ap');

            rep.classList.add('hidden');
            if (t === 'ar') {{
                ar.classList.remove('hidden');
                ap.classList.add('hidden');
                btnAr.className = "px-4 py-2 bg-blue-600 text-white rounded-lg text-xs font-bold shadow-sm transition";
                btnAp.className = "px-4 py-2 bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 rounded-lg text-xs font-semibold transition";
                loadInvoices();
            }} else {{
                ar.classList.add('hidden');
                ap.classList.remove('hidden');
                btnAp.className = "px-4 py-2 bg-blue-600 text-white rounded-lg text-xs font-bold shadow-sm transition";
                btnAr.className = "px-4 py-2 bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 rounded-lg text-xs font-semibold transition";
                loadBills();
            }}
        }}

        async function showAuditTrail() {{
            try {{
                const res = await fetch('/api/audit-trail');
                const data = await res.json();
                document.getElementById('view-ar-container').classList.add('hidden');
                document.getElementById('view-ap-container').classList.add('hidden');
                const rep = document.getElementById('view-reports-container');
                rep.classList.remove('hidden');

                let rows = data.logs.map(l => `
                    <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg flex items-center justify-between text-xs">
                        <div><span class="font-bold text-slate-800">${{l.action}}</span> · <span class="text-slate-600">${{l.details}}</span><div class="text-[10px] text-slate-400">By: ${{l.user_name}}</div></div>
                        <span class="text-[10px] font-mono text-slate-400">${{l.timestamp}}</span>
                    </div>
                `).join('');

                document.getElementById('reports-content-box').innerHTML = `
                    <div class="flex items-center justify-between mb-4 border-b pb-3">
                        <h3 class="text-base font-bold text-slate-900">Immutable Audit Trail</h3>
                        <button onclick="switchTab('ar')" class="text-xs px-3 py-1 bg-slate-100 rounded font-semibold text-slate-700">Back</button>
                    </div>
                    <div class="space-y-2">${{rows}}</div>
                `;
            }} catch (e) {{ showToast("Could not load audit trail", "error"); }}
        }}

        async function showJournalEntries() {{
            try {{
                const res = await fetch('/api/journal-entries');
                const data = await res.json();
                document.getElementById('view-ar-container').classList.add('hidden');
                document.getElementById('view-ap-container').classList.add('hidden');
                const rep = document.getElementById('view-reports-container');
                rep.classList.remove('hidden');

                let rows = data.entries.map(e => `
                    <tr class="border-b border-slate-100 text-xs hover:bg-slate-50">
                        <td class="py-2.5 px-4 font-mono font-bold text-blue-600">${{e.entry_number}}</td>
                        <td class="py-2.5 px-4 text-slate-600">${{e.date}}</td>
                        <td class="py-2.5 px-4 font-semibold text-slate-800">${{e.account_name}}</td>
                        <td class="py-2.5 px-4 text-slate-500">${{e.description}}</td>
                        <td class="py-2.5 px-4 text-right font-bold">${{e.debit ? formatCurrency(e.debit) : '-'}}</td>
                        <td class="py-2.5 px-4 text-right font-bold">${{e.credit ? formatCurrency(e.credit) : '-'}}</td>
                    </tr>
                `).join('');

                document.getElementById('reports-content-box').innerHTML = `
                    <div class="flex items-center justify-between mb-4 border-b pb-3">
                        <h3 class="text-base font-bold text-slate-900">General Ledger Journal Entries</h3>
                        <button onclick="switchTab('ar')" class="text-xs px-3 py-1 bg-slate-100 rounded font-semibold text-slate-700">Back</button>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs">
                            <thead class="bg-slate-50 text-slate-500 text-[10px] font-bold">
                                <tr><th class="py-2 px-4">ENTRY #</th><th class="py-2 px-4">DATE</th><th class="py-2 px-4">ACCOUNT</th><th class="py-2 px-4">DESCRIPTION</th><th class="py-2 px-4 text-right">DEBIT (₱)</th><th class="py-2 px-4 text-right">CREDIT (₱)</th></tr>
                            </thead>
                            <tbody>${{rows}}</tbody>
                        </table>
                    </div>
                `;
            }} catch (e) {{ showToast("Could not load journal entries", "error"); }}
        }}

        async function syncAdminState() {{
            try {{
                const res = await fetch('/api/admin/sync');
                const data = await res.json();
                if (data.sync_status === 'live_synced') {{
                    const dot = document.getElementById('live-sync-indicator');
                    if (dot) {{ dot.classList.add('opacity-30'); setTimeout(() => dot.classList.remove('opacity-30'), 400); }}
                    if (data.stats) {{
                        const outEl = document.getElementById('stat-outstanding');
                        const ovEl = document.getElementById('stat-overdue');
                        const colEl = document.getElementById('stat-collected');
                        if (outEl) outEl.innerText = formatCurrency(data.stats.total_outstanding);
                        if (ovEl) ovEl.innerText = formatCurrency(data.stats.overdue_amount);
                        if (colEl) colEl.innerText = formatCurrency(data.stats.collected_this_month);
                    }}
                }}
            }} catch (e) {{}}
        }}

        function handleLogout() {{
            if (confirm("Sign out of LedgerCraft PRO?")) {{
                showToast("Signing out...", "warning");
                setTimeout(() => window.location.href = '/logout', 500);
            }}
        }}

        function showToast(message, type = 'info') {{
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            let bgClass = "bg-slate-900 text-white";
            let icon = "ℹ";
            if (type === 'success') {{ bgClass = "bg-emerald-600 text-white"; icon = "✓"; }}
            else if (type === 'error') {{ bgClass = "bg-red-600 text-white"; icon = "⚠️"; }}
            else if (type === 'warning') {{ bgClass = "bg-amber-600 text-white"; icon = "!"; }}

            toast.className = `${{bgClass}} px-4 py-3 rounded-xl shadow-xl flex items-center space-x-2 text-xs font-semibold pointer-events-auto transform transition duration-300 translate-y-2 opacity-0 max-w-sm`;
            toast.innerHTML = `<span class="text-sm font-bold">${{icon}}</span><span>${{message}}</span>`;
            container.appendChild(toast);
            setTimeout(() => toast.classList.remove('translate-y-2', 'opacity-0'), 10);
            setTimeout(() => {{
                toast.classList.add('opacity-0', 'translate-y-2');
                setTimeout(() => toast.remove(), 300);
            }}, 4000);
        }}
    </script>
</body>
</html>
"""
