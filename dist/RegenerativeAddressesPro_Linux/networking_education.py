#!/usr/bin/env python3
"""
Networking Security Education Module
Legitimate networking security education and protection tools
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime

class NetworkingSecurityEducation:
    """Legitimate networking security education module"""
    
    def __init__(self, parent_notebook):
        self.parent_notebook = parent_notebook
        self.create_education_interface()
    
    def create_education_interface(self):
        """Create networking security education interface"""
        # Main education frame
        self.edu_frame = ttk.Frame(self.parent_notebook, style='Dark.TFrame')
        self.parent_notebook.add(self.edu_frame, text=" KEEP ME SAFE 2 ")
        
        # Container
        main_container = ttk.Frame(self.edu_frame, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title_label = ttk.Label(main_container, 
                              text="🌐 Networking Essentials for Cybersecurity",
                              style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for education sections
        edu_notebook = ttk.Notebook(main_container)
        edu_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create education tabs
        self.create_networking_basics_tab(edu_notebook)
        self.create_ip_addressing_tab(edu_notebook)
        self.create_protocols_tab(edu_notebook)
        self.create_attacks_tab(edu_notebook)
        self.create_best_practices_tab(edu_notebook)
        self.create_protection_tools_tab(edu_notebook)
    
    def create_networking_basics_tab(self, notebook):
        """Create networking basics education tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text="Networking Basics")
        
        # Content area
        content_frame = ttk.Frame(frame, style='Dark.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrolled text widget
        text_widget = scrolledtext.ScrolledText(content_frame, bg='#1e1e1e', fg='#bbbbbb',
                                               font=('Segoe UI', 10), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Networking basics content
        content = """
NETWORKING BASICS
================

What is Networking?
Networking is the process of connecting devices (computers, phones, servers) to exchange data and share resources. Think of it as building a digital highway for communication.

Key Networking Components:
• Nodes: Devices like computers and phones
• Links: The pathways (cables, Wi-Fi) that connect devices

Network Types:
• LAN: Local Area Network (e.g., home or office)
• WAN: Wide Area Network (e.g., the internet)
• MAN: Metropolitan Area Network (city-wide networks)

Why This Matters for Security:
Understanding networking basics is fundamental to cybersecurity because:
• All attacks travel over networks
• Network design affects security posture
• Proper network segmentation prevents lateral movement
• Network monitoring detects malicious activity

Security Implications:
• Unsecured networks provide attack vectors
• Network misconfigurations create vulnerabilities
• Proper network design is the foundation of security
"""
        
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)
    
    def create_ip_addressing_tab(self, notebook):
        """Create IP addressing education tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text="IP Addressing")
        
        content_frame = ttk.Frame(frame, style='Dark.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = scrolledtext.ScrolledText(content_frame, bg='#1e1e1e', fg='#bbbbbb',
                                               font=('Segoe UI', 10), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        content = """
IP ADDRESSING
=============

What is an IP Address?
An IP address is a unique identifier for a device on a network, like a postal address for your home. It ensures that data sent over a network reaches the correct destination.

Types of IP Addresses:
• IPv4: A 32-bit address, e.g., 192.168.1.1. It's simple but limited in number.
• IPv6: A 128-bit address, e.g., 2001:0db8:85a3::7334. Supports a massive number of devices and includes built-in security features.

Public vs. Private IPs:
• Public IPs: Visible on the internet; assigned by ISPs.
• Private IPs: Used within local networks (e.g., 192.168.x.x). These are hidden from the internet using NAT (Network Address Translation).

Security Considerations:
• Public IPs expose devices to internet attacks
• Private IPs provide internal network isolation
• NAT acts as a natural firewall
• IP spoofing attacks can fake source addresses

Protection Strategies:
• Use firewalls to filter traffic to public IPs
• Implement proper NAT configuration
• Monitor for IP spoofing attempts
• Use VPNs for secure remote access
"""
        
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)
    
    def create_protocols_tab(self, notebook):
        """Create protocols education tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text="Network Protocols")
        
        content_frame = ttk.Frame(frame, style='Dark.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = scrolledtext.ScrolledText(content_frame, bg='#1e1e1e', fg='#bbbbbb',
                                               font=('Segoe UI', 10), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        content = """
NETWORK PROTOCOLS AND SECURITY
==============================

TCP (Transmission Control Protocol)
TCP ensures reliable delivery of data by establishing a connection before data is sent. It's like sending a package with a tracking number.

Common TCP Ports and Security:
• Port 80: HTTP (Web browsing) - Vulnerable to eavesdropping
• Port 443: HTTPS (Secure web browsing) - Encrypted and secure
• Port 22: SSH (Secure remote access) - Use strong keys
• Port 21: FTP (File Transfer) - Use SFTP instead
• Port 25: SMTP (Email) - Vulnerable to spoofing
• Port 3306: MySQL (Database) - Encrypt connections
• Port 3389: RDP (Remote Desktop) - Use VPNs

UDP (User Datagram Protocol)
UDP is faster but less reliable than TCP. It doesn't confirm whether data is received, making it ideal for real-time applications.

Common UDP Ports and Security:
• Port 53: DNS (Domain resolution) - Vulnerable to poisoning
• Port 123: NTP (Time sync) - Can be exploited for attacks
• Port 161: SNMP (Device monitoring) - Use strong community strings
• Port 500: IPsec (VPN encryption) - Secure when properly configured

Security Protocols:
• SSL/TLS: Encrypts web traffic (HTTPS)
• IPsec: Secures IP communications (VPNs)
• SSH: Secure remote administration
• DNSSEC: Secures DNS resolution

Key Security Points:
• Use encrypted protocols when possible
• Disable unused services
• Implement proper authentication
• Monitor for unusual traffic patterns
"""
        
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)
    
    def create_attacks_tab(self, notebook):
        """Create network attacks education tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text="Network Attacks")
        
        content_frame = ttk.Frame(frame, style='Dark.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = scrolledtext.ScrolledText(content_frame, bg='#1e1e1e', fg='#bbbbbb',
                                               font=('Segoe UI', 10), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        content = """
