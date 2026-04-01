#!/usr/bin/env python3
"""
System Hardening Tool - Real Security Protection
White hat system hardening utilities
"""

import os
import sys
import subprocess
import platform
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple

class SystemHardener:
    """Real system hardening tool for security protection"""
    
    def __init__(self):
        self.system_os = platform.system()
        self.hardening_log = []
        self.backup_created = False
    
    def create_system_backup(self) -> bool:
        """Create backup before hardening"""
        try:
            backup_dir = f"system_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup important configuration files
            if self.system_os == "Linux":
                config_files = ['/etc/ssh/sshd_config', '/etc/sysctl.conf', '/etc/passwd']
                for config_file in config_files:
                    if os.path.exists(config_file):
                        backup_path = os.path.join(backup_dir, config_file.replace('/', '_'))
                        subprocess.run(['cp', config_file, backup_path])
            
            self.backup_created = True
            self.log_action("System backup created", f"Backup directory: {backup_dir}")
            return True
            
        except Exception as e:
            self.log_action("Backup failed", str(e))
            return False
    
    def log_action(self, action: str, details: str):
        """Log hardening actions"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details
        }
        self.hardening_log.append(log_entry)
    
    def harden_system(self) -> Dict:
        """Comprehensive system hardening"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'system_os': self.system_os,
            'hardening_applied': [],
            'warnings': [],
            'success': False
        }
        
        # Create backup first
        if not self.create_system_backup():
            results['warnings'].append("Failed to create system backup")
        
        try:
            if self.system_os == "Linux":
                results.update(self.harden_linux())
            elif self.system_os == "Windows":
                results.update(self.harden_windows())
            else:
                results['warnings'].append("Unsupported operating system")
                return results
            
            results['success'] = True
            
        except Exception as e:
            results['warnings'].append(f"Hardening failed: {str(e)}")
        
        return results
    
    def harden_linux(self) -> Dict:
        """Linux system hardening"""
        results = {
            'ssh_hardening': self.harden_ssh(),
            'firewall_hardening': self.harden_linux_firewall(),
            'system_hardening': self.harden_linux_system(),
            'network_hardening': self.harden_linux_network(),
            'user_hardening': self.harden_linux_users()
        }
        
        return results
    
    def harden_ssh(self) -> Dict:
        """Harden SSH configuration"""
        ssh_config = "/etc/ssh/sshd_config"
        if not os.path.exists(ssh_config):
            return {'status': 'SSH config not found'}
        
        hardening_changes = []
        
        try:
            # Read current config
            with open(ssh_config, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            changes_made = []
            
            for line in lines:
                # SSH hardening rules
                if line.strip().startswith('#') or '=' not in line:
                    new_lines.append(line)
                    continue
                
                key, value = line.strip().split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Apply hardening rules
                if key == 'PermitRootLogin' and value != 'no':
                    new_lines.append('PermitRootLogin=no\n')
                    changes_made.append('Disabled root login via SSH')
                elif key == 'PasswordAuthentication' and value != 'no':
                    new_lines.append('PasswordAuthentication=no\n')
                    changes_made.append('Disabled password authentication')
                elif key == 'PermitEmptyPasswords' and value != 'no':
                    new_lines.append('PermitEmptyPasswords=no\n')
                    changes_made.append('Disabled empty passwords')
                elif key == 'Protocol' and value != '2':
                    new_lines.append('Protocol=2\n')
                    changes_made.append('Enforced SSH protocol 2')
                elif key == 'MaxAuthTries' and int(value) > 3:
                    new_lines.append('MaxAuthTries=3\n')
                    changes_made.append('Limited authentication attempts to 3')
                elif key == 'ClientAliveInterval' and int(value) > 300:
                    new_lines.append('ClientAliveInterval=300\n')
                    changes_made.append('Set client alive interval to 300')
                else:
                    new_lines.append(line)
            
            # Add new hardening options if not present
            config_keys = [line.split('=')[0].strip() for line in new_lines if '=' in line and not line.strip().startswith('#')]
            
            if 'PermitRootLogin' not in config_keys:
                new_lines.append('PermitRootLogin=no\n')
                changes_made.append('Disabled root login via SSH')
            
            if 'PasswordAuthentication' not in config_keys:
                new_lines.append('PasswordAuthentication=no\n')
                changes_made.append('Disabled password authentication')
            
            if 'Protocol' not in config_keys:
                new_lines.append('Protocol=2\n')
                changes_made.append('Enforced SSH protocol 2')
            
            # Write new config
            with open(ssh_config, 'w') as f:
                f.writelines(new_lines)
            
            # Restart SSH service
            try:
                subprocess.run(['systemctl', 'restart', 'sshd'], check=True)
                changes_made.append('SSH service restarted')
            except:
                changes_made.append('SSH service restart failed - manual restart required')
            
            for change in changes_made:
                self.log_action("SSH Hardening", change)
            
            return {
                'status': 'success',
                'changes': changes_made
            }
            
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def harden_linux_firewall(self) -> Dict:
        """Harden Linux firewall"""
        changes = []
        
        try:
            # Check if ufw is available
            if subprocess.run(['which', 'ufw'], capture_output=True).returncode == 0:
                # Enable ufw
                subprocess.run(['ufw', '--force', 'enable'], check=True)
                changes.append('UFW firewall enabled')
                
                # Set default policies
                subprocess.run(['ufw', 'default', 'deny', 'incoming'], check=True)
                subprocess.run(['ufw', 'default', 'allow', 'outgoing'], check=True)
                changes.append('Set default firewall policies')
                
                # Allow essential services
                subprocess.run(['ufw', 'allow', 'ssh'], check=True)
                changes.append('SSH allowed through firewall')
                
                self.log_action("Firewall Hardening", "UFW configured")
                
            else:
                # Try iptables
                subprocess.run(['iptables', '-P', 'INPUT', 'DROP'], check=True)
                subprocess.run(['iptables', '-P', 'FORWARD', 'DROP'], check=True)
                subprocess.run(['iptables', '-P', 'OUTPUT', 'ACCEPT'], check=True)
                changes.append('iptables default policies set')
                
                self.log_action("Firewall Hardening", "iptables configured")
            
            return {
                'status': 'success',
                'changes': changes
            }
            
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def harden_linux_system(self) -> Dict:
        """Harden Linux system settings"""
        changes = []
        
        try:
            # Secure shared memory
            if os.path.exists('/etc/fstab'):
                with open('/etc/fstab', 'r') as f:
                    fstab_content = f.read()
                
                if 'tmpfs /dev/shm tmpfs defaults,noexec,nosuid 0 0' not in fstab_content:
                    with open('/etc/fstab', 'a') as f:
                        f.write('\ntmpfs /dev/shm tmpfs defaults,noexec,nosuid 0 0\n')
                    changes.append('Secured shared memory (noexec,nosuid)')
            
            # Disable unused filesystems
            sysctl_changes = [
                ('fs.suid_dumpable', '0'),
                ('kernel.dmesg_restrict', '1'),
                ('net.ipv4.ip_forward', '0'),
                ('net.ipv4.conf.all.send_redirects', '0'),
                ('net.ipv4.conf.default.send_redirects', '0'),
                ('net.ipv4.conf.all.accept_source_route', '0'),
                ('net.ipv4.conf.default.accept_source_route', '0'),
                ('net.ipv4.conf.all.accept_redirects', '0'),
                ('net.ipv4.conf.default.accept_redirects', '0')
            ]
            
            sysctl_file = '/etc/sysctl.conf'
            if os.path.exists(sysctl_file):
                with open(sysctl_file, 'r') as f:
                    sysctl_content = f.read()
                
                for setting, value in sysctl_changes:
                    if f"{setting} = {value}" not in sysctl_content:
                        with open(sysctl_file, 'a') as f:
                            f.write(f"\n{setting} = {value}\n")
                        changes.append(f'Applied sysctl setting: {setting}')
                
                # Apply sysctl settings
                subprocess.run(['sysctl', '-p'], check=True)
                changes.append('Applied sysctl settings')
            
            # Secure file permissions
            critical_files = [
                ('/etc/passwd', 644),
                ('/etc/shadow', 600),
                ('/etc/group', 644),
                ('/etc/gshadow', 640)
            ]
            
            for file_path, perm in critical_files:
                if os.path.exists(file_path):
                    os.chmod(file_path, perm)
                    changes.append(f'Set permissions for {file_path}')
            
            for change in changes:
                self.log_action("System Hardening", change)
            
            return {
                'status': 'success',
                'changes': changes
            }
            
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def harden_linux_network(self) -> Dict:
        """Harden Linux network settings"""
        changes = []
        
        try:
            # Disable unused network services
            services_to_disable = ['telnet', 'rsh', 'rlogin', 'ypbind', 'portmap']
            
            for service in services_to_disable:
                try:
                    subprocess.run(['systemctl', 'disable', service], check=False)
                    subprocess.run(['systemctl', 'stop', service], check=False)
                    changes.append(f'Disabled service: {service}')
                except:
                    pass
            
            # Configure network interface security
            try:
                # Disable IP source routing
                subprocess.run(['sysctl', '-w', 'net.ipv4.conf.all.accept_source_route=0'], check=True)
                changes.append('Disabled IP source routing')
                
                # Disable ICMP redirects
                subprocess.run(['sysctl', '-w', 'net.ipv4.conf.all.accept_redirects=0'], check=True)
                changes.append('Disabled ICMP redirects')
                
            except:
                changes.append('Network hardening partially applied')
            
            for change in changes:
                self.log_action("Network Hardening", change)
            
            return {
                'status': 'success',
                'changes': changes
            }
            
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def harden_linux_users(self) -> Dict:
        """Harden Linux user accounts"""
        changes = []
        
        try:
            # Check for accounts with no passwords
            try:
                result = subprocess.run(['awk', '-F:', '($2 == "") {print $1}', '/etc/shadow'], 
                                      capture_output=True, text=True)
                if result.stdout.strip():
                    accounts = result.stdout.strip().split('\n')
                    for account in accounts:
                        changes.append(f'Account with no password: {account}')
            except:
                pass
            
            # Check for accounts with UID 0 (root)
            try:
                result = subprocess.run(['awk', '-F:', '($3 == "0") {print $1}', '/etc/passwd'], 
                                      capture_output=True, text=True)
                root_accounts = result.stdout.strip().split('\n')
                if len(root_accounts) > 1:
                    changes.append(f'Multiple root accounts found: {root_accounts}')
            except:
                pass
            
            # Set password policies
            if os.path.exists('/etc/login.defs'):
                with open('/etc/login.defs', 'r') as f:
                    login_defs = f.read()
                
                policies = [
                    ('PASS_MIN_LEN', '8'),
                    ('PASS_MAX_DAYS', '90'),
                    ('PASS_MIN_DAYS', '1'),
                    ('PASS_WARN_AGE', '7')
                ]
                
                for policy, value in policies:
                    if policy not in login_defs:
                        with open('/etc/login.defs', 'a') as f:
                            f.write(f'\n{policy} {value}\n')
                        changes.append(f'Set password policy: {policy} = {value}')
            
            for change in changes:
                self.log_action("User Hardening", change)
            
            return {
                'status': 'success',
                'changes': changes
            }
            
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def harden_windows(self) -> Dict:
        """Windows system hardening"""
        results = {
            'firewall_hardening': self.harden_windows_firewall(),
            'user_hardening': self.harden_windows_users(),
            'policy_hardening': self.harden_windows_policies(),
            'network_hardening': self.harden_windows_network()
        }
        
        return results
    
    def harden_windows_firewall(self) -> Dict:
        """Harden Windows firewall"""
        changes = []
        
        try:
            # Enable Windows Firewall for all profiles
            subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'on'], check=True)
            changes.append('Windows Firewall enabled for all profiles')
            
            # Set default block behavior
            subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'firewallpolicy', 'blockinboundalways', 'yes'], check=True)
            changes.append('Set default block inbound behavior')
            
            # Enable logging
            subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'logging', 'allowedconnections', 'enable'], check=True)
            changes.append('Enabled firewall logging')
            
            for change in changes:
                self.log_action("Windows Firewall Hardening", change)
            
            return {
                'status': 'success',
                'changes': changes
            }
            
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def harden_windows_users(self) -> Dict:
        """Harden Windows user accounts"""
        changes = []
        
        try:
            # Check for accounts with no passwords
            result = subprocess.run(['net', 'user'], capture_output=True, text=True)
            
            for line in result.stdout.split('\n'):
                if 'The command completed' in line:
                    break
                
                parts = line.split()
                if len(parts) >= 2:
                    username = parts[0]
                    
                    # Check if account is active
                    if 'active' in line.lower():
                        # Additional user hardening would go here
                        changes.append(f'User account found: {username}')
            
            # Set account lockout policy
            try:
                subprocess.run(['net', 'accounts', 'lockoutthreshold', '5'], check=True)
                subprocess.run(['net', 'accounts', 'lockoutduration', '30'], check=True)
                changes.append('Set account lockout policy (5 attempts, 30 min duration)')
            except:
                changes.append('Failed to set account lockout policy')
            
            for change in changes:
                self.log_action("Windows User Hardening", change)
            
            return {
                'status': 'success',
                'changes': changes
            }
            
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def harden_windows_policies(self) -> Dict:
        """Harden Windows security policies"""
        changes = []
        
        try:
            # Enable Windows Defender (if available)
            try:
                subprocess.run(['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $false'], check=True)
                changes.append('Windows Defender real-time monitoring enabled')
            except:
                changes.append('Windows Defender configuration failed')
            
            # Set UAC level
            try:
                subprocess.run(['reg', 'add', 'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System', 
                              '/v', 'EnableLUA', '/t', 'REG_DWORD', '/d', '1', '/f'], check=True)
                changes.append('UAC enabled')
            except:
                changes.append('UAC configuration failed')
            
            for change in changes:
                self.log_action("Windows Policy Hardening", change)
            
            return {
                'status': 'success',
                'changes': changes
            }
            
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def harden_windows_network(self) -> Dict:
        """Harden Windows network settings"""
        changes = []
        
        try:
            # Disable unnecessary services
            services_to_disable = ['Telnet', 'Remote Registry']
            
            for service in services_to_disable:
                try:
                    subprocess.run(['sc', 'config', service, 'start=disabled'], check=False)
                    subprocess.run(['sc', 'stop', service], check=False)
                    changes.append(f'Disabled service: {service}')
                except:
                    pass
            
            # Configure network adapter settings
            try:
                subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=restricted'], check=True)
                changes.append('Set TCP autotuning to restricted')
            except:
                changes.append('TCP configuration failed')
            
            for change in changes:
                self.log_action("Windows Network Hardening", change)
            
            return {
                'status': 'success',
                'changes': changes
            }
            
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def generate_hardening_report(self, results: Dict) -> str:
        """Generate hardening report"""
        report = f"""
SYSTEM HARDENING REPORT
======================
Date: {results['timestamp']}
OS: {results['system_os']}
Status: {'Success' if results['success'] else 'Failed'}

HARDENING APPLIED:
"""
        
        if self.system_os == "Linux":
            for category, data in results.items():
                if isinstance(data, dict) and 'changes' in data:
                    report += f"\n{category.upper()}:\n"
                    for change in data['changes']:
                        report += f"  ✓ {change}\n"
        
        elif self.system_os == "Windows":
            for category, data in results.items():
                if isinstance(data, dict) and 'changes' in data:
                    report += f"\n{category.upper()}:\n"
                    for change in data['changes']:
                        report += f"  ✓ {change}\n"
        
        if results['warnings']:
            report += "\nWARNINGS:\n"
            for warning in results['warnings']:
                report += f"  ⚠ {warning}\n"
        
        report += f"\nACTIONS LOGGED: {len(self.hardening_log)}\n"
        report += f"BACKUP CREATED: {'Yes' if self.backup_created else 'No'}\n"
        
        return report
    
    def save_hardening_log(self, filename: str = None):
        """Save hardening log to file"""
        if filename is None:
            filename = f"hardening_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'system_os': self.system_os,
            'backup_created': self.backup_created,
            'actions': self.hardening_log
        }
        
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return filename


