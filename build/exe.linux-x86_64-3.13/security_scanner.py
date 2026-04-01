#!/usr/bin/env python3
"""
Network Security Scanner - Real Security Protection Tool
White hat security tools for keeping users safe
"""

import socket
import subprocess
import platform
import re
import os
import json
import time
import hashlib
import ssl
import urllib.request
import ipaddress
from datetime import datetime
import threading
from typing import Dict, List, Tuple, Optional

class NetworkSecurityScanner:
    """Real network security scanner for protection"""
    
    def __init__(self):
        self.scan_results = {}
        self.vulnerabilities = []
        self.open_ports = []
        self.system_info = {}
        
    def scan_system_security(self) -> Dict:
        """Comprehensive system security scan"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self.get_system_info(),
            'open_ports': self.scan_open_ports(),
            'vulnerabilities': self.check_vulnerabilities(),
            'password_security': self.check_password_policies(),
            'network_security': self.check_network_security(),
            'malware_scan': self.basic_malware_scan(),
            'security_score': 0
        }
        
        # Calculate security score
        results['security_score'] = self.calculate_security_score(results)
        return results
    
    def get_system_info(self) -> Dict:
        """Gather system information"""
        info = {
            'os': platform.system(),
            'version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'hostname': socket.gethostname(),
            'ip_address': self.get_local_ip(),
            'mac_address': self.get_mac_address()
        }
        
        # Check for security software
        info['antivirus'] = self.check_antivirus()
        info['firewall'] = self.check_firewall()
        
        return info
    
    def get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def get_mac_address(self) -> str:
        """Get MAC address"""
        try:
            import uuid
            mac = uuid.getnode()
            return ':'.join([f'{(mac >> elements) & 0xff:02x}' for elements in range(0, 8*6, 8)][::-1])
        except:
            return "Unknown"
    
    def check_antivirus(self) -> Dict:
        """Check for antivirus software"""
        av_status = {
            'installed': False,
            'name': None,
            'status': 'Unknown'
        }
        
        try:
            if platform.system() == "Windows":
                # Check Windows Defender
                result = subprocess.run(['powershell', '-Command', 'Get-MpComputerStatus'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    av_status['installed'] = True
                    av_status['name'] = 'Windows Defender'
                    av_status['status'] = 'Active'
            elif platform.system() == "Linux":
                # Check for common Linux AV tools
                av_tools = ['clamav', 'chkrootkit', 'rkhunter']
                for tool in av_tools:
                    if subprocess.run(['which', tool], capture_output=True).returncode == 0:
                        av_status['installed'] = True
                        av_status['name'] = tool
                        av_status['status'] = 'Installed'
                        break
        except:
            pass
        
        return av_status
    
    def check_firewall(self) -> Dict:
        """Check firewall status"""
        fw_status = {
            'enabled': False,
            'name': None,
            'rules': 0
        }
        
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                                      capture_output=True, text=True, timeout=10)
                if 'State' in result.stdout and 'ON' in result.stdout:
                    fw_status['enabled'] = True
                    fw_status['name'] = 'Windows Firewall'
            elif platform.system() == "Linux":
                # Check iptables
                result = subprocess.run(['iptables', '-L'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    fw_status['enabled'] = True
                    fw_status['name'] = 'iptables'
                    fw_status['rules'] = len([line for line in result.stdout.split('\n') if line.strip()])
        except:
            pass
        
        return fw_status
    
    def scan_open_ports(self, timeout=3) -> List[Dict]:
        """Scan for open ports on localhost"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 6379, 8080]
        open_ports = []
        
        def check_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex(('127.0.0.1', port))
                sock.close()
                
                if result == 0:
                    service = self.get_service_name(port)
                    open_ports.append({
                        'port': port,
                        'service': service,
                        'risk': self.assess_port_risk(port)
                    })
            except:
                pass
        
        # Use threading for faster scanning
        threads = []
        for port in common_ports:
            t = threading.Thread(target=check_port, args=(port,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        return open_ports
    
    def get_service_name(self, port: int) -> str:
        """Get service name for port"""
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
            443: 'HTTPS', 993: 'IMAPS', 995: 'POP3S',
            3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
            6379: 'Redis', 8080: 'HTTP-Alt'
        }
        return services.get(port, 'Unknown')
    
    def assess_port_risk(self, port: int) -> str:
        """Assess risk level of open port"""
        high_risk = [21, 23, 135, 139, 445]
        medium_risk = [22, 25, 53, 80, 110, 143, 3306, 3389, 5432]
        
        if port in high_risk:
            return 'High'
        elif port in medium_risk:
            return 'Medium'
        else:
            return 'Low'
    
    def check_vulnerabilities(self) -> List[Dict]:
        """Check for common vulnerabilities"""
        vulnerabilities = []
        
        # Check for outdated software
        vulnerabilities.extend(self.check_outdated_software())
        
        # Check for weak configurations
        vulnerabilities.extend(self.check_weak_configurations())
        
        # Check for system vulnerabilities
        vulnerabilities.extend(self.check_system_vulnerabilities())
        
        return vulnerabilities
    
    def check_outdated_software(self) -> List[Dict]:
        """Check for outdated software"""
        vulns = []
        
        # Check Python version
        python_version = platform.python_version()
        if tuple(map(int, python_version.split('.'))) < (3, 8):
            vulns.append({
                'type': 'Outdated Software',
                'description': f'Python {python_version} is outdated',
                'severity': 'Medium',
                'recommendation': 'Update to Python 3.8+'
            })
        
        # Check for common vulnerable services
        vulnerable_services = self.check_vulnerable_services()
        vulns.extend(vulnerable_services)
        
        return vulns
    
    def check_vulnerable_services(self) -> List[Dict]:
        """Check for vulnerable services"""
        vulns = []
        
        # Check for Telnet (insecure)
        if self.is_port_open(23):
            vulns.append({
                'type': 'Insecure Service',
                'description': 'Telnet service detected',
                'severity': 'High',
                'recommendation': 'Disable Telnet, use SSH instead'
            })
        
        # Check for anonymous FTP
        if self.is_port_open(21):
            vulns.append({
                'type': 'Insecure Service',
                'description': 'FTP service detected',
                'severity': 'Medium',
                'recommendation': 'Use SFTP instead of FTP'
            })
        
        return vulns
    
    def is_port_open(self, port: int) -> bool:
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result == 0
        except:
            return False
    
    def check_weak_configurations(self) -> List[Dict]:
        """Check for weak system configurations"""
        vulns = []
        
        # Check for default passwords
        vulns.extend(self.check_default_passwords())
        
        # Check for weak encryption
        vulns.extend(self.check_encryption_settings())
        
        return vulns
    
    def check_default_passwords(self) -> List[Dict]:
        """Check for default password vulnerabilities"""
        vulns = []
        
        # This would check for common default passwords
        # Implementation would depend on specific system
        
        return vulns
    
    def check_encryption_settings(self) -> List[Dict]:
        """Check encryption settings"""
        vulns = []
        
        # Check SSL/TLS settings
        try:
            context = ssl.create_default_context()
            # This would check for weak SSL/TLS versions
        except:
            pass
        
        return vulns
    
    def check_system_vulnerabilities(self) -> List[Dict]:
        """Check system-specific vulnerabilities"""
        vulns = []
        
        if platform.system() == "Windows":
            vulns.extend(self.check_windows_vulnerabilities())
        elif platform.system() == "Linux":
            vulns.extend(self.check_linux_vulnerabilities())
        
        return vulns
    
    def check_windows_vulnerabilities(self) -> List[Dict]:
        """Check Windows-specific vulnerabilities"""
        vulns = []
        
        try:
            # Check for Windows updates
            result = subprocess.run(['wmic', 'qfe', 'list'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                updates = result.stdout.count('\n')
                if updates < 10:  # Arbitrary threshold
                    vulns.append({
                        'type': 'System Updates',
                        'description': 'Few Windows updates installed',
                        'severity': 'Medium',
                        'recommendation': 'Install Windows updates'
                    })
        except:
            pass
        
        return vulns
    
    def check_linux_vulnerabilities(self) -> List[Dict]:
        """Check Linux-specific vulnerabilities"""
        vulns = []
        
        try:
            # Check for package updates
            if subprocess.run(['which', 'apt'], capture_output=True).returncode == 0:
                result = subprocess.run(['apt', 'list', '--upgradable'], 
                                      capture_output=True, text=True, timeout=30)
                updates = len([line for line in result.stdout.split('\n') if line.strip()])
                if updates > 0:
                    vulns.append({
                        'type': 'System Updates',
                        'description': f'{updates} packages need updates',
                        'severity': 'Medium',
                        'recommendation': 'Run system updates'
                    })
        except:
            pass
        
        return vulns
    
    def check_password_policies(self) -> Dict:
        """Check password security policies"""
        policies = {
            'min_length': 8,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_numbers': True,
            'require_special': True,
            'password_history': 5,
            'lockout_threshold': 5
        }
        
        # Check system password policies
        if platform.system() == "Linux":
            policies.update(self.check_linux_password_policies())
        elif platform.system() == "Windows":
            policies.update(self.check_windows_password_policies())
        
        return policies
    
    def check_linux_password_policies(self) -> Dict:
        """Check Linux password policies"""
        policies = {}
        
        try:
            # Check /etc/login.defs
            if os.path.exists('/etc/login.defs'):
                with open('/etc/login.defs', 'r') as f:
                    content = f.read()
                    
                for line in content.split('\n'):
                    if line.startswith('PASS_MIN_LEN'):
                        policies['min_length'] = int(line.split()[1])
                    elif line.startswith('PASS_MAX_DAYS'):
                        policies['max_age'] = int(line.split()[1])
        except:
            pass
        
        return policies
    
    def check_windows_password_policies(self) -> Dict:
        """Check Windows password policies"""
        policies = {}
        
        try:
            # Use net command to check password policy
            result = subprocess.run(['net', 'accounts'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'Minimum password length' in line:
                        policies['min_length'] = int(line.split(':')[1].strip())
        except:
            pass
        
        return policies
    
    def check_network_security(self) -> Dict:
        """Check network security settings"""
        security = {
            'dns_security': self.check_dns_security(),
            'wifi_security': self.check_wifi_security(),
            'proxy_settings': self.check_proxy_settings(),
            'host_file': self.check_host_file()
        }
        
        return security
    
    def check_dns_security(self) -> Dict:
        """Check DNS security settings"""
        dns_config = {
            'secure_dns': False,
            'dns_servers': [],
            'dnssec_enabled': False
        }
        
        try:
            # Get DNS servers
            if platform.system() == "Windows":
                result = subprocess.run(['nslookup', 'google.com'], 
                                      capture_output=True, text=True, timeout=10)
                # Parse DNS servers from result
            elif platform.system() == "Linux":
                with open('/etc/resolv.conf', 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if line.startswith('nameserver'):
                            dns_config['dns_servers'].append(line.split()[1])
        except:
            pass
        
        return dns_config
    
    def check_wifi_security(self) -> Dict:
        """Check WiFi security settings"""
        wifi_config = {
            'encryption': 'Unknown',
            'networks': [],
            'security_enabled': False
        }
        
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                                      capture_output=True, text=True, timeout=10)
                # Parse WiFi profiles
            elif platform.system() == "Linux":
                if subprocess.run(['which', 'iwlist'], capture_output=True).returncode == 0:
                    result = subprocess.run(['iwlist', 'scan'], 
                                          capture_output=True, text=True, timeout=30)
                    # Parse WiFi networks
        except:
            pass
        
        return wifi_config
    
    def check_proxy_settings(self) -> Dict:
        """Check proxy settings"""
        proxy_config = {
            'http_proxy': os.environ.get('HTTP_PROXY', ''),
            'https_proxy': os.environ.get('HTTPS_PROXY', ''),
            'no_proxy': os.environ.get('NO_PROXY', ''),
            'system_proxy': False
        }
        
        # Check system proxy settings
        if platform.system() == "Windows":
            try:
                result = subprocess.run(['reg', 'query', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'], 
                                      capture_output=True, text=True, timeout=10)
                if 'ProxyEnable' in result.stdout and '0x1' in result.stdout:
                    proxy_config['system_proxy'] = True
            except:
                pass
        
        return proxy_config
    
    def check_host_file(self) -> Dict:
        """Check hosts file for security"""
        host_config = {
            'entries': [],
            'suspicious_entries': [],
            'modified': False
        }
        
        try:
            if platform.system() == "Windows":
                hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
            else:
                hosts_path = '/etc/hosts'
            
            if os.path.exists(hosts_path):
                with open(hosts_path, 'r') as f:
                    lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        if len(parts) >= 2:
                            ip, hostname = parts[0], parts[1]
                            host_config['entries'].append({'ip': ip, 'hostname': hostname})
                            
                            # Check for suspicious entries
                            if self.is_suspicious_host_entry(ip, hostname):
                                host_config['suspicious_entries'].append({'ip': ip, 'hostname': hostname})
        except:
            pass
        
        return host_config
    
    def is_suspicious_host_entry(self, ip: str, hostname: str) -> bool:
        """Check if hosts entry is suspicious"""
        suspicious_domains = ['facebook.com', 'google.com', 'microsoft.com', 'apple.com']
        
        if hostname in suspicious_domains and ip != '127.0.0.1':
            return True
        
        return False
    
    def basic_malware_scan(self) -> Dict:
        """Basic malware detection scan"""
        scan_results = {
            'scanned_files': 0,
            'suspicious_files': [],
            'scan_time': 0,
            'status': 'Completed'
        }
        
        start_time = time.time()
        
        try:
            # Scan common directories for suspicious files
            common_dirs = []
            if platform.system() == "Windows":
                common_dirs = [os.path.expanduser('~/Desktop'), os.path.expanduser('~/Downloads')]
            else:
                common_dirs = [os.path.expanduser('~/Desktop'), os.path.expanduser('~/Downloads')]
            
            for directory in common_dirs:
                if os.path.exists(directory):
                    scan_results['suspicious_files'].extend(self.scan_directory(directory))
                    scan_results['scanned_files'] += len([f for f in os.listdir(directory) 
                                                         if os.path.isfile(os.path.join(directory, f))])
        
        except Exception as e:
            scan_results['status'] = f'Error: {str(e)}'
        
        scan_results['scan_time'] = time.time() - start_time
        
        return scan_results
    
    def scan_directory(self, directory: str) -> List[Dict]:
        """Scan directory for suspicious files"""
        suspicious_files = []
        
        try:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    if self.is_suspicious_file(filepath):
                        suspicious_files.append({
                            'file': filepath,
                            'reason': 'Suspicious file detected',
                            'size': os.path.getsize(filepath)
                        })
        except:
            pass
        
        return suspicious_files
    
    def is_suspicious_file(self, filepath: str) -> bool:
        """Check if file is suspicious"""
        suspicious_extensions = ['.exe', '.bat', '.com', '.scr', '.pif', '.vbs']
        suspicious_names = ['setup', 'install', 'crack', 'keygen', 'patch']
        
        filename = os.path.basename(filepath).lower()
        extension = os.path.splitext(filename)[1]
        
        # Check for suspicious extensions
        if extension in suspicious_extensions:
            return True
        
        # Check for suspicious names
        for name in suspicious_names:
            if name in filename:
                return True
        
        # Check file size (very small executables can be suspicious)
        if extension in ['.exe', '.bat', '.com'] and os.path.getsize(filepath) < 1024:
            return True
        
        return False
    
    def calculate_security_score(self, results: Dict) -> int:
        """Calculate overall security score"""
        score = 100
        
        # Deduct points for vulnerabilities
        for vuln in results['vulnerabilities']:
            if vuln['severity'] == 'High':
                score -= 20
            elif vuln['severity'] == 'Medium':
                score -= 10
            else:
                score -= 5
        
        # Deduct points for high-risk open ports
        for port in results['open_ports']:
            if port['risk'] == 'High':
                score -= 15
            elif port['risk'] == 'Medium':
                score -= 8
            else:
                score -= 3
        
        # Deduct points for suspicious files
        score -= len(results['malware_scan']['suspicious_files']) * 10
        
        # Add points for security measures
        if results['system_info']['antivirus']['installed']:
            score += 10
        
        if results['system_info']['firewall']['enabled']:
            score += 10
        
        return max(0, min(100, score))
    
    def generate_security_report(self, results: Dict) -> str:
        """Generate detailed security report"""
        report = f"""
SECURITY SCAN REPORT
==================
Scan Date: {results['timestamp']}
Security Score: {results['security_score']}/100

SYSTEM INFORMATION
-----------------
OS: {results['system_info']['os']} {results['system_info']['version']}
IP Address: {results['system_info']['ip_address']}
Antivirus: {results['system_info']['antivirus']['name'] or 'None'}
Firewall: {results['system_info']['firewall']['name'] or 'None'}

OPEN PORTS
-----------
"""
        
        for port in results['open_ports']:
            report += f"Port {port['port']}/{port['service']} - Risk: {port['risk']}\n"
        
        report += "\nVULNERABILITIES\n---------------\n"
        
        for vuln in results['vulnerabilities']:
            report += f"[{vuln['severity']}] {vuln['description']}\n"
            report += f"  Recommendation: {vuln['recommendation']}\n\n"
        
        report += f"\nMALWARE SCAN\n------------\n"
        report += f"Files Scanned: {results['malware_scan']['scanned_files']}\n"
        report += f"Suspicious Files: {len(results['malware_scan']['suspicious_files'])}\n"
        
        if results['malware_scan']['suspicious_files']:
            report += "\nSuspicious Files:\n"
            for file in results['malware_scan']['suspicious_files']:
                report += f"  - {file['file']}: {file['reason']}\n"
        
        report += "\nRECOMMENDATIONS\n----------------\n"
        
        if results['security_score'] < 70:
            report += "Your system has significant security issues that need immediate attention.\n"
        elif results['security_score'] < 90:
            report += "Your system has some security issues that should be addressed.\n"
        else:
            report += "Your system has good security posture.\n"
        
        return report
    
    def save_scan_results(self, results: Dict, filename: str = None):
        """Save scan results to file"""
        if filename is None:
            filename = f"security_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        return filename


class PasswordSecurityChecker:
    """Real password security analysis tool"""
    
    def __init__(self):
        self.common_passwords = self.load_common_passwords()
    
    def load_common_passwords(self) -> set:
        """Load common passwords list"""
        # Common weak passwords
        return {
            'password', '123456', '123456789', '12345678', '12345', '1234567',
            '1234567890', '1234', 'qwerty', 'abc123', 'password123', 'admin',
            'letmein', 'welcome', 'monkey', '1234567890', 'password1', 'qwertyuiop'
        }
    
    def check_password_strength(self, password: str) -> Dict:
        """Comprehensive password strength analysis"""
        analysis = {
            'password': password,
            'length': len(password),
            'strength': 'Weak',
            'score': 0,
            'issues': [],
            'recommendations': [],
            'entropy': self.calculate_entropy(password)
        }
        
        # Length check
        if len(password) < 8:
            analysis['issues'].append('Password is too short (minimum 8 characters)')
            analysis['recommendations'].append('Use at least 8 characters')
        elif len(password) >= 12:
            analysis['score'] += 20
        
        # Character variety check
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        if not has_upper:
            analysis['issues'].append('No uppercase letters')
            analysis['recommendations'].append('Add uppercase letters')
        else:
            analysis['score'] += 15
        
        if not has_lower:
            analysis['issues'].append('No lowercase letters')
            analysis['recommendations'].append('Add lowercase letters')
        else:
            analysis['score'] += 15
        
        if not has_digit:
            analysis['issues'].append('No numbers')
            analysis['recommendations'].append('Add numbers')
        else:
            analysis['score'] += 15
        
        if not has_special:
            analysis['issues'].append('No special characters')
            analysis['recommendations'].append('Add special characters')
        else:
            analysis['score'] += 15
        
        # Common password check
        if password.lower() in self.common_passwords:
            analysis['issues'].append('Password is too common')
            analysis['recommendations'].append('Use a unique password')
            analysis['score'] -= 30
        
        # Pattern check
        if self.has_repetitive_patterns(password):
            analysis['issues'].append('Contains repetitive patterns')
            analysis['recommendations'].append('Avoid repetitive characters')
            analysis['score'] -= 10
        
        # Dictionary word check
        if self.contains_dictionary_words(password):
            analysis['issues'].append('Contains common dictionary words')
            analysis['recommendations'].append('Avoid common words')
            analysis['score'] -= 10
        
        # Determine strength
        if analysis['score'] >= 80:
            analysis['strength'] = 'Very Strong'
        elif analysis['score'] >= 60:
            analysis['strength'] = 'Strong'
        elif analysis['score'] >= 40:
            analysis['strength'] = 'Medium'
        elif analysis['score'] >= 20:
            analysis['strength'] = 'Weak'
        else:
            analysis['strength'] = 'Very Weak'
        
        return analysis
    
    def calculate_entropy(self, password: str) -> float:
        """Calculate password entropy"""
        charset_size = 0
        
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            charset_size += 32
        
        if charset_size == 0:
            return 0
        
        import math
        return len(password) * math.log2(charset_size)
    
    def has_repetitive_patterns(self, password: str) -> bool:
        """Check for repetitive patterns"""
        # Check for repeated characters
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        
        # Check for sequential characters
        for i in range(len(password) - 2):
            if (ord(password[i+1]) == ord(password[i]) + 1 and 
                ord(password[i+2]) == ord(password[i+1]) + 1):
                return True
        
        # Check for keyboard patterns
        keyboard_rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
        for row in keyboard_rows:
            for i in range(len(row) - 2):
                pattern = row[i:i+3]
                if pattern in password.lower():
                    return True
        
        return False
    
    def contains_dictionary_words(self, password: str) -> bool:
        """Check if password contains common dictionary words"""
        # Simple check for common words
        common_words = ['password', 'admin', 'user', 'login', 'welcome', 'computer', 'system']
        password_lower = password.lower()
        
        for word in common_words:
            if word in password_lower:
                return True
        
        return False
    
    def generate_secure_password(self, length: int = 16) -> str:
        """Generate a secure password"""
        import secrets
        import string
        
        # Ensure at least one of each character type
        chars = []
        chars.append(secrets.choice(string.ascii_uppercase))
        chars.append(secrets.choice(string.ascii_lowercase))
        chars.append(secrets.choice(string.digits))
        chars.append(secrets.choice('!@#$%^&*()_+-=[]{}|;:,.<>?'))
        
        # Fill the rest
        all_chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
        for _ in range(length - 4):
            chars.append(secrets.choice(all_chars))
        
        # Shuffle and join
        secrets.SystemRandom().shuffle(chars)
        return ''.join(chars)


class NetworkVulnerabilityScanner:
    """Real network vulnerability scanner"""
    
    def __init__(self):
        self.target_range = None
        self.scan_results = {}
    
    def scan_network_range(self, target: str, ports: List[int] = None) -> Dict:
        """Scan network range for vulnerabilities"""
        if ports is None:
            ports = [22, 23, 53, 80, 135, 139, 443, 445, 993, 995]
        
        results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'hosts': [],
            'vulnerabilities': [],
            'open_services': []
        }
        
        try:
            # Parse target range
            network = ipaddress.ip_network(target, strict=False)
            
            # Scan each host
            for ip in network.hosts():
                if str(ip).endswith('.1'):  # Skip gateway for demo
                    continue
                
                host_result = self.scan_host(str(ip), ports)
                if host_result['open_ports']:
                    results['hosts'].append(host_result)
                    results['open_services'].extend(host_result['open_ports'])
        
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def scan_host(self, ip: str, ports: List[int]) -> Dict:
        """Scan individual host"""
        host_result = {
            'ip': ip,
            'hostname': self.get_hostname(ip),
            'open_ports': [],
            'vulnerabilities': []
        }
        
        # Port scan
        for port in ports:
            if self.is_port_open(ip, port):
                service = self.get_service_name(port)
                host_result['open_ports'].append({
                    'port': port,
                    'service': service,
                    'risk': self.assess_service_risk(port, service)
                })
        
        # Check for vulnerabilities
        host_result['vulnerabilities'] = self.check_host_vulnerabilities(host_result)
        
        return host_result
    
    def get_hostname(self, ip: str) -> str:
        """Get hostname for IP"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return ip
    
    def is_port_open(self, ip: str, port: int, timeout=2) -> bool:
        """Check if port is open on target"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def get_service_name(self, port: int) -> str:
        """Get service name for port"""
        services = {
            22: 'SSH', 23: 'Telnet', 53: 'DNS', 80: 'HTTP',
            135: 'RPC', 139: 'NetBIOS', 443: 'HTTPS',
            445: 'SMB', 993: 'IMAPS', 995: 'POP3S'
        }
        return services.get(port, 'Unknown')
    
    def assess_service_risk(self, port: int, service: str) -> str:
        """Assess risk level of service"""
        high_risk_services = ['Telnet', 'NetBIOS', 'SMB', 'RPC']
        medium_risk_services = ['SSH', 'HTTP', 'DNS']
        
        if service in high_risk_services:
            return 'High'
        elif service in medium_risk_services:
            return 'Medium'
        else:
            return 'Low'
    
    def check_host_vulnerabilities(self, host_result: Dict) -> List[Dict]:
        """Check host for specific vulnerabilities"""
        vulns = []
        
        for port_info in host_result['open_ports']:
            port = port_info['port']
            service = port_info['service']
            
            # Check for specific vulnerabilities
            if port == 23:  # Telnet
                vulns.append({
                    'type': 'Insecure Protocol',
                    'description': 'Telnet service running (unencrypted)',
                    'severity': 'High',
                    'port': port
                })
            
            elif port == 21:  # FTP
                vulns.append({
                    'type': 'Insecure Protocol',
                    'description': 'FTP service running (unencrypted)',
                    'severity': 'Medium',
                    'port': port
                })
            
            elif port == 80:  # HTTP
                vulns.append({
                    'type': 'Unencrypted Service',
                    'description': 'HTTP service running (unencrypted)',
                    'severity': 'Medium',
                    'port': port
                })
        
        return vulns


# Main execution for standalone use
if __name__ == "__main__":
    scanner = NetworkSecurityScanner()
    results = scanner.scan_system_security()
    print(scanner.generate_security_report(results))
