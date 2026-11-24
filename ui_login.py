# -*- coding: utf-8 -*-
"""
LedgerCraft PRO - Pure Python Login View
100% Template-Free Architecture
"""

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - LedgerCraft</title>
    <!-- Tailwind CSS (Offline Local + CDN Fallback) -->
    <script src="/static/js/tailwindcss.js"></script>
    <script>
        if (!window.tailwind) {
            document.write('<script src="https://cdn.tailwindcss.com"><\/script>');
        }
    </script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        darknavy: {
                            950: '#030712',
                            900: '#060B18',
                            850: '#080E21',
                            800: '#0B132B',
                            700: '#142045'
                        }
                    },
                    fontFamily: {
                        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
                    }
                }
            }
        };
    </script>
    <!-- Prevent FOUC: Immediate theme restoration before rendering -->
    <script>
        (function() {
            try {
                var saved = localStorage.getItem('ledgercraft_theme');
                var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
                if (saved === 'dark' || (!saved && prefersDark)) {
                    document.documentElement.classList.add('dark');
                } else {
                    document.documentElement.classList.remove('dark');
                }
            } catch (e) {}
        })();
    </script>
    <!-- Google Fonts: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background-color: #060B18;
        }
        .tree-node-active {
            border-color: #3B82F6 !important;
            background-color: rgba(59, 130, 246, 0.15) !important;
            color: #93C5FD !important;
        }
        .tree-node-error {
            border-color: #EF4444 !important;
            background-color: rgba(239, 68, 68, 0.15) !important;
            color: #FCA5A5 !important;
        }
        .tree-node-success {
            border-color: #10B981 !important;
            background-color: rgba(16, 185, 129, 0.15) !important;
            color: #6EE7B7 !important;
        }

        /* ================= DARK THEME STYLES ================= */
        html.dark header.bg-white,
        html.dark header {
            background-color: #0B132B !important;
            border-color: #1E293B !important;
            color: #F8FAFC !important;
        }
        html.dark header a {
            color: #CBD5E1 !important;
        }
        html.dark header a:hover {
            color: #60A5FA !important;
        }
        html.dark #btn-theme-toggle {
            color: #FBBF24 !important;
            background-color: #1E293B !important;
            border-color: #334155 !important;
        }
        html.dark #btn-theme-toggle:hover {
            background-color: #2D3E64 !important;
            color: #FDE047 !important;
        }
        html.dark .bg-white {
            background-color: #0F172A !important;
        }
        html.dark .border-slate-200 {
            border-color: #1E293B !important;
        }
        html.dark .text-slate-900,
        html.dark .text-slate-800 {
            color: #F8FAFC !important;
        }
        html.dark .text-slate-700 {
            color: #E2E8F0 !important;
        }
        html.dark .text-slate-600 {
            color: #CBD5E1 !important;
        }
    </style>
