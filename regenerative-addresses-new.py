#!/usr/bin/env python3
"""
Regenerative Addresses Tool - Rebuilt Version
A GUI tool for generating and regenerating various types of addresses
Educational and legitimate security testing purposes only
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import random
import string
import ipaddress
import re
from datetime import datetime, timedelta
import hashlib
import uuid
import os
import urllib.request
import json
import base64
import time
import threading
import subprocess
import getpass
import platform
import sys
import webbrowser
from pathlib import Path

# Import existing modules
try:
    from kali_credential_obtainer import KaliCredentialObtainer
    from auto_updater import AutoUpdater
    from proxy_manager import ProxyManager
except ImportError as e:
    print(f"Warning: Could not import module: {e}")
    KaliCredentialObtainer = None
    AutoUpdater = None
    ProxyManager = None

class RegenerativeAddressesTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Regenerative Addresses Tool v2.0")
        self.root.geometry("1000x750")
        self.root.configure(bg='#2b2b2b')
        
        # Session management
        self.current_user = None
        self.session_start = None
        self.session_timeout = 300  # 5 minutes
        
        # Initialize components
        self.setup_styles()
        self.load_proxies()
        self.initialize_components()
        
        # Create main interface
        self.create_main_interface()
        
        # Show login screen
        self.show_login()

    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Dark.TFrame', background='#2b2b2b')
        style.configure('Light.TFrame', background='#3c3c3c')
        style.configure('Header.TLabel', background='#1a1a1a', foreground='white', font=('Arial', 12, 'bold'))
        style.configure('Title.TLabel', background='#2b2b2b', foreground='#00ff00', font=('Arial', 14, 'bold'))
        style.configure('Info.TLabel', background='#2b2b2b', foreground='#ffffff', font=('Arial', 10))
        style.configure('Success.TLabel', background='#2b2b2b', foreground='#00ff00', font=('Arial', 10))
        style.configure('Error.TLabel', background='#2b2b2b', foreground='#ff0000', font=('Arial', 10))
        style.configure('Dark.TButton', background='#4a4a4a', foreground='white')
        style.configure('Primary.TButton', background='#007acc', foreground='white')
        style.configure('Success.TButton', background='#28a745', foreground='white')
        style.configure('Warning.TButton', background='#ffc107', foreground='black')
        style.configure('Danger.TButton', background='#dc3545', foreground='white')

    def initialize_components(self):
        """Initialize all components"""
        # Initialize Kali credential obtainer
        if KaliCredentialObtainer:
            self.kali_obtainer = KaliCredentialObtainer()
        else:
            self.kali_obtainer = None
        
        # Initialize auto-updater
        if AutoUpdater:
            self.updater = AutoUpdater(current_version="2.0.0")
        else:
            self.updater = None
        
        # Initialize proxy manager
        if ProxyManager:
            self.proxy_manager = ProxyManager()
        else:
            self.proxy_manager = None
            self.proxies = []
        
        # Initialize HTML storage
        self.stored_html = ""

    def load_proxies(self):
        """Load proxy lists from files"""
        self.proxies = []
        proxy_files = [
            'all_proxies.txt', 'proxies.txt', 'https_proxies.txt',
            'socks4_proxies.txt', 'socks5_proxies.txt'
        ]
        
        for proxy_file in proxy_files:
            if os.path.exists(proxy_file):
                try:
                    with open(proxy_file, 'r') as f:
                        file_proxies = [line.strip() for line in f if line.strip()]
                        self.proxies.extend(file_proxies)
                except Exception as e:
                    print(f"Error loading {proxy_file}: {e}")

    def create_main_interface(self):
        """Create the main interface"""
        # Main container
        self.main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.create_header()
        
        # Content area
        self.content_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Status bar
        self.create_status_bar()

    def create_header(self):
        """Create header section"""
        header_frame = ttk.Frame(self.main_frame, style='Light.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = ttk.Label(header_frame, text="Regenerative Addresses Tool", style='Title.TLabel')
        title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # User info
        self.user_info_label = ttk.Label(header_frame, text="", style='Info.TLabel')
        self.user_info_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Logout button (hidden initially)
        self.logout_btn = ttk.Button(header_frame, text="Logout", command=self.logout, style='Danger.TButton')
        self.logout_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    def create_status_bar(self):
        """Create status bar"""
        status_frame = ttk.Frame(self.main_frame, style='Light.TFrame')
        status_frame.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Info.TLabel')
        status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Version info
        version_label = ttk.Label(status_frame, text="v2.0.0", style='Info.TLabel')
        version_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def show_login(self):
        """Show login interface"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Login container
        login_container = ttk.Frame(self.content_frame, style='Light.TFrame')
        login_container.pack(expand=True)
        
        # Login form
        login_frame = ttk.LabelFrame(login_container, text="Login", padding="20")
        login_frame.pack(pady=20)
        
        # Username
        ttk.Label(login_frame, text="Username:", style='Info.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(login_frame, text="Password:", style='Info.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(login_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Login", command=self.login, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Register", command=self.show_register, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Focus on username
        self.username_entry.focus()

    def show_register(self):
        """Show registration interface"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Register container
        register_container = ttk.Frame(self.content_frame, style='Light.TFrame')
        register_container.pack(expand=True)
        
        # Register form
        register_frame = ttk.LabelFrame(register_container, text="Register", padding="20")
        register_frame.pack(pady=20)
        
        # Username
        ttk.Label(register_frame, text="Username:", style='Info.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.reg_username_entry = ttk.Entry(register_frame, width=30)
        self.reg_username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(register_frame, text="Password:", style='Info.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_password_entry = ttk.Entry(register_frame, width=30, show="*")
        self.reg_password_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Confirm Password
        ttk.Label(register_frame, text="Confirm Password:", style='Info.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reg_confirm_entry = ttk.Entry(register_frame, width=30, show="*")
        self.reg_confirm_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(register_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Register", command=self.register, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Back to Login", command=self.show_login, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Focus on username
        self.reg_username_entry.focus()

    def show_main_interface(self):
        """Show main application interface"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create tabbed interface
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Link Regenerator Tab
        self.create_link_tab(notebook)
        
        # Proxy Manager Tab
        self.create_proxy_tab(notebook)
        
        # Kali Tools Tab
        self.create_kali_tab(notebook)
        
        # HTML Processor Tab
        self.create_html_tab(notebook)
        
        # Settings Tab
        self.create_settings_tab(notebook)

    def create_link_tab(self, notebook):
        """Create link regenerator tab"""
        link_frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(link_frame, text="Link Regenerator")
        
        # Input section
        input_frame = ttk.LabelFrame(link_frame, text="Link Input", padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Original URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.link_entry = ttk.Entry(input_frame, width=60)
        self.link_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Technique selection
        ttk.Label(input_frame, text="Technique:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.technique_var = tk.StringVar(value="add_parameters")
        technique_combo = ttk.Combobox(input_frame, textvariable=self.technique_var, width=25)
        technique_combo['values'] = [
            "add_parameters", "change_subdomain", "add_path_segments",
            "change_tld", "add_tracking_params", "shorten_url_style", "affiliate_style"
        ]
        technique_combo.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Options
        self.use_proxy_var = tk.BooleanVar()
        proxy_check = ttk.Checkbutton(input_frame, text="Use Proxy", variable=self.use_proxy_var)
        proxy_check.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Button(button_frame, text="Regenerate", command=self.regenerate_link, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Batch Generate", command=self.batch_generate, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        
        # Results section
        results_frame = ttk.LabelFrame(link_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80, bg='#1a1a1a', fg='white')
        self.results_text.pack(fill=tk.BOTH, expand=True)

    def create_proxy_tab(self, notebook):
        """Create proxy manager tab"""
        proxy_frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(proxy_frame, text="Proxy Manager")
        
        # Proxy controls
        control_frame = ttk.LabelFrame(proxy_frame, text="Proxy Controls", padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="Test Proxies", command=self.test_proxies, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Load Proxies", command=self.load_proxies, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Export Proxies", command=self.export_proxies, style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        
        # Proxy list
        list_frame = ttk.LabelFrame(proxy_frame, text="Available Proxies", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.proxy_listbox = tk.Listbox(list_frame, bg='#1a1a1a', fg='white', height=20)
        self.proxy_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Load existing proxies
        self.update_proxy_list()

    def create_kali_tab(self, notebook):
        """Create Kali tools tab"""
        kali_frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(kali_frame, text="Kali Tools")
        
        if not self.kali_obtainer:
            ttk.Label(kali_frame, text="Kali tools not available", style='Error.TLabel').pack(pady=20)
            return
        
        # Tool selection
        tool_frame = ttk.LabelFrame(kali_frame, text="Available Tools", padding="10")
        tool_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tools = [
            ("nmap", "Network Scanning"),
            ("hydra", "Password Testing"),
            ("john", "Password Cracking"),
            ("hashcat", "Hash Recovery"),
            ("sqlmap", "SQL Injection Testing"),
            ("responder", "Network Security"),
            ("crunch", "Wordlist Generation")
        ]
        
        for i, (tool, description) in enumerate(tools):
            btn = ttk.Button(tool_frame, text=f"{tool} - {description}", 
                           command=lambda t=tool: self.run_kali_tool(t), style='Primary.TButton')
            btn.pack(fill=tk.X, pady=2)
        
        # Results area
        results_frame = ttk.LabelFrame(kali_frame, text="Tool Output", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.kali_results = scrolledtext.ScrolledText(results_frame, height=15, width=80, bg='#1a1a1a', fg='white')
        self.kali_results.pack(fill=tk.BOTH, expand=True)

    def create_html_tab(self, notebook):
        """Create HTML processor tab"""
        html_frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(html_frame, text="HTML Processor")
        
        # HTML input
        input_frame = ttk.LabelFrame(html_frame, text="HTML Input", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.html_input = scrolledtext.ScrolledText(input_frame, height=20, width=80, bg='#1a1a1a', fg='white')
        self.html_input.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Process HTML", command=self.process_html, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_html, style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load from File", command=self.load_html_file, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        
        # Results area
        results_frame = ttk.LabelFrame(html_frame, text="Analysis Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.html_results = scrolledtext.ScrolledText(results_frame, height=10, width=80, bg='#1a1a1a', fg='white')
        self.html_results.pack(fill=tk.BOTH, expand=True)

    def create_settings_tab(self, notebook):
        """Create settings tab"""
        settings_frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(settings_frame, text="Settings")
        
        # Settings sections
        sections = [
            ("General Settings", ["session_timeout", "debug_mode"]),
            ("Security Settings", ["csrf_protection", "rate_limiting"]),
            ("Proxy Settings", ["auto_rotate", "check_interval"]),
            ("Update Settings", ["auto_update", "update_channel"])
        ]
        
        for section_name, settings in sections:
            section_frame = ttk.LabelFrame(settings_frame, text=section_name, padding="10")
            section_frame.pack(fill=tk.X, padx=10, pady=10)
            
            for setting in settings:
                var = tk.BooleanVar(value=True)
                check = ttk.Checkbutton(section_frame, text=f"Enable {setting}", variable=var)
                check.pack(anchor=tk.W, pady=2)
        
        # PHP Integration
        php_frame = ttk.LabelFrame(settings_frame, text="PHP Integration", padding="10")
        php_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(php_frame, text="Open PHP Admin Panel", command=self.open_php_panel, style='Primary.TButton').pack(pady=5)
        ttk.Button(php_frame, text="Check PHP Status", command=self.check_php_status, style='Success.TButton').pack(pady=5)
        
        # About section
        about_frame = ttk.LabelFrame(settings_frame, text="About", padding="10")
        about_frame.pack(fill=tk.X, padx=10, pady=10)
        
        about_text = """
Regenerative Addresses Tool v2.0.0

Educational security testing and link regeneration tool.

Features:
- Link regeneration with multiple techniques
- Proxy management and testing
- Kali Linux tools integration
- HTML processing and analysis
- PHP web interface integration

Educational Purpose Only
        """
        
        ttk.Label(about_frame, text=about_text.strip(), style='Info.TLabel').pack(pady=10)

    def login(self):
        """Handle user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        # Simple authentication (in production, use proper hashing)
        if self.authenticate_user(username, password):
            self.current_user = username
            self.session_start = time.time()
            self.show_main_interface()
            self.update_user_info()
            self.status_var.set(f"Logged in as {username}")
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.status_var.set("Login failed")

    def register(self):
        """Handle user registration"""
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        confirm = self.reg_confirm_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        # Save user (in production, use proper hashing and storage)
        if self.save_user(username, password):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login()
        else:
            messagebox.showerror("Error", "Username already exists")

    def logout(self):
        """Handle user logout"""
        self.current_user = None
        self.session_start = None
        self.show_login()
        self.status_var.set("Logged out")

    def authenticate_user(self, username, password):
        """Authenticate user"""
        try:
            users_file = 'users.json'
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    users = json.load(f)
                    return username in users and users[username] == password
        except Exception:
            pass
        
        # Default admin account
        return username == "admin" and password == "admin"

    def save_user(self, username, password):
        """Save new user"""
        try:
            users_file = 'users.json'
            users = {}
            
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    users = json.load(f)
            
            if username in users:
                return False
            
            users[username] = password
            
            with open(users_file, 'w') as f:
                json.dump(users, f, indent=2)
            
            return True
        except Exception:
            return False

    def update_user_info(self):
        """Update user info display"""
        if self.current_user:
            session_time = int(time.time() - self.session_start) if self.session_start else 0
            self.user_info_label.config(text=f"User: {self.current_user} | Session: {session_time}s")
            self.logout_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        else:
            self.user_info_label.config(text="")
            self.logout_btn.pack_forget()

    def regenerate_link(self):
        """Regenerate a link"""
        original_url = self.link_entry.get().strip()
        technique = self.technique_var.get()
        use_proxy = self.use_proxy_var.get()
        
        if not original_url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        try:
            regenerated_url = self.apply_technique(original_url, technique)
            
            proxy_info = ""
            if use_proxy and self.proxies:
                proxy = random.choice(self.proxies)
                proxy_info = f" (Proxy: {proxy})"
            
            result = f"Original: {original_url}\n"
            result += f"Technique: {technique}\n"
            result += f"Regenerated: {regenerated_url}\n"
            result += f"Proxy: {'Yes' + proxy_info if use_proxy else 'No'}\n"
            result += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            result += "-" * 60 + "\n"
            
            self.results_text.insert(tk.END, result)
            self.results_text.see(tk.END)
            
            self.status_var.set(f"Link regenerated using {technique}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to regenerate link: {str(e)}")

    def apply_technique(self, url, technique):
        """Apply regeneration technique to URL"""
        if technique == "add_parameters":
            return self.add_parameters(url)
        elif technique == "change_subdomain":
            return self.change_subdomain(url)
        elif technique == "add_path_segments":
            return self.add_path_segments(url)
        elif technique == "change_tld":
            return self.change_tld(url)
        elif technique == "add_tracking_params":
            return self.add_tracking_params(url)
        elif technique == "shorten_url_style":
            return self.shorten_url_style(url)
        elif technique == "affiliate_style":
            return self.affiliate_style(url)
        else:
            return url

    def add_parameters(self, url):
        """Add tracking parameters"""
        params = [
            f"utm_source={self.random_string(8)}",
            f"utm_medium={self.random_string(6)}",
            f"utm_campaign={self.random_string(10)}"
        ]
        separator = '&' if '?' in url else '?'
        return url + separator + '&'.join(params)

    def change_subdomain(self, url):
        """Change subdomain"""
        subdomains = ['www', 'm', 'mobile', 'app', 'api', 'secure', 'shop', 'blog']
        new_subdomain = random.choice(subdomains)
        
        if '://' in url:
            parts = url.split('://')
            domain_parts = parts[1].split('.')
            if len(domain_parts) > 2:
                domain_parts[0] = new_subdomain
                return parts[0] + '://' + '.'.join(domain_parts)
        return url

    def add_path_segments(self, url):
        """Add random path segments"""
        segments = [
            self.random_string(8),
            self.random_string(12)
        ]
        return url.rstrip('/') + '/' + '/'.join(segments)

    def change_tld(self, url):
        """Change top-level domain"""
        tlds = ['.com', '.net', '.org', '.info', '.biz', '.co', '.io', '.me']
        if '://' in url:
            parts = url.split('://')
            domain_parts = parts[1].split('.')
            if len(domain_parts) > 1:
                current_tld = '.' + domain_parts[-1]
                new_tld = random.choice([t for t in tlds if t != current_tld])
                domain_parts[-1] = new_tld.lstrip('.')
                return parts[0] + '://' + '.'.join(domain_parts)
        return url

    def add_tracking_params(self, url):
        """Add tracking parameters"""
        tracking_id = self.random_string(8)
        session_id = self.random_string(16)
        
        params = [
            f"tid={tracking_id}",
            f"sid={session_id}",
            f"ts={int(time.time())}"
        ]
        separator = '&' if '?' in url else '?'
        return url + separator + '&'.join(params)

    def shorten_url_style(self, url):
        """Convert to shortened URL style"""
        short_code = self.random_string(6)
        return f"https://short.ly/{short_code}"

    def affiliate_style(self, url):
        """Convert to affiliate URL style"""
        affiliate_id = self.random_string(8)
        separator = '&' if '?' in url else '?'
        return url + separator + f"affiliate_id={affiliate_id}&ref=aff"

    def batch_generate(self):
        """Generate multiple link variations"""
        original_url = self.link_entry.get().strip()
        if not original_url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        techniques = [
            "add_parameters", "change_subdomain", "add_path_segments",
            "change_tld", "add_tracking_params", "shorten_url_style", "affiliate_style"
        ]
        
        result = f"Batch Generation for: {original_url}\n"
        result += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += "-" * 60 + "\n"
        
        for i, technique in enumerate(techniques, 1):
            regenerated = self.apply_technique(original_url, technique)
            result += f"{i}. {technique}: {regenerated}\n"
        
        result += "-" * 60 + "\n"
        
        self.results_text.insert(tk.END, result)
        self.results_text.see(tk.END)
        
        self.status_var.set(f"Generated {len(techniques)} link variations")

    def test_proxies(self):
        """Test proxy functionality"""
        if not self.proxies:
            messagebox.showinfo("Info", "No proxies available")
            return
        
        self.status_var.set("Testing proxies...")
        
        def test_thread():
            working_proxies = []
            test_count = min(10, len(self.proxies))
            
            for i in range(test_count):
                proxy = self.proxies[i]
                # Simple connectivity test
                if self.test_proxy_connectivity(proxy):
                    working_proxies.append(proxy)
            
            result = f"Proxy Test Results:\n"
            result += f"Tested: {test_count} proxies\n"
            result += f"Working: {len(working_proxies)} proxies\n"
            result += f"Success Rate: {len(working_proxies)/test_count*100:.1f}%\n"
            result += "-" * 60 + "\n"
            
            if working_proxies:
                result += "Working Proxies:\n"
                for proxy in working_proxies[:5]:
                    result += f"  - {proxy}\n"
            
            self.proxy_listbox.delete(0, tk.END)
            for proxy in working_proxies:
                self.proxy_listbox.insert(tk.END, proxy)
            
            self.results_text.insert(tk.END, result)
            self.results_text.see(tk.END)
            
            self.status_var.set(f"Proxy test complete: {len(working_proxies)} working")
        
        threading.Thread(target=test_thread, daemon=True).start()

    def test_proxy_connectivity(self, proxy):
        """Test proxy connectivity (simplified)"""
        try:
            import socket
            if ':' in proxy:
                host, port = proxy.rsplit(':', 1)
                port = int(port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((host, port))
                sock.close()
                return result == 0
        except Exception:
            pass
        return False

    def update_proxy_list(self):
        """Update proxy list display"""
        self.proxy_listbox.delete(0, tk.END)
        for proxy in self.proxies[:50]:  # Show first 50
            self.proxy_listbox.insert(tk.END, proxy)

    def export_proxies(self):
        """Export working proxies"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    for proxy in self.proxies:
                        f.write(proxy + '\n')
                messagebox.showinfo("Success", f"Proxies exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export proxies: {str(e)}")

    def run_kali_tool(self, tool):
        """Run Kali tool (educational demonstration)"""
        if not self.kali_obtainer:
            messagebox.showerror("Error", "Kali tools not available")
            return
        
        self.status_var.set(f"Running {tool} demonstration...")
        
        def tool_thread():
            try:
                # Demonstrate tool usage (educational only)
                result = self.kali_obtainer.demonstrate_tool_usage(tool)
                
                output = f"Tool: {tool}\n"
                output += f"Command: {result.get('command', 'N/A')}\n"
                output += f"Description: {result.get('explanation', 'N/A')}\n"
                output += f"Educational Note: {result.get('educational_note', 'N/A')}\n"
                output += "-" * 60 + "\n"
                
                self.kali_results.insert(tk.END, output)
                self.kali_results.see(tk.END)
                
                self.status_var.set(f"{tool} demonstration complete")
                
            except Exception as e:
                error_msg = f"Error running {tool}: {str(e)}"
                self.kali_results.insert(tk.END, error_msg + "\n")
                self.kali_results.see(tk.END)
                self.status_var.set(f"Error with {tool}")
        
        threading.Thread(target=tool_thread, daemon=True).start()

    def process_html(self):
        """Process HTML content"""
        html_content = self.html_input.get(1.0, tk.END).strip()
        
        if not html_content:
            messagebox.showerror("Error", "Please enter HTML content")
            return
        
        # Store HTML content
        self.stored_html = html_content
        
        # Analyze HTML
        analysis = self.analyze_html(html_content)
        
        result = f"HTML Analysis Results:\n"
        result += f"Length: {len(html_content)} characters\n"
        result += f"Lines: {len(html_content.splitlines())} lines\n"
        result += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += "-" * 60 + "\n"
        result += "Structure Analysis:\n"
        
        for key, value in analysis.items():
            result += f"  {key}: {value}\n"
        
        result += "-" * 60 + "\n"
        result += "HTML content stored for further processing.\n"
        
        self.html_results.insert(tk.END, result)
        self.html_results.see(tk.END)
        
        self.status_var.set("HTML content processed and stored")

    def analyze_html(self, html_content):
        """Analyze HTML structure"""
        analysis = {
            'doctype': 'DOCTYPE' in html_content.upper(),
            'html_tags': html_content.lower().count('<html'),
            'head_tags': html_content.lower().count('<head'),
            'body_tags': html_content.lower().count('<body'),
            'table_tags': html_content.lower().count('<table'),
            'script_tags': html_content.lower().count('<script'),
            'iframe_tags': html_content.lower().count('<iframe'),
            'forms': html_content.lower().count('<form'),
            'inputs': html_content.lower().count('<input'),
            'links': html_content.lower().count('<a '),
            'external_links': html_content.lower().count('http'),
            'javascript_events': html_content.lower().count('onclick'),
        }
        return analysis

    def clear_html(self):
        """Clear HTML input and results"""
        self.html_input.delete(1.0, tk.END)
        self.html_results.delete(1.0, tk.END)
        self.stored_html = ""
        self.status_var.set("HTML cleared")

    def load_html_file(self):
        """Load HTML from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("HTML files", "*.html"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.html_input.delete(1.0, tk.END)
                self.html_input.insert(1.0, content)
                self.status_var.set(f"Loaded {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def open_php_panel(self):
        """Open PHP admin panel"""
        try:
            # Try to open local PHP panel
            php_url = "http://localhost/regenerative-addresses/src"
            webbrowser.open(php_url)
            self.status_var.set("Opening PHP admin panel...")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PHP panel: {str(e)}")

    def check_php_status(self):
        """Check PHP integration status"""
        php_path = "/home/kali/Desktop/hello/src"
        
        status = "PHP Integration Status:\n"
        status += "-" * 60 + "\n"
        
        if os.path.exists(php_path):
            status += "✓ PHP directory exists\n"
            
            php_files = [
                'view.php', 'model.php', 'goat.php', 'controller.php',
                'config/config.php', 'controllers/errors.php',
                'helpers/AuthHelper.php', 'models/User.php'
            ]
            
            for php_file in php_files:
                full_path = os.path.join(php_path, php_file)
                if os.path.exists(full_path):
                    status += f"✓ {php_file}\n"
                else:
                    status += f"✗ {php_file}\n"
        else:
            status += "✗ PHP directory not found\n"
        
        status += "-" * 60 + "\n"
        status += "Note: PHP integration requires web server setup\n"
        status += "Use 'python -m http.server 8000' in src directory\n"
        
        self.html_results.insert(tk.END, status)
        self.html_results.see(tk.END)
        self.status_var.set("PHP status check complete")

    def random_string(self, length=8):
        """Generate random string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def check_session_timeout(self):
        """Check session timeout"""
        if self.current_user and self.session_start:
            if time.time() - self.session_start > self.session_timeout:
                self.logout()
                messagebox.showwarning("Session Expired", "Your session has expired. Please login again.")
                return False
        return True

    def run(self):
        """Main application loop"""
        def update_loop():
            if self.check_session_timeout():
                self.update_user_info()
            self.root.after(1000, update_loop)
        
        update_loop()
        self.root.mainloop()

def main():
    """Main function"""
    root = tk.Tk()
    app = RegenerativeAddressesTool(root)
    app.run()

if __name__ == "__main__":
    main()
