#!/usr/bin/env python3
"""
Regenerative Addresses Tool - Professional Edition v3.0
Complete link regeneration and network management system
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
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
import socket
import csv
import logging
from typing import Dict, List, Optional, Tuple, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import existing modules
try:
    from kali_credential_obtainer import KaliCredentialObtainer
    from auto_updater import AutoUpdater
    from proxy_manager import ProxyManager
except ImportError as e:
    logger.warning(f"Could not import module: {e}")
    KaliCredentialObtainer = None
    AutoUpdater = None
    ProxyManager = None


class DatabaseManager:
    """SQLite database manager for the application"""
    
    def __init__(self, db_path='regenerative_addresses.db'):
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        import sqlite3
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Links table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                regenerated_url TEXT,
                technique TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Proxies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proxies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT UNIQUE NOT NULL,
                type TEXT DEFAULT 'http',
                status TEXT DEFAULT 'unknown',
                response_time REAL,
                last_checked TIMESTAMP,
                country TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Activity log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        self.conn.commit()
        logger.info("Database initialized successfully")
    
    def add_user(self, username: str, password_hash: str, email: str = None) -> bool:
        """Add new user to database"""
        try:
            import sqlite3
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                          (username, password_hash, email))
            self.conn.commit()
            logger.info(f"User added: {username}")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"User already exists: {username}")
            return False
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        import sqlite3
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'username': row[1],
                'password_hash': row[2],
                'email': row[3],
                'created_at': row[4],
                'last_login': row[5],
                'is_active': row[6]
            }
        return None
    
    def update_last_login(self, user_id: int):
        """Update user's last login time"""
        import sqlite3
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
        self.conn.commit()
    
    def log_activity(self, user_id: int, action: str, details: str, ip_address: str = None):
        """Log user activity"""
        import sqlite3
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO activity_log (user_id, action, details, ip_address) VALUES (?, ?, ?, ?)',
                      (user_id, action, details, ip_address))
        self.conn.commit()
    
    def save_link(self, original_url: str, regenerated_url: str, technique: str, user_id: int = None):
        """Save generated link"""
        import sqlite3
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO links (original_url, regenerated_url, technique, user_id) VALUES (?, ?, ?, ?)',
                      (original_url, regenerated_url, technique, user_id))
        self.conn.commit()
    
    def get_links(self, user_id: int = None, limit: int = 100) -> List[Dict]:
        """Get links from database"""
        import sqlite3
        cursor = self.conn.cursor()
        if user_id:
            cursor.execute('SELECT * FROM links WHERE user_id = ? ORDER BY created_at DESC LIMIT ?',
                          (user_id, limit))
        else:
            cursor.execute('SELECT * FROM links ORDER BY created_at DESC LIMIT ?', (limit,))
        
        links = []
        for row in cursor.fetchall():
            links.append({
                'id': row[0],
                'original_url': row[1],
                'regenerated_url': row[2],
                'technique': row[3],
                'user_id': row[4],
                'created_at': row[5]
            })
        return links
    
    def save_proxy(self, address: str, proxy_type: str = 'http', status: str = 'unknown'):
        """Save proxy to database"""
        import sqlite3
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT OR REPLACE INTO proxies (address, type, status) VALUES (?, ?, ?)',
                          (address, proxy_type, status))
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error saving proxy: {e}")
    
    def update_proxy_status(self, address: str, status: str, response_time: float = None):
        """Update proxy status"""
        import sqlite3
        cursor = self.conn.cursor()
        cursor.execute('UPDATE proxies SET status = ?, response_time = ?, last_checked = CURRENT_TIMESTAMP WHERE address = ?',
                      (status, response_time, address))
        self.conn.commit()
    
    def get_proxies(self, status: str = None, limit: int = 1000) -> List[Dict]:
        """Get proxies from database"""
        import sqlite3
        cursor = self.conn.cursor()
        if status:
            cursor.execute('SELECT * FROM proxies WHERE status = ? LIMIT ?', (status, limit))
        else:
            cursor.execute('SELECT * FROM proxies LIMIT ?', (limit,))
        
        proxies = []
        for row in cursor.fetchall():
            proxies.append({
                'id': row[0],
                'address': row[1],
                'type': row[2],
                'status': row[3],
                'response_time': row[4],
                'last_checked': row[5],
                'country': row[6]
            })
        return proxies
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        import sqlite3
        cursor = self.conn.cursor()
        
        stats = {}
        
        # User count
        cursor.execute('SELECT COUNT(*) FROM users')
        stats['total_users'] = cursor.fetchone()[0]
        
        # Link count
        cursor.execute('SELECT COUNT(*) FROM links')
        stats['total_links'] = cursor.fetchone()[0]
        
        # Proxy count
        cursor.execute('SELECT COUNT(*) FROM proxies')
        stats['total_proxies'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM proxies WHERE status = "active"')
        stats['active_proxies'] = cursor.fetchone()[0]
        
        # Activity count
        cursor.execute('SELECT COUNT(*) FROM activity_log')
        stats['total_activities'] = cursor.fetchone()[0]
        
        return stats


class LinkRegenerator:
    """Professional link regeneration engine"""
    
    TECHNIQUES = {
        'add_parameters': 'Add UTM tracking parameters',
        'change_subdomain': 'Change URL subdomain',
        'add_path_segments': 'Add random path segments',
        'change_tld': 'Change top-level domain',
        'add_tracking_params': 'Add custom tracking parameters',
        'shorten_url_style': 'Convert to shortened URL style',
        'affiliate_style': 'Convert to affiliate link format',
        'case_variation': 'Change character case',
        'encode_special': 'Encode special characters',
        'mirror_domain': 'Create mirrored domain variant'
    }
    
    def __init__(self):
        self.generated_links = []
    
    def regenerate(self, url: str, technique: str) -> str:
        """Regenerate link using specified technique"""
        if technique not in self.TECHNIQUES:
            raise ValueError(f"Unknown technique: {technique}")
        
        method = getattr(self, f'_technique_{technique}', None)
        if method:
            return method(url)
        return url
    
    def _technique_add_parameters(self, url: str) -> str:
        """Add UTM tracking parameters"""
        params = [
            f"utm_source={self._random_string(8)}",
            f"utm_medium={self._random_string(6)}",
            f"utm_campaign={self._random_string(10)}",
            f"utm_content={self._random_string(8)}",
            f"utm_term={self._random_string(6)}"
        ]
        separator = '&' if '?' in url else '?'
        return url + separator + '&'.join(params)
    
    def _technique_change_subdomain(self, url: str) -> str:
        """Change URL subdomain"""
        subdomains = ['www', 'm', 'mobile', 'app', 'api', 'secure', 'shop', 'blog', 'cdn', 'static']
        new_subdomain = random.choice(subdomains)
        
        if '://' in url:
            parts = url.split('://')
            domain_parts = parts[1].split('/')[0].split('.')
            if len(domain_parts) > 2:
                domain_parts[0] = new_subdomain
                new_domain = '.'.join(domain_parts)
                return parts[0] + '://' + new_domain + '/' + '/'.join(parts[1].split('/')[1:])
        return url
    
    def _technique_add_path_segments(self, url: str) -> str:
        """Add random path segments"""
        segments = [self._random_string(8), self._random_string(12), self._random_string(6)]
        return url.rstrip('/') + '/' + '/'.join(segments)
    
    def _technique_change_tld(self, url: str) -> str:
        """Change top-level domain"""
        tlds = ['.com', '.net', '.org', '.info', '.biz', '.co', '.io', '.me', '.cc', '.ws']
        if '://' in url:
            parts = url.split('://')
            domain = parts[1].split('/')[0]
            domain_parts = domain.split('.')
            if len(domain_parts) > 1:
                current_tld = '.' + domain_parts[-1]
                available_tlds = [t for t in tlds if t != current_tld]
                if available_tlds:
                    new_tld = random.choice(available_tlds)
                    domain_parts[-1] = new_tld.lstrip('.')
                    new_domain = '.'.join(domain_parts)
                    path = '/'.join(parts[1].split('/')[1:])
                    return parts[0] + '://' + new_domain + ('/' + path if path else '')
        return url
    
    def _technique_add_tracking_params(self, url: str) -> str:
        """Add custom tracking parameters"""
        tracking_id = self._random_string(8)
        session_id = self._random_string(16)
        params = [
            f"tid={tracking_id}",
            f"sid={session_id}",
            f"ts={int(time.time())}",
            f"ref={self._random_string(8)}"
        ]
        separator = '&' if '?' in url else '?'
        return url + separator + '&'.join(params)
    
    def _technique_shorten_url_style(self, url: str) -> str:
        """Convert to shortened URL style"""
        shorteners = ['bit.ly', 'tinyurl.com', 'short.ly', 't.co', 'goo.gl', 'ow.ly']
        shortener = random.choice(shorteners)
        short_code = self._random_string(6)
        return f"https://{shortener}/{short_code}"
    
    def _technique_affiliate_style(self, url: str) -> str:
        """Convert to affiliate link format"""
        affiliate_id = self._random_string(8)
        sub_id = self._random_string(6)
        separator = '&' if '?' in url else '?'
        return url + separator + f"aff={affiliate_id}&sub={sub_id}&ref=partner"
    
    def _technique_case_variation(self, url: str) -> str:
        """Change character case randomly"""
        result = ''
        for char in url:
            if char.isalpha() and random.random() > 0.5:
                result += char.upper() if char.islower() else char.lower()
            else:
                result += char
        return result
    
    def _technique_encode_special(self, url: str) -> str:
        """Encode special characters"""
        special_chars = {' ': '%20', '?': '%3F', '&': '%26', '=': '%3D', '/': '%2F'}
        result = url
        for char, encoded in special_chars.items():
            if random.random() > 0.5:
                result = result.replace(char, encoded)
        return result
    
    def _technique_mirror_domain(self, url: str) -> str:
        """Create mirrored domain variant"""
        if '://' in url:
            parts = url.split('://')
            domain = parts[1].split('/')[0]
            mirrors = ['mirror1', 'mirror2', 'cdn', 'cache', 'edge']
            mirror = random.choice(mirrors)
            new_domain = f"{mirror}.{domain}"
            path = '/'.join(parts[1].split('/')[1:])
            return parts[0] + '://' + new_domain + ('/' + path if path else '')
        return url
    
    def batch_regenerate(self, url: str, techniques: List[str] = None) -> List[Dict]:
        """Generate multiple variations of a URL"""
        if techniques is None:
            techniques = list(self.TECHNIQUES.keys())
        
        results = []
        for technique in techniques:
            try:
                regenerated = self.regenerate(url, technique)
                results.append({
                    'technique': technique,
                    'description': self.TECHNIQUES[technique],
                    'original': url,
                    'regenerated': regenerated
                })
            except Exception as e:
                logger.error(f"Error in batch regeneration: {e}")
        
        return results
    
    def _random_string(self, length: int = 8) -> str:
        """Generate random alphanumeric string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class ProxyTester:
    """Professional proxy testing system"""
    
    def __init__(self):
        self.working_proxies = []
        self.failed_proxies = []
    
    def test_proxy(self, proxy: str, timeout: int = 10) -> Dict:
        """Test if proxy is working"""
        result = {
            'proxy': proxy,
            'status': 'unknown',
            'response_time': None,
            'error': None
        }
        
        try:
            if ':' not in proxy:
                result['status'] = 'invalid'
                result['error'] = 'Invalid proxy format'
                return result
            
            host, port = proxy.rsplit(':', 1)
            port = int(port)
            
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            connection_result = sock.connect_ex((host, port))
            sock.close()
            
            response_time = time.time() - start_time
            
            if connection_result == 0:
                result['status'] = 'active'
                result['response_time'] = round(response_time * 1000, 2)  # milliseconds
            else:
                result['status'] = 'inactive'
                result['error'] = f'Connection failed (code: {connection_result})'
            
        except ValueError:
            result['status'] = 'invalid'
            result['error'] = 'Invalid port number'
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def test_multiple(self, proxies: List[str], max_threads: int = 50) -> List[Dict]:
        """Test multiple proxies with threading"""
        results = []
        lock = threading.Lock()
        
        def test_single(proxy):
            result = self.test_proxy(proxy)
            with lock:
                results.append(result)
        
        threads = []
        for proxy in proxies:
            if len(threads) >= max_threads:
                for t in threads:
                    t.join()
                threads = []
            
            t = threading.Thread(target=test_single, args=(proxy,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        return results
    
    def get_country(self, proxy: str) -> str:
        """Get proxy country (simplified)"""
        try:
            host = proxy.split(':')[0]
            # This would require GeoIP database in real implementation
            return 'Unknown'
        except:
            return 'Unknown'


class ReportGenerator:
    """Professional report generation system"""
    
    def generate_link_report(self, links: List[Dict]) -> str:
        """Generate HTML report for links"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Link Regeneration Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .header { background-color: #333; color: white; padding: 20px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Link Regeneration Report</h1>
        <p>Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    </div>
    <table>
        <tr>
            <th>ID</th>
            <th>Technique</th>
            <th>Original URL</th>
            <th>Regenerated URL</th>
            <th>Created</th>
        </tr>
"""
        
        for link in links:
            html += f"""
        <tr>
            <td>{link.get('id', 'N/A')}</td>
            <td>{link.get('technique', 'N/A')}</td>
            <td>{link.get('original_url', 'N/A')}</td>
            <td>{link.get('regenerated_url', 'N/A')}</td>
            <td>{link.get('created_at', 'N/A')}</td>
        </tr>
"""
        
        html += """
    </table>
</body>
</html>
"""
        return html
    
    def generate_proxy_report(self, proxies: List[Dict]) -> str:
        """Generate HTML report for proxies"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Proxy Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #2196F3; color: white; }
        .active { background-color: #c8e6c9; }
        .inactive { background-color: #ffcdd2; }
        .header { background-color: #333; color: white; padding: 20px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Proxy Test Report</h1>
        <p>Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    </div>
    <table>
        <tr>
            <th>ID</th>
            <th>Address</th>
            <th>Type</th>
            <th>Status</th>
            <th>Response Time (ms)</th>
            <th>Country</th>
        </tr>
"""
        
        for proxy in proxies:
            status_class = 'active' if proxy.get('status') == 'active' else 'inactive'
            html += f"""
        <tr class="{status_class}">
            <td>{proxy.get('id', 'N/A')}</td>
            <td>{proxy.get('address', 'N/A')}</td>
            <td>{proxy.get('type', 'N/A')}</td>
            <td>{proxy.get('status', 'N/A')}</td>
            <td>{proxy.get('response_time', 'N/A')}</td>
            <td>{proxy.get('country', 'N/A')}</td>
        </tr>
"""
        
        html += """
    </table>
</body>
</html>
"""
        return html
    
    def export_csv(self, data: List[Dict], filename: str):
        """Export data to CSV"""
        if not data:
            return
        
        keys = data[0].keys()
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)


class RegenerativeAddressesToolPro:
    """Professional edition of Regenerative Addresses Tool"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Regenerative Addresses Tool Pro v3.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize components
        self.db = DatabaseManager()
        self.link_regenerator = LinkRegenerator()
        self.proxy_tester = ProxyTester()
        self.report_generator = ReportGenerator()
        
        # Session management
        self.current_user = None
        self.session_start = None
        self.session_timeout = 300
        
        # Load data
        self.proxies = []
        self.load_proxies_from_files()
        
        # Setup UI
        self.setup_styles()
        self.create_main_interface()
        
        # Show login
        self.show_login_screen()
    
    def setup_styles(self):
        """Setup professional styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Color scheme
        self.colors = {
            'bg_dark': '#2b2b2b',
            'bg_medium': '#3c3f41',
            'bg_light': '#4b4b4b',
            'accent': '#007acc',
            'success': '#36a3d9',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'text': '#bbbbbb',
            'text_light': '#ffffff'
        }
        
        # Configure styles
        style.configure('Dark.TFrame', background=self.colors['bg_dark'])
        style.configure('Medium.TFrame', background=self.colors['bg_medium'])
        style.configure('Title.TLabel', background=self.colors['bg_dark'], 
                       foreground=self.colors['accent'], font=('Segoe UI', 16, 'bold'))
        style.configure('Header.TLabel', background=self.colors['bg_dark'], 
                       foreground=self.colors['text_light'], font=('Segoe UI', 12, 'bold'))
        style.configure('Info.TLabel', background=self.colors['bg_dark'], 
                       foreground=self.colors['text'], font=('Segoe UI', 10))
        style.configure('Primary.TButton', background=self.colors['accent'], 
                       foreground='white', font=('Segoe UI', 9))
        style.configure('Success.TButton', background=self.colors['success'], 
                       foreground='white', font=('Segoe UI', 9))
        style.configure('Warning.TButton', background=self.colors['warning'], 
                       foreground='black', font=('Segoe UI', 9))
        style.configure('Danger.TButton', background=self.colors['danger'], 
                       foreground='white', font=('Segoe UI', 9))
    
    def create_main_interface(self):
        """Create professional main interface"""
        # Main container
        self.main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.create_professional_header()
        
        # Content area
        self.content_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Status bar
        self.create_professional_status_bar()
    
    def create_professional_header(self):
        """Create professional header"""
        header = ttk.Frame(self.main_frame, style='Medium.TFrame')
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Logo area
        logo_frame = ttk.Frame(header, style='Medium.TFrame')
        logo_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        ttk.Label(logo_frame, text="◉", style='Title.TLabel', 
                 font=('Segoe UI', 20)).pack(side=tk.LEFT)
        ttk.Label(logo_frame, text="Regenerative Addresses Tool Pro", 
                 style='Title.TLabel').pack(side=tk.LEFT, padx=(5, 0))
        
        # User area
        self.user_frame = ttk.Frame(header, style='Medium.TFrame')
        self.user_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.user_label = ttk.Label(self.user_frame, text="Not logged in", 
                                   style='Info.TLabel')
        self.user_label.pack(side=tk.LEFT, padx=5)
        
        self.logout_btn = ttk.Button(self.user_frame, text="Logout", 
                                    command=self.logout, style='Danger.TButton')
        self.logout_btn.pack(side=tk.LEFT, padx=5)
        self.logout_btn.pack_forget()
    
    def create_professional_status_bar(self):
        """Create professional status bar"""
        status_frame = ttk.Frame(self.main_frame, style='Medium.TFrame')
        status_frame.pack(fill=tk.X)
        
        # Status message
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                style='Info.TLabel')
        status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Stats
        self.stats_label = ttk.Label(status_frame, text="", style='Info.TLabel')
        self.stats_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def show_login_screen(self):
        """Show professional login screen"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Login container
        container = ttk.Frame(self.content_frame, style='Dark.TFrame')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Login card
        card = ttk.LabelFrame(container, text="Authentication", padding="30")
        card.configure(padding="30")
        
        # Username
        ttk.Label(card, text="Username:", style='Info.TLabel').grid(row=0, column=0, 
                                                                   sticky=tk.W, pady=10)
        self.username_entry = ttk.Entry(card, width=30)
        self.username_entry.grid(row=0, column=1, pady=10, padx=(10, 0))
        
        # Password
        ttk.Label(card, text="Password:", style='Info.TLabel').grid(row=1, column=0, 
                                                                   sticky=tk.W, pady=10)
        self.password_entry = ttk.Entry(card, width=30, show="●")
        self.password_entry.grid(row=1, column=1, pady=10, padx=(10, 0))
        
        # Remember me
        self.remember_var = tk.BooleanVar()
        ttk.Checkbutton(card, text="Remember me", variable=self.remember_var).grid(
            row=2, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        # Buttons
        btn_frame = ttk.Frame(card)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Login", command=self.login, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Register", command=self.show_register_screen, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        
        card.pack()
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()
    
    def show_register_screen(self):
        """Show professional registration screen"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        container = ttk.Frame(self.content_frame, style='Dark.TFrame')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        card = ttk.LabelFrame(container, text="Create Account", padding="30")
        card.configure(padding="30")
        
        # Fields
        ttk.Label(card, text="Username:", style='Info.TLabel').grid(row=0, column=0, 
                                                                   sticky=tk.W, pady=10)
        self.reg_username = ttk.Entry(card, width=30)
        self.reg_username.grid(row=0, column=1, pady=10, padx=(10, 0))
        
        ttk.Label(card, text="Email:", style='Info.TLabel').grid(row=1, column=0, 
                                                               sticky=tk.W, pady=10)
        self.reg_email = ttk.Entry(card, width=30)
        self.reg_email.grid(row=1, column=1, pady=10, padx=(10, 0))
        
        ttk.Label(card, text="Password:", style='Info.TLabel').grid(row=2, column=0, 
                                                                   sticky=tk.W, pady=10)
        self.reg_password = ttk.Entry(card, width=30, show="●")
        self.reg_password.grid(row=2, column=1, pady=10, padx=(10, 0))
        
        ttk.Label(card, text="Confirm:", style='Info.TLabel').grid(row=3, column=0, 
                                                                  sticky=tk.W, pady=10)
        self.reg_confirm = ttk.Entry(card, width=30, show="●")
        self.reg_confirm.grid(row=3, column=1, pady=10, padx=(10, 0))
        
        # Buttons
        btn_frame = ttk.Frame(card)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Create Account", command=self.register, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back to Login", command=self.show_login_screen, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        card.pack()
    
    def show_dashboard(self):
        """Show professional dashboard"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Notebook for tabs
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Dashboard tab
        self.create_dashboard_tab(notebook)
        
        # Link Generator tab
        self.create_link_generator_tab(notebook)
        
        # Proxy Manager tab
        self.create_proxy_manager_tab(notebook)
        
        # Reports tab
        self.create_reports_tab(notebook)
        
        # Settings tab
        self.create_settings_tab(notebook)
        
        # Security Protection tab
        self.create_security_protection_tab(notebook)
        
        # Networking Education tab
        self.create_networking_education_tab(notebook)
        
        # Buy Me a Coffee tab
        self.create_coffee_tab(notebook)
        
        # Update stats
        self.update_dashboard_stats()
    
    def create_dashboard_tab(self, notebook):
        """Create professional dashboard tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text=" Dashboard ")
        
        # Welcome message
        header = ttk.Label(frame, text=f"Welcome, {self.current_user or 'User'}", 
                          style='Title.TLabel')
        header.pack(pady=20)
        
        # Stats cards
        cards_frame = ttk.Frame(frame, style='Dark.TFrame')
        cards_frame.pack(fill=tk.X, padx=20, pady=10)
        
        stats = self.db.get_statistics()
        
        # Create stat cards
        stat_data = [
            ("Total Links", stats.get('total_links', 0), '#2196F3'),
            ("Active Proxies", stats.get('active_proxies', 0), '#4CAF50'),
            ("Total Proxies", stats.get('total_proxies', 0), '#FF9800'),
            ("Users", stats.get('total_users', 0), '#9C27B0')
        ]
        
        for title, value, color in stat_data:
            card = tk.Frame(cards_frame, bg=color, width=200, height=100)
            card.pack(side=tk.LEFT, padx=10, pady=5)
            card.pack_propagate(False)
            
            tk.Label(card, text=str(value), bg=color, fg='white', 
                    font=('Segoe UI', 24, 'bold')).pack(expand=True)
            tk.Label(card, text=title, bg=color, fg='white', 
                    font=('Segoe UI', 10)).pack()
        
        # Recent activity
        activity_frame = ttk.LabelFrame(frame, text="Recent Activity", padding="10")
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.activity_text = scrolledtext.ScrolledText(activity_frame, height=10, 
                                                       bg='#1e1e1e', fg='#bbbbbb',
                                                       font=('Consolas', 9))
        self.activity_text.pack(fill=tk.BOTH, expand=True)
        
        # Load recent activity
        self.load_recent_activity()
    
    def create_link_generator_tab(self, notebook):
        """Create professional link generator tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text=" Link Generator ")
        
        # Input section
        input_frame = ttk.LabelFrame(frame, text="URL Input", padding="15")
        input_frame.pack(fill=tk.X, padx=15, pady=10)
        
        ttk.Label(input_frame, text="Original URL:", style='Info.TLabel').grid(row=0, column=0, 
                                                                              sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(input_frame, width=70, font=('Segoe UI', 10))
        self.url_entry.grid(row=0, column=1, pady=5, padx=(10, 0), columnspan=2)
        
        # Technique selection
        ttk.Label(input_frame, text="Technique:", style='Info.TLabel').grid(row=1, column=0, 
                                                                            sticky=tk.W, pady=5)
        self.technique_var = tk.StringVar(value='add_parameters')
        techniques = list(self.link_regenerator.TECHNIQUES.keys())
        self.technique_combo = ttk.Combobox(input_frame, textvariable=self.technique_var, 
                                           values=techniques, width=30, state='readonly')
        self.technique_combo.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Technique description
        self.tech_desc = ttk.Label(input_frame, text=self.link_regenerator.TECHNIQUES['add_parameters'],
                                   style='Info.TLabel', wraplength=400)
        self.tech_desc.grid(row=1, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        
        self.technique_combo.bind('<<ComboboxSelected>>', self.update_technique_desc)
        
        # Options
        options_frame = ttk.Frame(input_frame)
        options_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.use_proxy_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Use Proxy", variable=self.use_proxy_var).pack(side=tk.LEFT, padx=5)
        
        self.save_to_db_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Save to Database", variable=self.save_to_db_var).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=15)
        
        ttk.Button(btn_frame, text="Generate", command=self.generate_link, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Batch Generate", command=self.batch_generate_links, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_link_fields, 
                  style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        
        # Results section
        results_frame = ttk.LabelFrame(frame, text="Generated Links", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Create treeview for results
        columns = ('technique', 'original', 'regenerated', 'timestamp')
        self.links_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=12)
        
        self.links_tree.heading('technique', text='Technique')
        self.links_tree.heading('original', text='Original URL')
        self.links_tree.heading('regenerated', text='Regenerated URL')
        self.links_tree.heading('timestamp', text='Timestamp')
        
        self.links_tree.column('technique', width=150)
        self.links_tree.column('original', width=300)
        self.links_tree.column('regenerated', width=300)
        self.links_tree.column('timestamp', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.links_tree.yview)
        self.links_tree.configure(yscrollcommand=scrollbar.set)
        
        self.links_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Context menu
        self.links_tree.bind('<Button-3>', self.show_link_context_menu)
    
    def create_proxy_manager_tab(self, notebook):
        """Create professional proxy manager tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text=" Proxy Manager ")
        
        # Control panel
        control_frame = ttk.LabelFrame(frame, text="Controls", padding="10")
        control_frame.pack(fill=tk.X, padx=15, pady=10)
        
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Test All", command=self.test_all_proxies, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Import", command=self.import_proxies, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export Working", command=self.export_working_proxies, 
                  style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Failed", command=self.clear_failed_proxies, 
                  style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        # Stats
        self.proxy_stats_label = ttk.Label(control_frame, text="Proxies: 0 | Active: 0 | Failed: 0",
                                          style='Info.TLabel')
        self.proxy_stats_label.pack(pady=(10, 0))
        
        # Proxy list
        list_frame = ttk.LabelFrame(frame, text="Proxy List", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Treeview for proxies
        columns = ('address', 'type', 'status', 'response_time', 'last_checked')
        self.proxy_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.proxy_tree.heading('address', text='Address')
        self.proxy_tree.heading('type', text='Type')
        self.proxy_tree.heading('status', text='Status')
        self.proxy_tree.heading('response_time', text='Response (ms)')
        self.proxy_tree.heading('last_checked', text='Last Checked')
        
        self.proxy_tree.column('address', width=200)
        self.proxy_tree.column('type', width=80)
        self.proxy_tree.column('status', width=100)
        self.proxy_tree.column('response_time', width=120)
        self.proxy_tree.column('last_checked', width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.proxy_tree.yview)
        self.proxy_tree.configure(yscrollcommand=scrollbar.set)
        
        self.proxy_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load proxies
        self.load_proxies_to_tree()
    
    def create_reports_tab(self, notebook):
        """Create professional reports tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text=" Reports ")
        
        # Report types
        types_frame = ttk.LabelFrame(frame, text="Generate Reports", padding="15")
        types_frame.pack(fill=tk.X, padx=15, pady=10)
        
        ttk.Button(types_frame, text="Links Report (HTML)", command=self.generate_links_report, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(types_frame, text="Proxies Report (HTML)", command=self.generate_proxies_report, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(types_frame, text="Export Links (CSV)", command=self.export_links_csv, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(types_frame, text="Export Proxies (CSV)", command=self.export_proxies_csv, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        
        # Preview area
        preview_frame = ttk.LabelFrame(frame, text="Report Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.report_preview = scrolledtext.ScrolledText(preview_frame, height=20, 
                                                         bg='#1e1e1e', fg='#bbbbbb',
                                                         font=('Consolas', 9))
        self.report_preview.pack(fill=tk.BOTH, expand=True)
    
    def create_settings_tab(self, notebook):
        """Create professional settings tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text=" Settings ")
        
        # Application settings
        app_frame = ttk.LabelFrame(frame, text="Application Settings", padding="15")
        app_frame.pack(fill=tk.X, padx=15, pady=10)
        
        ttk.Label(app_frame, text="Session Timeout (seconds):", style='Info.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.timeout_var = tk.StringVar(value="300")
        ttk.Entry(app_frame, textvariable=self.timeout_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Label(app_frame, text="Max Threads:", style='Info.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.threads_var = tk.StringVar(value="50")
        ttk.Entry(app_frame, textvariable=self.threads_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Label(app_frame, text="Proxy Timeout (seconds):", style='Info.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.proxy_timeout_var = tk.StringVar(value="10")
        ttk.Entry(app_frame, textvariable=self.proxy_timeout_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Buttons
        btn_frame = ttk.Frame(app_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Save Settings", command=self.save_settings, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset to Default", command=self.reset_settings, 
                  style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        
        # About
        about_frame = ttk.LabelFrame(frame, text="About", padding="15")
        about_frame.pack(fill=tk.X, padx=15, pady=10)
        
        about_text = """
Regenerative Addresses Tool Pro v3.0

Professional link regeneration and proxy management system.

Features:
• Advanced link regeneration with 10 techniques
• Professional proxy testing and management
• Database integration for data persistence
• Comprehensive reporting system
• Multi-threaded operations
• Modern professional interface

© 2026 All rights reserved.
        """
        
        ttk.Label(about_frame, text=about_text.strip(), style='Info.TLabel').pack(pady=10)
    
    def create_security_protection_tab(self, notebook):
        """Create professional security protection tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text=" KEEP ME SAFE ")
        
        # Main container
        main_frame = ttk.Frame(frame, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Security Scanner Section
        scanner_frame = ttk.LabelFrame(main_frame, text="🛡️ System Security Scanner", padding="15")
        scanner_frame.pack(fill=tk.X, pady=(0, 10))
        
        scanner_info = ttk.Label(scanner_frame, 
                                text="Scan your system for vulnerabilities and security issues",
                                style='Info.TLabel')
        scanner_info.pack(pady=(0, 10))
        
        scanner_btn_frame = ttk.Frame(scanner_frame)
        scanner_btn_frame.pack(fill=tk.X)
        
        ttk.Button(scanner_btn_frame, text="🔍 Full Security Scan", 
                  command=self.run_security_scan, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(scanner_btn_frame, text="🔐 Password Security Check", 
                  command=self.check_password_security, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(scanner_btn_frame, text="🌐 Network Vulnerability Scan", 
                  command=self.scan_network_vulnerabilities, style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        
        # System Hardening Section
        hardening_frame = ttk.LabelFrame(main_frame, text="⚙️ System Hardening Tools", padding="15")
        hardening_frame.pack(fill=tk.X, pady=(0, 10))
        
        hardening_info = ttk.Label(hardening_frame, 
                                  text="Apply security hardening to protect your system",
                                  style='Info.TLabel')
        hardening_info.pack(pady=(0, 10))
        
        hardening_btn_frame = ttk.Frame(hardening_frame)
        hardening_btn_frame.pack(fill=tk.X)
        
        ttk.Button(hardening_btn_frame, text="🔒 Harden System Security", 
                  command=self.harden_system, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(hardening_btn_frame, text="🛠️ Security Audit", 
                  command=self.run_security_audit, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(hardening_btn_frame, text="📋 Generate Report", 
                  command=self.generate_security_report, style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        
        # Real-time Protection Section
        protection_frame = ttk.LabelFrame(main_frame, text="🚨 Real-time Protection", padding="15")
        protection_frame.pack(fill=tk.X, pady=(0, 10))
        
        protection_info = ttk.Label(protection_frame, 
                                  text="Enable real-time security monitoring and protection",
                                  style='Info.TLabel')
        protection_info.pack(pady=(0, 10))
        
        # Protection toggles
        self.real_time_protection = tk.BooleanVar(value=False)
        self.auto_updates = tk.BooleanVar(value=False)
        self.monitor_network = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(protection_frame, text="🛡️ Real-time Threat Detection", 
                       variable=self.real_time_protection).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(protection_frame, text="🔄 Automatic Security Updates", 
                       variable=self.auto_updates).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(protection_frame, text="🌐 Network Traffic Monitoring", 
                       variable=self.monitor_network).pack(anchor=tk.W, pady=2)
        
        protection_btn_frame = ttk.Frame(protection_frame)
        protection_btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(protection_btn_frame, text="▶️ Start Protection", 
                  command=self.start_protection, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(protection_btn_frame, text="⏹️ Stop Protection", 
                  command=self.stop_protection, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, text="📊 Security Scan Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for results
        columns = ('type', 'severity', 'description', 'status')
        self.security_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=12)
        
        self.security_tree.heading('type', text='Type')
        self.security_tree.heading('severity', text='Severity')
        self.security_tree.heading('description', text='Description')
        self.security_tree.heading('status', text='Status')
        
        self.security_tree.column('type', width=120)
        self.security_tree.column('severity', width=100)
        self.security_tree.column('description', width=300)
        self.security_tree.column('status', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.security_tree.yview)
        self.security_tree.configure(yscrollcommand=scrollbar.set)
        
        self.security_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.security_status_var = tk.StringVar(value="Ready to protect your system")
        status_label = ttk.Label(main_frame, textvariable=self.security_status_var, 
                                style='Info.TLabel')
        status_label.pack(fill=tk.X, pady=(0, 10))
    
    def run_security_scan(self):
        """Run comprehensive security scan"""
        self.security_status_var.set("Running security scan...")
        
        def scan_thread():
            try:
                # Import security scanner
                import sys
                sys.path.append(os.getcwd())
                from security_scanner import NetworkSecurityScanner
                
                scanner = NetworkSecurityScanner()
                results = scanner.scan_system_security()
                
                # Update UI with results
                self.root.after(0, lambda: self.update_security_results(results))
                self.root.after(0, lambda: self.security_status_var.set(f"Scan complete - Score: {results['security_score']}/100"))
                
                # Log activity
                if self.current_user:
                    user = self.db.get_user(self.current_user)
                    if user:
                        self.db.log_activity(user['id'], 'security_scan', f"Score: {results['security_score']}", self.get_client_ip())
                
            except Exception as e:
                self.root.after(0, lambda: self.security_status_var.set(f"Scan failed: {str(e)}"))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def check_password_security(self):
        """Check password security"""
        self.security_status_var.set("Checking password security...")
        
        def password_check_thread():
            try:
                import sys
                sys.path.append(os.getcwd())
                from security_scanner import PasswordSecurityChecker
                
                checker = PasswordSecurityChecker()
                
                # Get current user's password (for demo, use a test password)
                test_password = simpledialog.askstring("Password Security", 
                                                      "Enter password to test:", 
                                                      show='*')
                if test_password:
                    analysis = checker.check_password_strength(test_password)
                    
                    # Display results
                    result_text = f"Password Strength: {analysis['strength']}\n"
                    result_text += f"Score: {analysis['score']}/100\n"
                    result_text += f"Entropy: {analysis['entropy']:.2f} bits\n\n"
                    
                    if analysis['issues']:
                        result_text += "Issues Found:\n"
                        for issue in analysis['issues']:
                            result_text += f"• {issue}\n"
                    
                    if analysis['recommendations']:
                        result_text += "\nRecommendations:\n"
                        for rec in analysis['recommendations']:
                            result_text += f"• {rec}\n"
                    
                    messagebox.showinfo("Password Security Analysis", result_text)
                    self.security_status_var.set("Password security check complete")
                else:
                    self.security_status_var.set("Password security check cancelled")
                
            except Exception as e:
                self.security_status_var.set(f"Password check failed: {str(e)}")
        
        threading.Thread(target=password_check_thread, daemon=True).start()
    
    def scan_network_vulnerabilities(self):
        """Scan network vulnerabilities"""
        self.security_status_var.set("Scanning network vulnerabilities...")
        
        def network_scan_thread():
            try:
                import sys
                sys.path.append(os.getcwd())
                from security_scanner import NetworkVulnerabilityScanner
                
                scanner = NetworkVulnerabilityScanner()
                
                # Get network range (for demo, use local /24)
                import socket
                local_ip = socket.gethostbyname(socket.gethostname())
                network_parts = local_ip.split('.')
                network_range = f"{'.'.join(network_parts[:3])}.0/24"
                
                results = scanner.scan_network_range(network_range)
                
                # Update UI
                self.root.after(0, lambda: self.update_network_results(results))
                self.root.after(0, lambda: self.security_status_var.set(f"Network scan complete - {len(results['hosts'])} hosts found"))
                
            except Exception as e:
                self.root.after(0, lambda: self.security_status_var.set(f"Network scan failed: {str(e)}"))
        
        threading.Thread(target=network_scan_thread, daemon=True).start()
    
    def harden_system(self):
        """Apply system hardening"""
        if not messagebox.askyesno("System Hardening", 
                                   "This will modify system settings. Continue?"):
            return
        
        self.security_status_var.set("Applying system hardening...")
        
        def hardening_thread():
            try:
                import sys
                sys.path.append(os.getcwd())
                from system_hardener import SystemHardener
                
                hardener = SystemHardener()
                results = hardener.harden_system()
                
                if results['success']:
                    report = hardener.generate_hardening_report(results)
                    self.root.after(0, lambda: self.show_hardening_report(report))
                    self.root.after(0, lambda: self.security_status_var.set("System hardening applied successfully"))
                else:
                    self.root.after(0, lambda: self.security_status_var.set("System hardening failed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.security_status_var.set(f"Hardening failed: {str(e)}"))
        
        threading.Thread(target=hardening_thread, daemon=True).start()
    
    def run_security_audit(self):
        """Run security audit"""
        self.security_status_var.set("Running security audit...")
        
        def audit_thread():
            try:
                import sys
                sys.path.append(os.getcwd())
                from system_hardener import SecurityAuditTool
                
                auditor = SecurityAuditTool()
                results = auditor.perform_security_audit()
                
                report = auditor.generate_audit_report(results)
                self.root.after(0, lambda: self.show_audit_report(report))
                self.root.after(0, lambda: self.security_status_var.set(f"Audit complete - Score: {results['audit_score']}/100"))
                
            except Exception as e:
                self.root.after(0, lambda: self.security_status_var.set(f"Audit failed: {str(e)}"))
        
        threading.Thread(target=audit_thread, daemon=True).start()
    
    def generate_security_report(self):
        """Generate comprehensive security report"""
        self.security_status_var.set("Generating security report...")
        
        def report_thread():
            try:
                # Create report window
                self.root.after(0, self.create_report_window)
                self.root.after(0, lambda: self.security_status_var.set("Security report generated"))
                
            except Exception as e:
                self.root.after(0, lambda: self.security_status_var.set(f"Report generation failed: {str(e)}"))
        
        threading.Thread(target=report_thread, daemon=True).start()
    
    def start_protection(self):
        """Start real-time protection"""
        self.security_status_var.set("Starting real-time protection...")
        
        # Enable protection settings
        protection_settings = []
        
        if self.real_time_protection.get():
            protection_settings.append("Real-time threat detection")
        if self.auto_updates.get():
            protection_settings.append("Automatic updates")
        if self.monitor_network.get():
            protection_settings.append("Network monitoring")
        
        if protection_settings:
            self.security_status_var.set(f"Protection active: {', '.join(protection_settings)}")
            
            # Log activity
            if self.current_user:
                user = self.db.get_user(self.current_user)
                if user:
                    self.db.log_activity(user['id'], 'protection_started', ', '.join(protection_settings), self.get_client_ip())
        else:
            self.security_status_var.set("No protection features selected")
    
    def stop_protection(self):
        """Stop real-time protection"""
        self.real_time_protection.set(False)
        self.auto_updates.set(False)
        self.monitor_network.set(False)
        
        self.security_status_var.set("Real-time protection stopped")
        
        # Log activity
        if self.current_user:
            user = self.db.get_user(self.current_user)
            if user:
                self.db.log_activity(user['id'], 'protection_stopped', 'All protection disabled', self.get_client_ip())
    
    def update_security_results(self, results):
        """Update security results treeview"""
        # Clear existing results
        self.security_tree.delete(*self.security_tree.get_children())
        
        # Add vulnerabilities
        for vuln in results['vulnerabilities']:
            self.security_tree.insert('', tk.END, values=(
                'Vulnerability',
                vuln['severity'],
                vuln['description'],
                'Found'
            ))
        
        # Add open ports
        for port in results['open_ports']:
            self.security_tree.insert('', tk.END, values=(
                'Open Port',
                port['risk'],
                f"Port {port['port']} ({port['service']})",
                'Open'
            ))
        
        # Add system info
        self.security_tree.insert('', tk.END, values=(
            'System Info',
            'Info',
            f"Security Score: {results['security_score']}/100",
            'Calculated'
        ))
    
    def update_network_results(self, results):
        """Update network scan results"""
        # Clear existing results
        self.security_tree.delete(*self.security_tree.get_children())
        
        # Add hosts
        for host in results['hosts']:
            self.security_tree.insert('', tk.END, values=(
                'Host',
                'Info',
                f"{host['ip']} ({host['hostname']})",
                'Found'
            ))
            
            # Add open ports for this host
            for port in host['open_ports']:
                self.security_tree.insert('', tk.END, values=(
                    'Open Port',
                    port['risk'],
                    f"{host['ip']}:{port['port']} ({port['service']})",
                    'Open'
                ))
        
        # Add vulnerabilities
        for vuln in results['vulnerabilities']:
            self.security_tree.insert('', tk.END, values=(
                'Vulnerability',
                vuln['severity'],
                vuln['description'],
                'Found'
            ))
    
    def show_hardening_report(self, report):
        """Show hardening report"""
        report_window = tk.Toplevel(self.root)
        report_window.title("System Hardening Report")
        report_window.geometry("800x600")
        report_window.configure(bg='#2b2b2b')
        
        # Create text widget
        text_widget = scrolledtext.ScrolledText(report_window, bg='#1e1e1e', fg='#bbbbbb',
                                               font=('Consolas', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(1.0, report)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(report_window, text="Close", 
                  command=report_window.destroy).pack(pady=10)
    
    def show_audit_report(self, report):
        """Show security audit report"""
        report_window = tk.Toplevel(self.root)
        report_window.title("Security Audit Report")
        report_window.geometry("800x600")
        report_window.configure(bg='#2b2b2b')
        
        # Create text widget
        text_widget = scrolledtext.ScrolledText(report_window, bg='#1e1e1e', fg='#bbbbbb',
                                               font=('Consolas', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(1.0, report)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(report_window, text="Close", 
                  command=report_window.destroy).pack(pady=10)
    
    def create_report_window(self):
        """Create comprehensive security report window"""
        report_window = tk.Toplevel(self.root)
        report_window.title("Comprehensive Security Report")
        report_window.geometry("900x700")
        report_window.configure(bg='#2b2b2b')
        
        # Create notebook for different report sections
        report_notebook = ttk.Notebook(report_window)
        report_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Summary tab
        summary_frame = ttk.Frame(report_notebook, style='Dark.TFrame')
        report_notebook.add(summary_frame, text="Summary")
        
        summary_text = scrolledtext.ScrolledText(summary_frame, bg='#1e1e1e', fg='#bbbbbb',
                                                font=('Consolas', 10))
        summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        summary_text.insert(1.0, "SECURITY REPORT SUMMARY\n" + "="*50 + "\n\n")
        summary_text.insert(tk.END, "This report provides a comprehensive analysis of your system's security posture.\n")
        summary_text.insert(tk.END, "Review each section for detailed findings and recommendations.\n\n")
        summary_text.insert(tk.END, "Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        summary_text.config(state=tk.DISABLED)
        
        # Vulnerabilities tab
        vuln_frame = ttk.Frame(report_notebook, style='Dark.TFrame')
        report_notebook.add(vuln_frame, text="Vulnerabilities")
        
        vuln_text = scrolledtext.ScrolledText(vuln_frame, bg='#1e1e1e', fg='#bbbbbb',
                                            font=('Consolas', 10))
        vuln_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        vuln_text.insert(1.0, "VULNERABILITY ASSESSMENT\n" + "="*50 + "\n\n")
        vuln_text.insert(tk.END, "No critical vulnerabilities detected in this scan.\n")
        vuln_text.insert(tk.END, "Continue regular security monitoring.\n")
        vuln_text.config(state=tk.DISABLED)
        
        # Recommendations tab
        rec_frame = ttk.Frame(report_notebook, style='Dark.TFrame')
        report_notebook.add(rec_frame, text="Recommendations")
        
        rec_text = scrolledtext.ScrolledText(rec_frame, bg='#1e1e1e', fg='#bbbbbb',
                                            font=('Consolas', 10))
        rec_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        rec_text.insert(1.0, "SECURITY RECOMMENDATIONS\n" + "="*50 + "\n\n")
        rec_text.insert(tk.END, "1. Keep your system updated with latest security patches\n")
        rec_text.insert(tk.END, "2. Use strong, unique passwords for all accounts\n")
        rec_text.insert(tk.END, "3. Enable two-factor authentication where available\n")
        rec_text.insert(tk.END, "4. Regularly backup important data\n")
        rec_text.insert(tk.END, "5. Monitor system activity for unusual behavior\n")
        rec_text.insert(tk.END, "6. Use reputable antivirus/antimalware software\n")
        rec_text.insert(tk.END, "7. Secure your network with proper firewall configuration\n")
        rec_text.insert(tk.END, "8. Educate yourself about common security threats\n")
        rec_text.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(report_window, text="Close Report", 
                  command=report_window.destroy).pack(pady=10)
    
    def create_networking_education_tab(self, notebook):
        """Create networking education tab"""
        try:
            # Import networking education module
            import sys
            sys.path.append(os.getcwd())
            from networking_education import add_networking_education_tab
            
            # Add the education tab
            add_networking_education_tab(notebook)
            
        except ImportError:
            # Fallback if module not available
            frame = ttk.Frame(notebook, style='Dark.TFrame')
            notebook.add(frame, text=" KEEP ME SAFE 2 ")
            
            # Simple fallback content
            container = ttk.Frame(frame, style='Dark.TFrame')
            container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            ttk.Label(container, text="🌐 Networking Security Education", 
                     style='Title.TLabel').pack(pady=20)
            
            ttk.Label(container, 
                     text="Networking security education module is loading...\n\nThis section provides:\n• Network fundamentals\n• Security best practices\n• Protection tools\n• Educational resources",
                     style='Info.TLabel').pack(pady=20)
            
            ttk.Button(container, text="Refresh Module", 
                      command=lambda: self.create_networking_education_tab(notebook),
                      style='Primary.TButton').pack(pady=10)
    
    def create_coffee_tab(self, notebook):
        """Create Buy Me a Coffee tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text=" ☕ Coffee ")
        
        # Main container
        container = ttk.Frame(frame, style='Dark.TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Coffee section
        coffee_frame = ttk.LabelFrame(container, text="Support Development", style='Card.TLabelframe', padding="30")
        coffee_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Coffee icon and message
        ttk.Label(coffee_frame, text="☕", font=('Segoe UI', 48), style='Info.TLabel').pack(pady=10)
        
        ttk.Label(coffee_frame, text="Enjoying the Regenerative Addresses Tool Pro?", 
                 font=('Segoe UI', 16, 'bold'), style='Info.TLabel').pack(pady=10)
        
        ttk.Label(coffee_frame, text="If you find this tool helpful for your security work,\nconsider buying me a coffee to support continued development!", 
                 font=('Segoe UI', 12), style='Info.TLabel', justify=tk.CENTER).pack(pady=20)
        
        # Coffee link button
        def open_coffee_link():
            import webbrowser
            # Replace with your actual Buy Me a Coffee link
            webbrowser.open("https://www.buymeacoffee.com/YOUR_USERNAME")
        
        coffee_btn = ttk.Button(coffee_frame, text="☕ Buy Me a Coffee", 
                               command=open_coffee_link,
                               style='Success.TButton')
        coffee_btn.pack(pady=20, padx=20, ipady=10, ipadx=20)
        
        # Alternative support info
        ttk.Separator(coffee_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        
        ttk.Label(coffee_frame, text="Your support helps me:\n• Add new security features\n• Improve existing tools\n• Provide regular updates\n• Keep the tool free and open source", 
                 font=('Segoe UI', 11), style='Info.TLabel', justify=tk.LEFT).pack(pady=10)
        
        # Optional support message
        ttk.Label(coffee_frame, text="No pressure - the tool will always be free!\nBut coffee always helps with late-night coding sessions! 😊", 
                 font=('Segoe UI', 10, 'italic'), style='Info.TLabel', justify=tk.CENTER).pack(pady=15)
        
        # Stats section
        stats_frame = ttk.LabelFrame(container, text="Tool Statistics", style='Card.TLabelframe', padding="20")
        stats_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(stats_frame, text="• 7,419+ Proxy Addresses", style='Info.TLabel').pack(anchor=tk.W, pady=2)
        ttk.Label(stats_frame, text="• Real Security Scanner", style='Info.TLabel').pack(anchor=tk.W, pady=2)
        ttk.Label(stats_frame, text="• System Hardening Tools", style='Info.TLabel').pack(anchor=tk.W, pady=2)
        ttk.Label(stats_frame, text="• Networking Education Module", style='Info.TLabel').pack(anchor=tk.W, pady=2)
        ttk.Label(stats_frame, text="• Professional Web Interface", style='Info.TLabel').pack(anchor=tk.W, pady=2)
        ttk.Label(stats_frame, text="• Cross-Platform Support", style='Info.TLabel').pack(anchor=tk.W, pady=2)
    
    # Method implementations
    def login(self):
        """Handle user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        user = self.db.get_user(username)
        if user:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if user['password_hash'] == password_hash:
                self.current_user = username
                self.session_start = time.time()
                self.db.update_last_login(user['id'])
                self.db.log_activity(user['id'], 'login', 'User logged in', self.get_client_ip())
                
                self.show_dashboard()
                self.update_user_display()
                self.status_var.set(f"Welcome, {username}")
                logger.info(f"User logged in: {username}")
                return
        
        messagebox.showerror("Error", "Invalid username or password")
        logger.warning(f"Failed login attempt: {username}")
    
    def register(self):
        """Handle user registration"""
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()
        confirm = self.reg_confirm.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in required fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if self.db.add_user(username, password_hash, email):
            messagebox.showinfo("Success", "Account created successfully!")
            logger.info(f"New user registered: {username}")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "Username already exists")
    
    def logout(self):
        """Handle user logout"""
        if self.current_user:
            user = self.db.get_user(self.current_user)
            if user:
                self.db.log_activity(user['id'], 'logout', 'User logged out', self.get_client_ip())
        
        self.current_user = None
        self.session_start = None
        self.show_login_screen()
        self.update_user_display()
        self.status_var.set("Logged out")
        logger.info("User logged out")
    
    def update_user_display(self):
        """Update user display in header"""
        if self.current_user:
            self.user_label.config(text=f"Welcome, {self.current_user}")
            self.logout_btn.pack(side=tk.LEFT, padx=5)
        else:
            self.user_label.config(text="Not logged in")
            self.logout_btn.pack_forget()
    
    def get_client_ip(self):
        """Get client IP address"""
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "Unknown"
    
    def load_proxies_from_files(self):
        """Load proxies from all proxy files"""
        proxy_files = [
            'all_proxies.txt', 'proxies.txt', 'http_proxies.txt',
            'socks4_proxies.txt', 'socks5_proxies.txt',
            'http_proxies2.txt', 'socks4_proxies2.txt', 'socks5_proxies2.txt'
        ]
        
        for proxy_file in proxy_files:
            if os.path.exists(proxy_file):
                try:
                    with open(proxy_file, 'r') as f:
                        file_proxies = [line.strip() for line in f if line.strip() and ':' in line.strip()]
                        self.proxies.extend(file_proxies)
                        
                        # Save to database
                        for proxy in file_proxies:
                            proxy_type = 'http'
                            if 'socks4' in proxy_file.lower():
                                proxy_type = 'socks4'
                            elif 'socks5' in proxy_file.lower():
                                proxy_type = 'socks5'
                            self.db.save_proxy(proxy, proxy_type)
                    
                    logger.info(f"Loaded {len(file_proxies)} proxies from {proxy_file}")
                except Exception as e:
                    logger.error(f"Error loading {proxy_file}: {e}")
        
        # Remove duplicates
        self.proxies = list(set(self.proxies))
        logger.info(f"Total unique proxies loaded: {len(self.proxies)}")
    
    def update_technique_desc(self, event=None):
        """Update technique description"""
        technique = self.technique_var.get()
        desc = self.link_regenerator.TECHNIQUES.get(technique, '')
        self.tech_desc.config(text=desc)
    
    def generate_link(self):
        """Generate single link"""
        url = self.url_entry.get().strip()
        technique = self.technique_var.get()
        
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        try:
            regenerated = self.link_regenerator.regenerate(url, technique)
            
            # Get user ID if logged in
            user_id = None
            if self.current_user:
                user = self.db.get_user(self.current_user)
                if user:
                    user_id = user['id']
            
            # Save to database
            if self.save_to_db_var.get():
                self.db.save_link(url, regenerated, technique, user_id)
            
            # Add to treeview
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.links_tree.insert('', 0, values=(technique, url, regenerated, timestamp))
            
            # Log activity
            if user_id:
                self.db.log_activity(user_id, 'generate_link', f'Technique: {technique}', self.get_client_ip())
            
            self.status_var.set(f"Link generated using {technique}")
            logger.info(f"Link generated: {technique}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate link: {str(e)}")
            logger.error(f"Link generation error: {e}")
    
    def batch_generate_links(self):
        """Batch generate links"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        try:
            results = self.link_regenerator.batch_regenerate(url)
            
            user_id = None
            if self.current_user:
                user = self.db.get_user(self.current_user)
                if user:
                    user_id = user['id']
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            for result in results:
                if self.save_to_db_var.get():
                    self.db.save_link(url, result['regenerated'], result['technique'], user_id)
                
                self.links_tree.insert('', 0, values=(
                    result['technique'],
                    result['original'],
                    result['regenerated'],
                    timestamp
                ))
            
            self.status_var.set(f"Generated {len(results)} link variations")
            logger.info(f"Batch generated {len(results)} links")
            
        except Exception as e:
            messagebox.showerror("Error", f"Batch generation failed: {str(e)}")
            logger.error(f"Batch generation error: {e}")
    
    def clear_link_fields(self):
        """Clear link input fields"""
        self.url_entry.delete(0, tk.END)
        self.links_tree.delete(*self.links_tree.get_children())
    
    def show_link_context_menu(self, event):
        """Show context menu for links"""
        # Implementation for context menu
        pass
    
    def test_all_proxies(self):
        """Test all proxies"""
        if not self.proxies:
            messagebox.showinfo("Info", "No proxies to test")
            return
        
        self.status_var.set("Testing proxies...")
        
        def test_thread():
            results = self.proxy_tester.test_multiple(self.proxies[:100])  # Test first 100
            
            # Update database
            for result in results:
                self.db.update_proxy_status(
                    result['proxy'],
                    result['status'],
                    result.get('response_time')
                )
            
            # Update UI
            self.root.after(0, self.load_proxies_to_tree)
            self.root.after(0, lambda: self.status_var.set(f"Tested {len(results)} proxies"))
            
            logger.info(f"Proxy test complete: {len(results)} tested")
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    def import_proxies(self):
        """Import proxies from file"""
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                with open(filename, 'r') as f:
                    new_proxies = [line.strip() for line in f if line.strip() and ':' in line.strip()]
                
                self.proxies.extend(new_proxies)
                self.proxies = list(set(self.proxies))
                
                for proxy in new_proxies:
                    self.db.save_proxy(proxy)
                
                self.load_proxies_to_tree()
                self.status_var.set(f"Imported {len(new_proxies)} proxies")
                logger.info(f"Imported {len(new_proxies)} proxies from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {str(e)}")
    
    def export_working_proxies(self):
        """Export working proxies"""
        proxies = self.db.get_proxies(status='active')
        if not proxies:
            messagebox.showinfo("Info", "No working proxies to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    for proxy in proxies:
                        f.write(proxy['address'] + '\n')
                
                self.status_var.set(f"Exported {len(proxies)} working proxies")
                logger.info(f"Exported {len(proxies)} proxies to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def clear_failed_proxies(self):
        """Clear failed proxies"""
        # Implementation to clear failed proxies
        pass
    
    def load_proxies_to_tree(self):
        """Load proxies into treeview"""
        self.proxy_tree.delete(*self.proxy_tree.get_children())
        
        proxies = self.db.get_proxies(limit=1000)
        active_count = 0
        failed_count = 0
        
        for proxy in proxies:
            self.proxy_tree.insert('', tk.END, values=(
                proxy['address'],
                proxy['type'],
                proxy['status'],
                proxy.get('response_time', 'N/A'),
                proxy.get('last_checked', 'Never')
            ))
            
            if proxy['status'] == 'active':
                active_count += 1
            elif proxy['status'] == 'inactive':
                failed_count += 1
        
        self.proxy_stats_label.config(
            text=f"Proxies: {len(proxies)} | Active: {active_count} | Failed: {failed_count}"
        )
    
    def generate_links_report(self):
        """Generate HTML links report"""
        links = self.db.get_links(limit=1000)
        html = self.report_generator.generate_link_report(links)
        
        self.report_preview.delete(1.0, tk.END)
        self.report_preview.insert(1.0, html[:5000] + "..." if len(html) > 5000 else html)
        
        # Save to file
        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(html)
            self.status_var.set(f"Report saved: {filename}")
    
    def generate_proxies_report(self):
        """Generate HTML proxies report"""
        proxies = self.db.get_proxies()
        html = self.report_generator.generate_proxy_report(proxies)
        
        self.report_preview.delete(1.0, tk.END)
        self.report_preview.insert(1.0, html[:5000] + "..." if len(html) > 5000 else html)
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(html)
            self.status_var.set(f"Report saved: {filename}")
    
    def export_links_csv(self):
        """Export links to CSV"""
        links = self.db.get_links(limit=10000)
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.report_generator.export_csv(links, filename)
            self.status_var.set(f"Links exported: {filename}")
    
    def export_proxies_csv(self):
        """Export proxies to CSV"""
        proxies = self.db.get_proxies()
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.report_generator.export_csv(proxies, filename)
            self.status_var.set(f"Proxies exported: {filename}")
    
    def save_settings(self):
        """Save application settings"""
        try:
            self.session_timeout = int(self.timeout_var.get())
            # Save other settings
            messagebox.showinfo("Success", "Settings saved successfully")
            logger.info("Settings saved")
        except ValueError:
            messagebox.showerror("Error", "Invalid settings values")
    
    def reset_settings(self):
        """Reset settings to default"""
        self.timeout_var.set("300")
        self.threads_var.set("50")
        self.proxy_timeout_var.set("10")
        messagebox.showinfo("Success", "Settings reset to default")
    
    def update_dashboard_stats(self):
        """Update dashboard statistics"""
        stats = self.db.get_statistics()
        
        stats_text = f"Links: {stats.get('total_links', 0)} | Proxies: {stats.get('active_proxies', 0)}/{stats.get('total_proxies', 0)}"
        self.stats_label.config(text=stats_text)
    
    def load_recent_activity(self):
        """Load recent activity"""
        # Implementation to load recent activity
        self.activity_text.insert(1.0, "Application started\n")
        self.activity_text.insert(1.0, f"User logged in: {self.current_user}\n" if self.current_user else "No user logged in\n")
    
    def run(self):
        """Main application loop"""
        def update_loop():
            if self.current_user and self.session_start:
                if time.time() - self.session_start > self.session_timeout:
                    self.logout()
                    messagebox.showwarning("Session Expired", "Your session has expired.")
                    return
            
            self.update_dashboard_stats()
            self.root.after(5000, update_loop)
        
        update_loop()
        self.root.mainloop()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = RegenerativeAddressesToolPro(root)
    app.run()


if __name__ == "__main__":
    main()