</head>
<body class="min-h-screen text-slate-100 flex flex-col bg-[#060B18] antialiased overflow-x-hidden">

    <!-- ================= TOP HEADER (WHITE BAR MATCHING REFERENCE) ================= -->
    <header class="h-14 sm:h-16 px-4 sm:px-8 lg:px-12 xl:px-16 flex items-center justify-between bg-white border-b border-slate-200 z-20 flex-shrink-0 w-full text-slate-800 shadow-xs">
        <!-- Left: Blue Rounded Icon + Brand Name "LedgerCraft" -->
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

        <!-- Right: Links, Theme Toggle & Blue Register Pill Button -->
        <div class="flex items-center space-x-3 sm:space-x-5 text-xs sm:text-[13px]">
            <a href="#" onclick="openHelpdeskModal()" class="text-slate-700 hover:text-blue-600 font-medium transition cursor-pointer">
                Campus Helpdesk
            </a>
            <a href="#" onclick="openFaqModal()" class="text-slate-700 hover:text-blue-600 font-medium transition cursor-pointer">
                FAQ
            </a>
            <!-- Dark / Light Theme Toggle -->
            <button id="btn-theme-toggle" onclick="toggleTheme()" class="p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer border border-transparent hover:border-slate-200" title="Toggle Light / Dark Mode" aria-label="Toggle Theme">
                <svg id="theme-icon-sun" class="w-5 h-5 hidden text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
                </svg>
                <svg id="theme-icon-moon" class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
                </svg>
            </button>
            <button type="button" onclick="openRegisterModal()" class="inline-flex items-center justify-center bg-[#007CB9] hover:bg-[#006A9F] text-white font-bold text-xs px-5 py-2 rounded-full transition shadow-sm cursor-pointer hover:shadow-md">
                Register
            </button>
        </div>
    </header>

    <!-- ================= FULL-SCREEN SPLIT MAIN VIEWPORT ================= -->
    <main class="flex-1 w-full grid grid-cols-1 lg:grid-cols-12 min-h-[calc(100vh-4rem)] p-0 m-0 border-0 bg-[#060B18]">
        
        <!-- ================= LEFT COLUMN: HERO WITH FINANCIAL CHART GRAPHICS ================= -->
        <div class="lg:col-span-7 xl:col-span-7 2xl:col-span-7 p-8 sm:p-12 lg:p-16 xl:p-20 2xl:p-24 flex flex-col justify-between relative overflow-hidden w-full text-slate-100 border-b lg:border-b-0 lg:border-r border-slate-800/80">
            
            <!-- Financial Chart Graphic SVG Overlay (Matches Reference) -->
            <svg class="absolute inset-0 w-full h-full pointer-events-none opacity-45" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
                        <path d="M 48 0 L 0 0 0 48" fill="none" stroke="rgba(255, 255, 255, 0.035)" stroke-width="1"/>
                    </pattern>
                    <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#2563EB" stop-opacity="0.2"/>
                        <stop offset="40%" stop-color="#3B82F6" stop-opacity="0.8"/>
                        <stop offset="70%" stop-color="#60A5FA" stop-opacity="0.95"/>
                        <stop offset="100%" stop-color="#93C5FD" stop-opacity="0.4"/>
                    </linearGradient>
                    <linearGradient id="areaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.12"/>
                        <stop offset="100%" stop-color="#3B82F6" stop-opacity="0.0"/>
                    </linearGradient>
                    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="3" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                </defs>
                <rect width="100%" height="100%" fill="url(#grid)" />
                <!-- Area Fill -->
                <path d="M 0 420 Q 90 440, 160 360 T 310 300 T 460 390 T 610 230 T 760 290 T 900 160 L 900 700 L 0 700 Z" fill="url(#areaGrad)" />
                <!-- Chart Line -->
                <path d="M 0 420 Q 90 440, 160 360 T 310 300 T 460 390 T 610 230 T 760 290 T 900 160" fill="none" stroke="url(#lineGrad)" stroke-width="2.5" filter="url(#glow)" />
                <!-- Chart Connecting Data Points -->
                <circle cx="160" cy="360" r="4.5" fill="#60A5FA" stroke="#1E40AF" stroke-width="2" />
                <circle cx="310" cy="300" r="5" fill="#93C5FD" stroke="#2563EB" stroke-width="2.5" filter="url(#glow)" />
                <circle cx="460" cy="390" r="4.5" fill="#60A5FA" stroke="#1E40AF" stroke-width="2" />
                <circle cx="610" cy="230" r="5.5" fill="#BFDBFE" stroke="#3B82F6" stroke-width="2.5" filter="url(#glow)" />
                <circle cx="760" cy="290" r="4.5" fill="#60A5FA" stroke="#1E40AF" stroke-width="2" />
                <circle cx="900" cy="160" r="5" fill="#DBEAFE" stroke="#60A5FA" stroke-width="2.5" filter="url(#glow)" />
            </svg>

            <!-- Content Area -->
            <div class="max-w-2xl relative z-10">
                <!-- Top pill badge matching reference -->
                <div class="inline-flex items-center space-x-2 bg-[#0B1530]/90 backdrop-blur-md border border-blue-500/30 text-[#60A5FA] text-[10px] sm:text-[11px] font-bold uppercase tracking-wider px-3.5 py-1.5 rounded-full">
                    <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                    <span>TREASURY &amp; LEDGER OPERATIONS</span>
                </div>

                <!-- Main headline matching reference line wrapping -->
                <h1 class="text-3xl sm:text-4xl lg:text-[46px] xl:text-[52px] font-extrabold text-white tracking-tight leading-[1.12] mt-6 sm:mt-8">
                    Smart financial orchestration<br>
                    for high-velocity teams.
                </h1>

                <!-- Paragraph matching reference -->
                <p class="text-slate-300 text-xs sm:text-sm lg:text-base mt-4 sm:mt-5 max-w-xl leading-relaxed font-normal">
                    Unify journal reconciliations, real-time A/R tracking, and automated cashflows in one secure operating system.
                </p>
            </div>

            <!-- Bottom 3 Metric Cards matching reference -->
            <div class="grid grid-cols-3 gap-3 sm:gap-4 lg:gap-5 pt-10 sm:pt-14 mt-auto max-w-2xl relative z-10">
                
                <!-- Metric 1: Matched Invoices -->
                <div class="bg-[#0B132B]/90 backdrop-blur-md p-4 sm:p-5 rounded-2xl border border-slate-800/90 shadow-xl">
                    <span class="text-[9px] sm:text-[10px] uppercase font-bold text-slate-400 tracking-wider block">MATCHED INVOICES</span>
                    <div class="text-xl sm:text-2xl lg:text-3xl font-extrabold text-white mt-1 tracking-tight">99.8%</div>
                    <div class="text-[10px] sm:text-[11px] text-emerald-400 font-semibold mt-0.5">Realtime FIFO match</div>
                </div>

                <!-- Metric 2: Ledger Velocity -->
                <div class="bg-[#0B132B]/90 backdrop-blur-md p-4 sm:p-5 rounded-2xl border border-slate-800/90 shadow-xl">
                    <span class="text-[9px] sm:text-[10px] uppercase font-bold text-slate-400 tracking-wider block">LEDGER VELOCITY</span>
                    <div class="text-xl sm:text-2xl lg:text-3xl font-extrabold text-white mt-1 tracking-tight">&lt; 120ms</div>
                    <div class="text-[10px] sm:text-[11px] text-blue-400 font-semibold mt-0.5">Sub-second posting</div>
                </div>

                <!-- Metric 3: Enterprise Ready -->
                <div class="bg-[#0B132B]/90 backdrop-blur-md p-4 sm:p-5 rounded-2xl border border-slate-800/90 shadow-xl">
                    <span class="text-[9px] sm:text-[10px] uppercase font-bold text-slate-400 tracking-wider block">ENTERPRISE READY</span>
                    <div class="text-xl sm:text-2xl lg:text-3xl font-extrabold text-white mt-1 tracking-tight">SOC 2</div>
                    <div class="text-[10px] sm:text-[11px] text-slate-400 font-medium mt-0.5">Type II certified</div>
                </div>

            </div>

        </div>

        <!-- ================= RIGHT COLUMN: DARK WORKSPACE (MATCHING REFERENCE) ================= -->
        <div class="lg:col-span-5 xl:col-span-5 2xl:col-span-5 bg-[#060B18] p-8 sm:p-12 lg:p-14 xl:p-16 2xl:p-20 flex flex-col justify-center items-center w-full text-slate-100">
            
            <div class="w-full max-w-[420px] my-auto">
                
                <!-- Rejection Alert Notification (Lesson 6 Academic Branch Diagnostic) -->
                <div id="rejection-alert" class="hidden mb-4 p-3.5 rounded-xl border border-red-500/50 bg-red-950/70 text-red-200 text-xs shadow-lg">
                    <div class="flex items-start space-x-2">
                        <span class="text-red-400 font-bold text-sm">⚠</span>
                        <div class="flex-1">
                            <h5 id="alert-title" class="font-bold text-red-300 text-xs">Rejection Alert: Access Denied</h5>
                            <p id="alert-message" class="text-[11px] text-red-200 mt-0.5 font-medium">Invalid credentials provided.</p>
                            <span id="alert-branch" class="text-[10px] font-mono text-red-400 block mt-1">Decision Branch: Evaluation Failed</span>
                        </div>
                    </div>
                </div>

                <!-- Success Alert Notification -->
                <div id="success-alert" class="hidden mb-4 p-3.5 rounded-xl border border-emerald-500/50 bg-emerald-950/70 text-emerald-200 text-xs shadow-lg">
                    <div class="flex items-center space-x-2">
                        <span class="text-emerald-400 font-bold text-sm">✓</span>
                        <div>
                            <h5 class="font-bold text-emerald-300 text-xs">Authentication Successful</h5>
                            <p id="success-message" class="text-[11px] text-emerald-200 mt-0.5 font-medium">Token Generated. Redirecting to Treasury Dashboard...</p>
                        </div>
                    </div>
                </div>

                <!-- Main Login Form -->
                <form id="login-form" onsubmit="handleLoginSubmit(event)" class="space-y-4 text-xs">
                    
                    <!-- WORK EMAIL ADDRESS Field (White Input Box Matching Reference) -->
                    <div>
                        <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-300 mb-2">
                            WORK EMAIL ADDRESS
                        </label>
                        <div class="relative bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex items-center transition focus-within:ring-2 focus-within:ring-blue-500">
                            <span class="pl-3.5 pr-2 text-slate-400 flex items-center pointer-events-none select-none">
                                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.206"></path>
                                </svg>
                            </span>
                            <input type="text" id="input-username" required placeholder="name@institution.edu" class="w-full bg-white text-slate-900 font-medium py-3 pr-4 text-sm focus:outline-none placeholder-slate-400">
                        </div>
                    </div>

                    <!-- PASSWORD Field (White Input Box Matching Reference) -->
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <label class="text-[11px] font-bold uppercase tracking-wider text-slate-300">
                                PASSWORD
                            </label>
                            <a href="#" onclick="showForgotPasswordAlert()" class="text-xs font-semibold text-sky-400 hover:text-sky-300 transition">
                                Forgot password?
                            </a>
                        </div>
                        <div class="relative bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex items-center transition focus-within:ring-2 focus-within:ring-blue-500">
                            <span class="pl-3.5 pr-2 text-slate-400 flex items-center pointer-events-none select-none">
                                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke-width="2"></rect>
                                    <path d="M7 11V7a5 5 0 0110 0v4" stroke-width="2"></path>
                                </svg>
                            </span>
                            <input type="password" id="input-password" required placeholder="••••••••••••" class="w-full bg-white text-slate-900 font-medium py-3 pr-2 text-sm focus:outline-none placeholder-slate-400">
                            <button type="button" onclick="togglePasswordVisibility()" class="pr-3.5 pl-2 text-slate-400 hover:text-slate-600 transition cursor-pointer">
                                <svg id="eye-icon" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <!-- Remember Workstation Checkbox -->
                    <div class="flex items-center space-x-2 py-1">
                        <input type="checkbox" id="remember-me" checked class="w-4 h-4 rounded border-slate-700 bg-slate-900 text-blue-600 focus:ring-blue-500 cursor-pointer accent-blue-600">
                        <label for="remember-me" class="text-xs text-slate-300 font-normal cursor-pointer select-none">
                            Remember this workstation for 30 days
                        </label>
                    </div>

                    <!-- Primary Submit Button -->
                    <button type="submit" id="btn-submit" class="w-full py-3.5 px-4 bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm rounded-xl shadow-lg shadow-blue-600/30 flex items-center justify-center space-x-2 transition mt-2 cursor-pointer">
                        <span id="btn-text">Sign In to Workspace</span>
                        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                        </svg>
                        <svg id="btn-spinner" class="hidden w-4 h-4 animate-spin text-white ml-2" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                        </svg>
                    </button>
                </form>

                <!-- Divider matching reference: "OR CONTINUE WITH EMAIL" -->
                <div class="relative flex items-center justify-center my-6">
                    <div class="border-t border-slate-800 w-full"></div>
                    <span class="bg-[#060B18] px-3 text-[10px] uppercase font-bold text-slate-500 tracking-wider whitespace-nowrap">
                        OR CONTINUE WITH EMAIL
                    </span>
                    <div class="border-t border-slate-800 w-full"></div>
                </div>

                <!-- Secondary Button: Continue with Okta / SSO (Dark Button Matching Reference) -->
                <button type="button" onclick="handleSsoClick()" class="w-full flex items-center justify-center space-x-3 py-3 px-4 bg-[#0B132B]/80 hover:bg-[#121c3b] text-slate-200 border border-slate-800 rounded-xl font-semibold text-xs sm:text-sm transition shadow-sm mb-6 cursor-pointer">
                    <!-- Multi-color Google G icon -->
                    <svg class="w-4 h-4" viewBox="0 0 24 24">
                        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
                    </svg>
                    <span>Continue with Okta / SSO</span>
                </button>

                <!-- Footer Encryption Text Matching Reference -->
                <p class="text-center text-[11px] text-slate-500">
                    Protected by enterprise-grade TLS 1.3 encryption &amp; multi-factor validation.
                </p>

                <!-- Helper Links: Quick Demo & Process Tree (Preserves Academic Rubric Testing) -->
                <div class="mt-6 pt-4 border-t border-slate-900 flex items-center justify-between text-[11px] text-slate-500">
                    <button type="button" onclick="fillDemoCredentials('alex', 'password123')" class="text-blue-400 font-semibold hover:underline cursor-pointer">
                        ⚡ Quick Fill Demo: Alex Rivera
                    </button>
                    <button type="button" onclick="toggleProcessTreeModal()" class="text-slate-500 font-medium hover:text-slate-300 hover:underline cursor-pointer flex items-center space-x-1">
                        <span>🌲 Lesson 6 Process Tree</span>
                    </button>
                </div>

            </div>

        </div>

    </main>

    <!-- ================= REGISTRATION POP-UP MODAL ================= -->
    <div id="modal-register" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm" onclick="closeRegisterModal()"></div>
        <div class="relative bg-white rounded-2xl border border-slate-200 max-w-md w-full p-6 sm:p-7 m-4 z-10 shadow-2xl text-xs flex flex-col text-slate-800">
            
            <!-- Header -->
            <div class="flex items-center justify-between pb-4 border-b border-slate-200">
                <div class="flex items-center space-x-2.5">
                    <div class="w-7 h-7 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-xs">
                        LC
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-slate-900 leading-tight">Register LedgerCraft Account</h3>
                        <p class="text-[11px] text-slate-500">Create credentials to sign in to the workspace</p>
                    </div>
                </div>
                <button type="button" onclick="closeRegisterModal()" class="text-slate-400 hover:text-slate-600 p-1 rounded-lg">✕</button>
            </div>

            <!-- Register Form -->
            <form id="form-register" onsubmit="handleRegisterSubmit(event)" class="mt-4 space-y-3.5 text-xs">
                <div id="register-error-box" class="hidden p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-[11px]"></div>

                <div>
                    <label class="block text-slate-700 font-semibold mb-1">Full Name *</label>
                    <input type="text" id="reg-fullname" required placeholder="e.g. Juan Dela Cruz" class="w-full bg-slate-50 border border-slate-300 text-slate-900 rounded-xl px-3.5 py-2 text-xs focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none">
                </div>

                <div class="grid grid-cols-2 gap-2.5">
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1">Username *</label>
                        <input type="text" id="reg-username" required placeholder="e.g. jdelacruz" class="w-full bg-slate-50 border border-slate-300 text-slate-900 rounded-xl px-3.5 py-2 text-xs focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1">Work / Institution Email</label>
                        <input type="email" id="reg-email" placeholder="e.g. jdelacruz@institution.edu" class="w-full bg-slate-50 border border-slate-300 text-slate-900 rounded-xl px-3.5 py-2 text-xs focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none">
                    </div>
                </div>

                <div>
                    <label class="block text-slate-700 font-semibold mb-1">Password *</label>
                    <input type="password" id="reg-password" required placeholder="••••••••••••" class="w-full bg-slate-50 border border-slate-300 text-slate-900 rounded-xl px-3.5 py-2 text-xs focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none">
                </div>

                <div>
                    <label class="block text-slate-700 font-semibold mb-1">Account Role</label>
                    <select id="reg-role" class="w-full bg-slate-50 border border-slate-300 text-slate-900 rounded-xl px-3.5 py-2 text-xs focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none">
                        <option value="User">User (Submit Bills & Invoices)</option>
                        <option value="Accounting Staff">Accounting Staff (Monitor & Archive)</option>
                        <option value="Admin">Admin (Full Access & Account Management)</option>
                    </select>
                </div>

                <div class="pt-3 border-t border-slate-200 flex items-center justify-end space-x-2.5">
                    <button type="button" onclick="closeRegisterModal()" class="px-4 py-2 border border-slate-200 text-slate-600 rounded-xl hover:bg-slate-100 transition">Cancel</button>
                    <button type="submit" id="btn-register-submit" class="px-5 py-2 bg-[#007CB9] hover:bg-[#006A9F] text-white font-bold rounded-xl shadow-md shadow-blue-500/20 transition">Register & Pre-fill Login</button>
                </div>
            </form>
        </div>
    </div>

    <!-- ================= LESSON 6 DECISION TREE MODAL ================= -->
    <div id="modal-process-tree" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm" onclick="toggleProcessTreeModal()"></div>
        <div class="relative bg-[#0B132B] rounded-2xl border border-slate-800 max-w-2xl w-full p-6 m-4 z-10 shadow-2xl max-h-[90vh] overflow-y-auto text-xs text-slate-200">
            
            <div class="flex items-center justify-between pb-3 border-b border-slate-800">
                <div class="flex items-center space-x-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                    <h3 class="text-base font-bold text-white">Lesson 6: Login Validation & Verification Process Tree</h3>
                </div>
                <button onclick="toggleProcessTreeModal()" class="text-slate-400 hover:text-white p-1">✕</button>
            </div>

            <p class="text-slate-400 text-xs mt-2 mb-4">
                Flowchart decision tree reflecting Academic Exercise NO. 16-20. The backend automatically executes each branch when credentials are submitted.
            </p>

            <div class="space-y-3 font-mono text-[11px]">
                <div class="p-3 bg-slate-900/80 border border-slate-700 rounded-lg flex items-center justify-between">
                    <div>
                        <span class="text-blue-400 font-bold">Node 1: Credential Submission / Input</span>
                        <div class="text-slate-400">Captures work email/username and plaintext password via HTTPS</div>
                    </div>
                    <span class="bg-blue-950 text-blue-300 px-2 py-0.5 rounded border border-blue-800">Step 16</span>
                </div>

                <div class="text-center text-slate-600">↓</div>

                <div class="p-3 bg-slate-900/80 border border-slate-700 rounded-lg flex items-center justify-between">
                    <div>
                        <span class="text-blue-400 font-bold">Node 2: Database User Search</span>
                        <div class="text-slate-400">SELECT * FROM users WHERE username = ? OR email = ?</div>
                    </div>
                    <span class="bg-blue-950 text-blue-300 px-2 py-0.5 rounded border border-blue-800">Step 17</span>
                </div>

                <div class="text-center text-slate-600">↓</div>

                <div class="p-3 bg-slate-900/80 border border-slate-700 rounded-lg">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-amber-400 font-bold">Node 3: User Existence Decision Branch (Yes / No)</span>
                        <span class="bg-amber-950 text-amber-300 px-2 py-0.5 rounded border border-amber-800">Step 18</span>
                    </div>
                    <div class="grid grid-cols-2 gap-2 text-[10px]">
                        <div class="p-2 rounded bg-red-950/40 border border-red-900/40 text-red-300">
                            <strong>Branch: NO</strong> → Rejection Alert dispatched
                        </div>
                        <div class="p-2 rounded bg-emerald-950/40 border border-emerald-900/40 text-emerald-300">
                            <strong>Branch: YES</strong> → Proceed to Hash Verification
                        </div>
                    </div>
                </div>

                <div class="text-center text-slate-600">↓ (if YES)</div>

                <div class="p-3 bg-slate-900/80 border border-slate-700 rounded-lg flex items-center justify-between">
                    <div>
                        <span class="text-indigo-400 font-bold">Node 4: Password Hash Verification</span>
                        <div class="text-slate-400">Evaluates check_password_hash(stored_hash, submitted_password)</div>
                    </div>
                    <span class="bg-indigo-950 text-indigo-300 px-2 py-0.5 rounded border border-indigo-800">Step 19</span>
                </div>

                <div class="text-center text-slate-600">↓</div>

                <div class="p-3 bg-slate-900/80 border border-slate-700 rounded-lg">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-amber-400 font-bold">Node 5: Password Validity Branch (Valid / Invalid)</span>
                        <span class="bg-amber-950 text-amber-300 px-2 py-0.5 rounded border border-amber-800">Step 19</span>
                    </div>
                    <div class="grid grid-cols-2 gap-2 text-[10px]">
                        <div class="p-2 rounded bg-red-950/40 border border-red-900/40 text-red-300">
                            <strong>Branch: INVALID</strong> → Rejection Alert dispatched
                        </div>
                        <div class="p-2 rounded bg-emerald-950/40 border border-emerald-900/40 text-emerald-300">
                            <strong>Branch: VALID</strong> → Authorize for token generation
                        </div>
                    </div>
                </div>

                <div class="text-center text-slate-600">↓</div>

                <div class="p-3 bg-slate-900/80 border border-slate-700 rounded-lg">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-emerald-400 font-bold">Node 6: Token Generation & Dashboard Redirection vs. Rejection Alert</span>
                        <span class="bg-emerald-950 text-emerald-300 px-2 py-0.5 rounded border border-emerald-800">Step 20</span>
                    </div>
                    <div class="text-slate-400 text-[10px]">
                        • If Valid: Generates 256-bit crypto session token, logs to audit trail, redirects to /<br>
                        • If Invalid: Displays diagnostic Rejection Alert on form
                    </div>
                </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 text-right">
                <button onclick="toggleProcessTreeModal()" class="px-4 py-1.5 bg-blue-600 text-white rounded-lg font-bold text-xs hover:bg-blue-500">Close</button>
            </div>
        </div>
    </div>

    <!-- JAVASCRIPT AUTHENTICATION & MODAL CONTROLLER -->
    <script>
        function fillDemoCredentials(u, p) {
            document.getElementById('input-username').value = u;
            document.getElementById('input-password').value = p;
            hideAlerts();
        }

        function togglePasswordVisibility() {
            const pass = document.getElementById('input-password');
            pass.type = pass.type === 'password' ? 'text' : 'password';
        }

        function hideAlerts() {
            document.getElementById('rejection-alert').classList.add('hidden');
            document.getElementById('success-alert').classList.add('hidden');
        }

        function toggleProcessTreeModal() {
            const modal = document.getElementById('modal-process-tree');
            modal.classList.toggle('hidden');
        }

        function openRegisterModal() {
            document.getElementById('register-error-box').classList.add('hidden');
            document.getElementById('modal-register').classList.remove('hidden');
        }

        function closeRegisterModal() {
            document.getElementById('modal-register').classList.add('hidden');
        }

        async function handleRegisterSubmit(e) {
            e.preventDefault();
            const errBox = document.getElementById('register-error-box');
            errBox.classList.add('hidden');

            const fullName = document.getElementById('reg-fullname').value.trim();
            const username = document.getElementById('reg-username').value.trim();
            const email = document.getElementById('reg-email').value.trim();
            const password = document.getElementById('reg-password').value;
            const role = document.getElementById('reg-role').value;

            const btn = document.getElementById('btn-register-submit');
            btn.disabled = true;
            btn.innerText = "Registering Account...";

            try {
                const res = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        full_name: fullName,
                        username: username,
                        email: email,
                        password: password,
                        role: role
                    })
                });

                const data = await res.json();

                if (!res.ok || !data.success) {
                    errBox.innerText = data.message || "Registration failed. Please check inputs.";
                    errBox.classList.remove('hidden');
                } else {
                    closeRegisterModal();

                    // Pre-fill login inputs
                    document.getElementById('input-username').value = data.username;
                    document.getElementById('input-password').value = password;

                    // Show success alert on login box
                    const successBox = document.getElementById('success-alert');
                    document.getElementById('success-message').innerText = `Account '${data.username}' registered successfully! Credentials pre-filled below. Click 'Sign In to Workspace' to log in.`;
                    successBox.classList.remove('hidden');

                    // Pop up notification alert
                    alert(`Registration Successful!\n\nYour account has been registered into the LedgerCraft directory:\n\n• Name: ${fullName}\n• Username: ${username}\n• Email: ${email || username + '@institution.edu'}\n\nYour credentials have been pre-filled into the login form. Click 'Sign In to Workspace' to proceed.`);
                }
            } catch (err) {
                console.error("Registration error", err);
                errBox.innerText = "Network error connecting to registration endpoint.";
                errBox.classList.remove('hidden');
            } finally {
                btn.disabled = false;
                btn.innerText = "Register & Pre-fill Login";
            }
        }

        function openHelpdeskModal() {
            alert("LedgerCraft Campus Helpdesk\n\nFor IT Elective, Student Portal, and LMS Support:\nPortal: https://one.sti.edu\nEmail: helpdesk@institution.edu\nHotline: (02) 8887-8447");
        }

        function openFaqModal() {
            alert("LedgerCraft FAQ:\n\n1. What is this portal?\nOfficial LedgerCraft PRO Financial OS & IT Elective Treasury System.\n\n2. How do I log in?\nUse your registered account credentials or demo: alex / password123 (or Brichang123 / 123456789).");
        }

        function handleSsoClick() {
            fillDemoCredentials('alex.rivera@acmeglobal.com', 'password123');
            alert("SSO simulation: Pre-filled Enterprise Okta credentials for Alex Rivera (CFO). Click 'Sign In to Workspace' to authenticate.");
        }

        function showForgotPasswordAlert() {
            alert("Contact Acme Global Corporate IT / Security Administrator: security@acmeglobal.com for password reset.");
        }

        async function handleLoginSubmit(e) {
            e.preventDefault();
            hideAlerts();

            const username = document.getElementById('input-username').value.trim();
            const password = document.getElementById('input-password').value;

            const btnText = document.getElementById('btn-text');
            const btnSpinner = document.getElementById('btn-spinner');
            const btnSubmit = document.getElementById('btn-submit');

            btnText.innerText = "Authenticating...";
            btnSpinner.classList.remove('hidden');
            btnSubmit.disabled = true;

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (!response.ok) {
                    const alertBox = document.getElementById('rejection-alert');
                    document.getElementById('alert-title').innerText = "Rejection Alert: Access Denied";
                    document.getElementById('alert-message').innerText = data.message || "Invalid credentials provided.";
                    
                    let branchInfo = "Evaluation Node: Input Validation";
                    if (data.failed_step === 'user_existence') {
                        branchInfo = "Decision Branch 3: User Existence = NO";
                    } else if (data.failed_step === 'password_validity') {
                        branchInfo = "Decision Branch 5: Password Validity = INVALID";
                    }
                    document.getElementById('alert-branch').innerText = branchInfo;
                    alertBox.classList.remove('hidden');
                } else {
                    const successBox = document.getElementById('success-alert');
                    document.getElementById('success-message').innerText = `Welcome, ${data.user.full_name} (${data.user.role}). Token issued. Launching workspace...`;
                    successBox.classList.remove('hidden');

                    setTimeout(() => {
                        window.location.href = data.redirect || '/';
                    }, 800);
                }
            } catch (err) {
                console.error("Login request error", err);
                const alertBox = document.getElementById('rejection-alert');
                document.getElementById('alert-title').innerText = "Communication Failure";
                document.getElementById('alert-message').innerText = "Unable to connect to Treasury Authentication Gateway.";
                document.getElementById('alert-branch').innerText = "Network Error";
                alertBox.classList.remove('hidden');
            } finally {
                btnSpinner.classList.add('hidden');
                btnSubmit.disabled = false;
                btnText.innerText = "Sign In to Workspace";
            }
        }

        // ==================== THEME CONTROLLER (DARK / LIGHT MODE) ====================
        function applyTheme(theme) {
            const isDark = theme === 'dark';
            if (isDark) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
            try {
                localStorage.setItem('ledgercraft_theme', theme);
            } catch (e) {}

            const sunIcons = document.querySelectorAll('#theme-icon-sun');
            const moonIcons = document.querySelectorAll('#theme-icon-moon');
            sunIcons.forEach(icon => icon.classList.toggle('hidden', !isDark));
            moonIcons.forEach(icon => icon.classList.toggle('hidden', isDark));
        }

        function toggleTheme() {
            const isDark = document.documentElement.classList.contains('dark');
            applyTheme(isDark ? 'light' : 'dark');
        }

        function initTheme() {
            let saved = null;
            try {
                saved = localStorage.getItem('ledgercraft_theme');
            } catch (e) {}
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            const theme = saved || (prefersDark ? 'dark' : 'light');
            applyTheme(theme);
        }

        document.addEventListener('DOMContentLoaded', initTheme);
        initTheme();
    </script>
</body>
</html>
"""

def render_login_view() -> str:
    """Returns the pure Python LedgerCraft login view."""
    return LOGIN_HTML