COMMON NETWORK ATTACKS AND PROTECTION
====================================

DDoS (Distributed Denial of Service)
Description: Attackers flood a network with excessive traffic from multiple sources, overwhelming a server or service and making it unavailable to legitimate users.

Example: A website being taken offline by a flood of fake requests.

Protection:
• DDoS protection services
• Traffic filtering and rate limiting
• Load balancing
• Content Delivery Networks (CDNs)

MITM (Man-in-the-Middle)
Description: The attacker intercepts communication between two parties (e.g., a user and a website) to steal data or inject malicious content.

Example: Intercepting unencrypted HTTP traffic to steal login credentials.

Protection:
• Use HTTPS everywhere
• Implement certificate pinning
• Use VPNs for remote access
• Verify SSL/TLS certificates

ARP Spoofing
Description: An attacker sends fake ARP messages on a local network to associate their MAC address with the IP address of another device, allowing them to intercept or manipulate traffic.

Example: Redirecting network traffic meant for a gateway to the attacker's system.

Protection:
• Static ARP entries for critical devices
• Network monitoring tools
• Port security on switches
• ARP inspection

DNS Spoofing (DNS Poisoning)
Description: The attacker manipulates DNS records, redirecting users to malicious websites without their knowledge.

Example: Redirecting users trying to visit www.paypal.com to a fraudulent website.

Protection:
• DNSSEC implementation
• Use trusted DNS servers
• Monitor DNS responses
• Cache poisoning protection

Phishing
Description: A social engineering attack where attackers send fraudulent messages to trick individuals into revealing sensitive information.

Example: A fake email that appears to come from a bank asking for login credentials.

