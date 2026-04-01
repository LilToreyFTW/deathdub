#!/usr/bin/env python3
"""
Auto-Updater Module for Regenerative Addresses Tool
Handles automatic updates from GitHub repository
"""

import os
import sys
import json
import hashlib
import subprocess
import threading
import time
import re
from datetime import datetime
import urllib.request
import urllib.parse
import zipfile
import shutil
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

class AutoUpdater:
    def __init__(self, current_version="1.0.0", repo_url="https://github.com/LilToreyFTW/deathdub.git"):
        self.current_version = current_version
        self.repo_url = repo_url
        self.update_interval = 3600  # Check every hour
        self.update_thread = None
        self.callback = None
        
    def check_for_updates(self, callback=None):
        """Check for updates from GitHub repository"""
        try:
            self.callback = callback
            
            # Get latest release info from GitHub API
            api_url = "https://api.github.com/repos/LilToreyFTW/deathdub/releases/latest"
            
            with urllib.request.urlopen(api_url, timeout=10) as response:
                release_data = json.loads(response.read().decode())
            
            latest_version = release_data.get('tag_name', '1.0.0').lstrip('v')
            download_url = release_data.get('zipball_url', '')
            
            # Compare versions
            if self._compare_versions(latest_version, self.current_version) > 0:
                update_info = {
                    'available': True,
                    'version': latest_version,
                    'download_url': download_url,
                    'release_notes': release_data.get('body', ''),
                    'published_at': release_data.get('published_at', '')
                }
                
                if callback:
                    callback(update_info)
                
                return update_info
            else:
                return {'available': False, 'version': latest_version}
                
        except Exception as e:
            error_info = {'available': False, 'error': str(e)}
            if callback:
                callback(error_info)
            return error_info
    
    def _compare_versions(self, v1, v2):
        """Compare two version strings"""
        def normalize(v):
            return [int(x) for x in re.sub(r'[^0-9.]', '', v).split('.')]
        
        v1_parts = normalize(v1)
        v2_parts = normalize(v2)
        
        # Pad shorter version with zeros
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))
        
        for i in range(max_len):
            if v1_parts[i] > v2_parts[i]:
                return 1
            elif v1_parts[i] < v2_parts[i]:
                return -1
        
        return 0
    
    def download_update(self, download_url, progress_callback=None):
        """Download update from GitHub"""
        try:
            # Create temporary directory for update
            temp_dir = os.path.join(os.getcwd(), 'temp_update')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Download the update
            zip_path = os.path.join(temp_dir, 'update.zip')
            
            with urllib.request.urlopen(download_url, timeout=30) as response:
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                
                with open(zip_path, 'wb') as f:
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)
            
            return zip_path
            
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")
    
    def install_update(self, zip_path, backup_callback=None):
        """Install the downloaded update"""
        try:
            # Create backup
            backup_dir = os.path.join(os.getcwd(), 'backup')
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup current files
            important_files = [
                'regenerative-addresses.py',
                'kali_credential_obtainer.py',
                'users.json',
                'all_proxies.txt'
            ]
            
            for file in important_files:
                if os.path.exists(file):
                    backup_path = os.path.join(backup_dir, file)
                    shutil.copy2(file, backup_path)
            
            if backup_callback:
                backup_callback("Backup created successfully")
            
            # Extract update
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find extracted directory (GitHub creates a folder with commit hash)
            extracted_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d)) and d != 'backup']
            if not extracted_dirs:
                raise Exception("No extracted directory found")
            
            source_dir = os.path.join(temp_dir, extracted_dirs[0])
            
            # Update files
            updated_files = []
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    source_file = os.path.join(root, file)
                    relative_path = os.path.relpath(source_file, source_dir)
                    target_file = os.path.join(os.getcwd(), relative_path)
                    
                    # Create directory if needed
                    os.makedirs(os.path.dirname(target_file), exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(source_file, target_file)
                    updated_files.append(relative_path)
            
            # Cleanup
            shutil.rmtree(temp_dir)
            
            return {
                'success': True,
                'updated_files': updated_files,
                'message': f"Successfully updated {len(updated_files)} files"
            }
            
        except Exception as e:
            # Restore from backup if update failed
            self._restore_backup()
            raise Exception(f"Update installation failed: {str(e)}")
    
    def _restore_backup(self):
        """Restore files from backup"""
        try:
            backup_dir = os.path.join(os.getcwd(), 'backup')
            if os.path.exists(backup_dir):
                for file in os.listdir(backup_dir):
                    backup_file = os.path.join(backup_dir, file)
                    target_file = os.path.join(os.getcwd(), file)
                    if os.path.exists(backup_file):
                        shutil.copy2(backup_file, target_file)
        except:
            pass
    
    def start_auto_update_check(self):
        """Start background thread to check for updates periodically"""
        if self.update_thread and self.update_thread.is_alive():
            return
        
        def check_loop():
            while True:
                try:
                    self.check_for_updates()
                    time.sleep(self.update_interval)
                except:
                    time.sleep(300)  # Wait 5 minutes on error
        
        self.update_thread = threading.Thread(target=check_loop, daemon=True)
        self.update_thread.start()
    
    def stop_auto_update_check(self):
        """Stop the auto-update check thread"""
        if self.update_thread and self.update_thread.is_alive():
            # Thread will stop naturally when main program exits
            pass
    
    def show_update_dialog(self, parent, update_info):
        """Show update available dialog"""
        dialog = tk.Toplevel(parent)
        dialog.title("Update Available")
        dialog.geometry("500x400")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Update info
        info_frame = tk.Frame(dialog, padx=20, pady=20)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(info_frame, text="New Version Available!", 
                font=('Arial', 14, 'bold'), fg='green').pack(pady=(0, 10))
        
        tk.Label(info_frame, text=f"Current: {self.current_version} → Latest: {update_info['version']}").pack()
        
        # Release notes
        tk.Label(info_frame, text="Release Notes:", font=('Arial', 12, 'bold')).pack(pady=(20, 5))
        
        notes_text = tk.Text(info_frame, height=10, width=50)
        notes_text.pack(fill=tk.BOTH, expand=True)
        notes_text.insert(tk.END, update_info.get('release_notes', 'No release notes available.'))
        notes_text.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def download_and_install():
            try:
                # Show progress
                progress_window = tk.Toplevel(dialog)
                progress_window.title("Downloading Update")
                progress_window.geometry("300x100")
                
                progress_label = tk.Label(progress_window, text="Downloading update...")
                progress_label.pack(pady=10)
                
                progress_bar = tk.ttk.Progressbar(progress_window, length=250, mode='determinate')
                progress_bar.pack(pady=10)
                
                def progress_callback(percent):
                    progress_bar['value'] = percent
                    progress_window.update()
                
                # Download
                zip_path = self.download_update(update_info['download_url'], progress_callback)
                
                progress_window.destroy()
                
                # Install
                result = self.install_update(zip_path)
                
                messagebox.showinfo("Update Complete", 
                    f"Update installed successfully!\n\n{result['message']}\n\nPlease restart the application.")
                dialog.destroy()
                
                # Restart application
                os.execv(sys.executable, ['python'] + sys.argv)
                
            except Exception as e:
                messagebox.showerror("Update Failed", f"Failed to install update:\n{str(e)}")
        
        tk.Button(button_frame, text="Download & Install", command=download_and_install, 
                 bg='green', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Later", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Skip This Version", 
                 command=lambda: [dialog.destroy(), self._skip_version(update_info['version'])]).pack(side=tk.LEFT, padx=5)
    
    def _skip_version(self, version):
        """Skip this version"""
        skip_file = 'skip_version.txt'
        with open(skip_file, 'w') as f:
            f.write(version)
    
    def is_version_skipped(self, version):
        """Check if version was skipped"""
        skip_file = 'skip_version.txt'
        if os.path.exists(skip_file):
            with open(skip_file, 'r') as f:
                return f.read().strip() == version
        return False

# Usage example
if __name__ == "__main__":
    updater = AutoUpdater()
    update = updater.check_for_updates()
    print("Update available:", update.get('available', False))
    if update.get('available'):
        print("Latest version:", update['version'])