class SecurityAuditTool:
    """Real security audit tool"""
    
    def __init__(self):
        self.audit_results = {}
    
    def perform_security_audit(self) -> Dict:
        """Comprehensive security audit"""
        audit = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self.audit_system_info(),
            'file_permissions': self.audit_file_permissions(),
            'user_accounts': self.audit_user_accounts(),
            'network_services': self.audit_network_services(),
            'security_policies': self.audit_security_policies(),
            'audit_score': 0
        }
        
        # Calculate audit score
        audit['audit_score'] = self.calculate_audit_score(audit)
        
        return audit
    
    def audit_system_info(self) -> Dict:
        """Audit system information"""
        info = {
            'os': platform.system(),
            'version': platform.version(),
            'architecture': platform.architecture()[0],
            'hostname': platform.node(),
            'uptime': self.get_system_uptime(),
            'last_boot': self.get_last_boot_time(),
            'security_patches': self.check_security_patches()
        }
        
        return info
    
    def get_system_uptime(self) -> str:
        """Get system uptime"""
        try:
            if platform.system() == "Linux":
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.read().split()[0])
                    days = int(uptime_seconds // 86400)
                    hours = int((uptime_seconds % 86400) // 3600)
                    return f"{days} days, {hours} hours"
            elif platform.system() == "Windows":
                result = subprocess.run(['wmic', 'os', 'get', 'lastbootuptime'], 
                                      capture_output=True, text=True, timeout=10)
                # Parse Windows uptime
                return "Windows uptime data"
        except:
            pass
        
        return "Unknown"
    
    def get_last_boot_time(self) -> str:
        """Get last boot time"""
        try:
            if platform.system() == "Linux":
                with open('/proc/stat', 'r') as f:
                    for line in f:
                        if line.startswith('btime'):
                            boot_time = int(line.split()[1])
                            return datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass
        
        return "Unknown"
    
    def check_security_patches(self) -> Dict:
        """Check for security patches"""
        patches = {
            'total_patches': 0,
            'security_patches': 0,
            'last_update': 'Unknown',
            'missing_critical': []
        }
        
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['wmic', 'qfe', 'list'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    patches['total_patches'] = result.stdout.count('\n') - 2
            elif platform.system() == "Linux":
                if subprocess.run(['which', 'apt'], capture_output=True).returncode == 0:
                    result = subprocess.run(['apt', 'list', '--upgradable'], 
                                          capture_output=True, text=True, timeout=30)
                    patches['missing_critical'] = len([line for line in result.stdout.split('\n') if line.strip()])
        except:
            pass
        
        return patches
    
    def audit_file_permissions(self) -> Dict:
        """Audit critical file permissions"""
        permissions = {
            'critical_files': [],
            'world_writable': [],
            'suid_files': [],
            'sgid_files': []
        }
        
        try:
            if platform.system() == "Linux":
                # Check critical files
                critical_files = ['/etc/passwd', '/etc/shadow', '/etc/group', '/etc/gshadow']
                for file_path in critical_files:
                    if os.path.exists(file_path):
                        stat_info = os.stat(file_path)
                        permissions['critical_files'].append({
                            'file': file_path,
                            'permissions': oct(stat_info.st_mode)[-3:],
                            'owner': stat_info.st_uid,
                            'group': stat_info.st_gid
                        })
                
                # Find world-writable files
                result = subprocess.run(['find', '/', '-type', 'f', '-perm', '/o+w'], 
                                      capture_output=True, text=True, timeout=30)
                if result.stdout:
                    permissions['world_writable'] = result.stdout.strip().split('\n')[:10]  # Limit results
                
                # Find SUID files
                result = subprocess.run(['find', '/', '-type', 'f', '-perm', '-4000'], 
                                      capture_output=True, text=True, timeout=30)
                if result.stdout:
                    permissions['suid_files'] = result.stdout.strip().split('\n')[:10]
                
                # Find SGID files
                result = subprocess.run(['find', '/', '-type', 'f', '-perm', '-2000'], 
                                      capture_output=True, text=True, timeout=30)
                if result.stdout:
                    permissions['sgid_files'] = result.stdout.strip().split('\n')[:10]
        
        except Exception as e:
            permissions['error'] = str(e)
        
        return permissions
    
    def audit_user_accounts(self) -> Dict:
        """Audit user accounts"""
        accounts = {
            'total_users': 0,
            'active_users': 0,
            'privileged_users': [],
            'accounts_without_password': [],
            'last_login': []
        }
        
        try:
            if platform.system() == "Linux":
                # Count users
                result = subprocess.run(['awk', '-F:', '($3 >= 1000) {print $1}', '/etc/passwd'], 
                                      capture_output=True, text=True)
                users = result.stdout.strip().split('\n') if result.stdout.strip() else []
                accounts['total_users'] = len(users)
                
                # Check for accounts without passwords
                result = subprocess.run(['awk', '-F:', '($2 == "") {print $1}', '/etc/shadow'], 
                                      capture_output=True, text=True)
                if result.stdout.strip():
                    accounts['accounts_without_password'] = result.stdout.strip().split('\n')
                
                # Check for privileged users
                result = subprocess.run(['awk', '-F:', '($3 == 0) {print $1}', '/etc/passwd'], 
                                      capture_output=True, text=True)
                if result.stdout.strip():
                    accounts['privileged_users'] = result.stdout.strip().split('\n')
            
            elif platform.system() == "Windows":
                result = subprocess.run(['net', 'user'], capture_output=True, text=True)
                # Parse Windows user information
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'The command completed' in line:
                        break
                    parts = line.split()
                    if len(parts) >= 2 and 'active' in line.lower():
                        accounts['total_users'] += 1
        
        except Exception as e:
            accounts['error'] = str(e)
        
        return accounts
    
    def audit_network_services(self) -> Dict:
        """Audit network services"""
        services = {
            'listening_ports': [],
            'running_services': [],
            'vulnerable_services': []
        }
        
        try:
            if platform.system() == "Linux":
                # Get listening ports
                result = subprocess.run(['netstat', '-tlnp'], capture_output=True, text=True, timeout=10)
                for line in result.stdout.split('\n'):
                    if 'LISTEN' in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            services['listening_ports'].append({
                                'port': parts[3].split(':')[-1],
                                'address': parts[3].split(':')[0],
                                'program': parts[-1].split('/')[-1] if '/' in parts[-1] else parts[-1]
                            })
                
                # Check for vulnerable services
                vulnerable_ports = [23, 21, 69, 111, 512, 513, 514]
                for port_info in services['listening_ports']:
                    if int(port_info['port']) in vulnerable_ports:
                        services['vulnerable_services'].append(port_info)
            
            elif platform.system() == "Windows":
                result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=10)
                for line in result.stdout.split('\n'):
                    if 'LISTENING' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            address_port = parts[1]
                            if ':' in address_port:
                                port = address_port.split(':')[-1]
                                services['listening_ports'].append({
                                    'port': port,
                                    'address': address_port.split(':')[0],
                                    'program': 'Unknown'
                                })
        
        except Exception as e:
            services['error'] = str(e)
        
        return services
    
    def audit_security_policies(self) -> Dict:
        """Audit security policies"""
        policies = {
            'password_policy': {},
            'account_lockout': {},
            'audit_policy': {},
            'firewall_enabled': False
        }
        
        try:
            if platform.system() == "Linux":
                # Check password policy
                if os.path.exists('/etc/login.defs'):
                    with open('/etc/login.defs', 'r') as f:
                        content = f.read()
                    
                    for line in content.split('\n'):
                        if line.startswith('PASS_MIN_LEN'):
                            policies['password_policy']['min_length'] = line.split()[1]
                        elif line.startswith('PASS_MAX_DAYS'):
                            policies['password_policy']['max_age'] = line.split()[1]
                
                # Check firewall
                if subprocess.run(['which', 'ufw'], capture_output=True).returncode == 0:
                    result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
                    policies['firewall_enabled'] = 'active' in result.stdout.lower()
            
            elif platform.system() == "Windows":
                # Check Windows security policies
                result = subprocess.run(['net', 'accounts'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Lockout threshold' in line:
                        policies['account_lockout']['threshold'] = line.split(':')[1].strip()
                    elif 'Lockout duration' in line:
                        policies['account_lockout']['duration'] = line.split(':')[1].strip()
                
                # Check firewall
                result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                                      capture_output=True, text=True, timeout=10)
                policies['firewall_enabled'] = 'State' in result.stdout and 'ON' in result.stdout
        
        except Exception as e:
            policies['error'] = str(e)
        
        return policies
    
    def calculate_audit_score(self, audit: Dict) -> int:
        """Calculate security audit score"""
        score = 100
        
        # Deduct points for security issues
        if audit['file_permissions']['world_writable']:
            score -= len(audit['file_permissions']['world_writable']) * 5
        
        if audit['file_permissions']['suid_files']:
            score -= len(audit['file_permissions']['suid_files']) * 3
        
        if audit['user_accounts']['accounts_without_password']:
            score -= len(audit['user_accounts']['accounts_without_password']) * 10
        
        if audit['network_services']['vulnerable_services']:
            score -= len(audit['network_services']['vulnerable_services']) * 8
        
        if not audit['security_policies']['firewall_enabled']:
            score -= 15
        
        return max(0, min(100, score))
    
    def generate_audit_report(self, audit: Dict) -> str:
        """Generate security audit report"""
        report = f"""
SECURITY AUDIT REPORT
====================
Date: {audit['timestamp']}
Audit Score: {audit['audit_score']}/100

SYSTEM INFORMATION
-----------------
OS: {audit['system_info']['os']} {audit['system_info']['version']}
Hostname: {audit['system_info']['hostname']}
Uptime: {audit['system_info']['uptime']}

USER ACCOUNTS
--------------
Total Users: {audit['user_accounts']['total_users']}
Accounts without Password: {len(audit['user_accounts']['accounts_without_password'])}
Privileged Users: {len(audit['user_accounts']['privileged_users'])}

NETWORK SERVICES
-----------------
Listening Ports: {len(audit['network_services']['listening_ports'])}
Vulnerable Services: {len(audit['network_services']['vulnerable_services'])}
Firewall Enabled: {'Yes' if audit['security_policies']['firewall_enabled'] else 'No'}

FILE PERMISSIONS
----------------
World-Writable Files: {len(audit['file_permissions']['world_writable'])}
SUID Files: {len(audit['file_permissions']['suid_files'])}
SGID Files: {len(audit['file_permissions']['sgid_files'])}

SECURITY RECOMMENDATIONS
------------------------
"""
        
        if audit['audit_score'] < 70:
            report += "CRITICAL: Multiple security issues found. Immediate action required.\n"
        elif audit['audit_score'] < 85:
            report += "WARNING: Some security issues found. Review and address soon.\n"
        else:
            report += "GOOD: Security posture is strong. Continue monitoring.\n"
        
        return report


# Main execution
if __name__ == "__main__":
    hardener = SystemHardener()
    results = hardener.harden_system()
    print(hardener.generate_hardening_report(results))