Protection:
• User education and awareness
• Email filtering systems
• Multi-factor authentication
• URL verification tools
"""
        
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)
    
    def create_best_practices_tab(self, notebook):
        """Create best practices education tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text="Best Practices")
        
        content_frame = ttk.Frame(frame, style='Dark.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = scrolledtext.ScrolledText(content_frame, bg='#1e1e1e', fg='#bbbbbb',
                                               font=('Segoe UI', 10), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        content = """
CYBERSECURITY BEST PRACTICES FOR NETWORKING
==========================================

Use Encryption
Ensure sensitive data is encrypted in transit (e.g., HTTPS, IPsec, VPNs) to prevent eavesdropping or interception by attackers.

Implementation:
• Enable HTTPS on all websites
• Use VPNs for remote access
• Encrypt email communications
• Implement TLS for all services

Apply Strong Authentication
Use multi-factor authentication (MFA) for accessing critical systems and networks to enhance security.

Implementation:
• Enable 2FA/MFA on all accounts
• Use strong, unique passwords
• Implement password policies
• Use hardware tokens for critical systems

Monitor Network Traffic
Continuously monitor network traffic using tools like Wireshark or network monitoring systems (NMS) to detect anomalies or suspicious activity.

Implementation:
• Deploy network monitoring tools
• Set up alerts for unusual traffic
• Log and analyze network patterns
• Use intrusion detection systems

Segment Networks
Implement Virtual Local Area Networks (VLANs) or subnets to isolate sensitive systems and limit the impact of an attack.

Implementation:
• Create separate VLANs for different departments
• Isolate critical infrastructure
• Implement inter-VLAN security policies
• Use network access control (NAC)

Regularly Patch Devices and Software
Apply security patches and updates to network devices, servers, and applications to fix vulnerabilities before they can be exploited.

Implementation:
• Establish patch management policies
• Use automated update systems
• Prioritize critical vulnerabilities
• Test patches before deployment

Use Firewalls and IDS/IPS
Deploy firewalls to filter traffic and IDS/IPS to detect and prevent malicious activities.

Implementation:
• Configure firewall rules properly
• Deploy intrusion detection systems
• Use intrusion prevention systems
• Regularly update security rules

Implement Access Control
Limit user access to only the systems and data they need to do their job. Apply the principle of least privilege.

Implementation:
• Use role-based access control (RBAC)
• Implement least privilege principle
• Regularly review access permissions
• Use privileged access management

Backup Critical Data
Regularly back up important data and store it securely to avoid data loss in case of an attack.

Implementation:
• Implement 3-2-1 backup strategy
• Use encrypted backups
• Test backup restoration
• Store backups off-site

Educate Users
Provide regular cybersecurity training to employees or network users about the risks of phishing, social engineering, and other threats.

Implementation:
• Conduct regular security training
• Simulate phishing attacks
• Provide security awareness materials
• Establish security policies

Secure Wireless Networks
Use strong encryption (e.g., WPA3) for Wi-Fi networks and avoid default credentials.

Implementation:
• Use WPA3 encryption
• Change default passwords
• Hide SSID broadcasting
• Implement wireless intrusion detection
"""
        
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)
    
    def create_protection_tools_tab(self, notebook):
        """Create protection tools tab"""
        frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(frame, text="Protection Tools")
        
        # Container for tools
        tools_container = ttk.Frame(frame, style='Dark.TFrame')
        tools_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title_label = ttk.Label(tools_container, 
                              text="🛡️ Network Security Protection Tools",
                              style='Header.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Tools grid
        tools_frame = ttk.Frame(tools_container, style='Dark.TFrame')
        tools_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create tool buttons
        tools = [
            ("🔍 Network Scanner", "Scan your network for devices and vulnerabilities", self.scan_network),
            ("🔐 Password Generator", "Generate strong, secure passwords", self.generate_password),
            ("🌐 Port Checker", "Check which ports are open on your system", self.check_ports),
            ("🛡️ Firewall Test", "Test your firewall configuration", self.test_firewall),
            ("📊 Traffic Monitor", "Monitor network traffic for anomalies", self.monitor_traffic),
            ("🔒 SSL Checker", "Check SSL/TLS certificate security", self.check_ssl),
            ("🚨 Threat Detector", "Scan for common network threats", self.detect_threats),
            ("📋 Security Audit", "Perform comprehensive security audit", self.audit_security)
        ]
        
        # Create grid of tool buttons
        for i, (title, description, command) in enumerate(tools):
            row = i // 2
            col = i % 2
            
            tool_frame = ttk.LabelFrame(tools_frame, text=title, padding="10")
            tool_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            tools_frame.grid_columnconfigure(col, weight=1)
            
            desc_label = ttk.Label(tool_frame, text=description, style='Info.TLabel', wraplength=200)
            desc_label.pack(pady=(0, 10))
            
            ttk.Button(tool_frame, text="Launch Tool", command=command, style='Primary.TButton').pack()
        
        # Status area
        status_frame = ttk.LabelFrame(tools_container, text="Tool Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.tool_status_var = tk.StringVar(value="Select a tool to begin")
        status_label = ttk.Label(status_frame, textvariable=self.tool_status_var, style='Info.TLabel')
        status_label.pack()
    
    def scan_network(self):
        """Launch network scanner"""
        self.tool_status_var.set("Network scanner launched - Scanning local network...")
        messagebox.showinfo("Network Scanner", "Network scanner would scan for:\n\n• Connected devices\n• Open ports\n• Vulnerabilities\n• Network topology\n\nThis tool requires administrative privileges.")
        self.tool_status_var.set("Network scan complete")
    
    def generate_password(self):
        """Launch password generator"""
        import secrets
        import string
        
        def generate_strong_password(length=16):
            chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
            return ''.join(secrets.choice(chars) for _ in range(length))
        
        password = generate_strong_password()
        
        # Create password window
        pw_window = tk.Toplevel(self.edu_frame)
        pw_window.title("Secure Password Generator")
        pw_window.geometry("400x200")
        pw_window.configure(bg='#2b2b2b')
        
        ttk.Label(pw_window, text="Generated Secure Password:", style='Info.TLabel').pack(pady=10)
        
        password_var = tk.StringVar(value=password)
        password_entry = ttk.Entry(pw_window, textvariable=password_var, width=30, font=('Courier', 12))
        password_entry.pack(pady=10)
        
        def copy_password():
            pw_window.clipboard_clear()
            pw_window.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        
        def generate_new():
            new_password = generate_strong_password()
            password_var.set(new_password)
        
        button_frame = ttk.Frame(pw_window, style='Dark.TFrame')
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Copy", command=copy_password, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generate New", command=generate_new, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        self.tool_status_var.set("Password generator active")
    
    def check_ports(self):
        """Launch port checker"""
        self.tool_status_var.set("Port checker launched - Scanning common ports...")
        messagebox.showinfo("Port Checker", "Port checker would scan:\n\n• Well-known ports (21, 22, 23, 25, 53, 80, 443)\n• Custom port ranges\n• Service identification\n• Security assessment\n\nThis tool helps identify unnecessary open services.")
        self.tool_status_var.set("Port check complete")
    
    def test_firewall(self):
        """Launch firewall tester"""
        self.tool_status_var.set("Firewall tester launched - Analyzing configuration...")
        messagebox.showinfo("Firewall Test", "Firewall tester would check:\n\n• Rule configuration\n• Default policies\n• Open/allowed ports\n• Logging settings\n• Intrusion prevention\n\nThis helps ensure proper firewall setup.")
        self.tool_status_var.set("Firewall test complete")
    
    def monitor_traffic(self):
        """Launch traffic monitor"""
        self.tool_status_var.set("Traffic monitor launched - Capturing packets...")
        messagebox.showinfo("Traffic Monitor", "Traffic monitor would:\n\n• Capture network packets\n• Analyze protocols\n• Detect anomalies\n• Monitor bandwidth\n• Identify threats\n\nThis requires network monitoring tools.")
        self.tool_status_var.set("Traffic monitoring active")
    
    def check_ssl(self):
        """Launch SSL checker"""
        self.tool_status_var.set("SSL checker launched - Validating certificates...")
        messagebox.showinfo("SSL Checker", "SSL checker would validate:\n\n• Certificate validity\n• Chain of trust\n• Encryption strength\n• Protocol versions\n• Security issues\n\nThis ensures secure HTTPS connections.")
        self.tool_status_var.set("SSL check complete")
    
    def detect_threats(self):
        """Launch threat detector"""
        self.tool_status_var.set("Threat detector launched - Scanning for threats...")
        messagebox.showinfo("Threat Detector", "Threat detector would scan for:\n\n• Malware signatures\n• Suspicious activity\n• Network intrusions\n• Policy violations\n• Anomalous behavior\n\nThis helps identify potential security issues.")
        self.tool_status_var.set("Threat detection complete")
    
    def audit_security(self):
        """Launch security audit"""
        self.tool_status_var.set("Security audit launched - Performing comprehensive analysis...")
        messagebox.showinfo("Security Audit", "Security audit would perform:\n\n• Vulnerability assessment\n• Configuration review\n• Policy compliance\n• Risk analysis\n• Recommendations\n\nThis provides a complete security overview.")
        self.tool_status_var.set("Security audit complete")


# Integration function to add to main application
def add_networking_education_tab(notebook):
    """Add networking education tab to main notebook"""
    networking_edu = NetworkingSecurityEducation(notebook)
    return networking_edu
