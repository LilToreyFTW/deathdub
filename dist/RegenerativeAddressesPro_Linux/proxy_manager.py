#!/usr/bin/env python3
"""
Proxy Manager for Regenerative Addresses Tool
Downloads and manages free proxy lists
"""

import urllib.request
import os
import time
from datetime import datetime

class ProxyManager:
    def __init__(self):
        self.proxy_sources = [
            {
                'name': 'Proxifly All Proxies',
                'url': 'https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt',
                'filename': 'proxifly_all.txt'
            },
            {
                'name': 'Proxifly HTTP Proxies',
                'url': 'https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt',
                'filename': 'proxifly_http.txt'
            },
            {
                'name': 'Proxifly SOCKS4 Proxies',
                'url': 'https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt',
                'filename': 'proxifly_socks4.txt'
            },
            {
                'name': 'Proxifly SOCKS5 Proxies',
                'url': 'https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.txt',
                'filename': 'proxifly_socks5.txt'
            },
            {
                'name': 'SpeedX HTTP Proxies',
                'url': 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
                'filename': 'speedx_http.txt'
            },
            {
                'name': 'SpeedX SOCKS4 Proxies',
                'url': 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
                'filename': 'speedx_socks4.txt'
            },
            {
                'name': 'SpeedX SOCKS5 Proxies',
                'url': 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
                'filename': 'speedx_socks5.txt'
            }
        ]
    
    def download_proxies(self):
        """Download proxy lists from all sources"""
        print("Starting proxy download...")
        total_proxies = 0
        
        for source in self.proxy_sources:
            try:
                print(f"Downloading {source['name']}...")
                response = urllib.request.urlopen(source['url'], timeout=30)
                data = response.read().decode('utf-8')
                
                with open(source['filename'], 'w') as f:
                    f.write(data)
                
                proxy_count = len([line for line in data.split('\n') if line.strip()])
                total_proxies += proxy_count
                print(f"Downloaded {proxy_count} proxies from {source['name']}")
                
                time.sleep(1)  # Be respectful to the servers
                
            except Exception as e:
                print(f"Failed to download {source['name']}: {e}")
        
        # Combine all proxies
        self.combine_proxies()
        
        print(f"Total proxies downloaded: {total_proxies}")
        return total_proxies
    
    def combine_proxies(self):
        """Combine all proxy files into one master file"""
        all_proxies = []
        
        for source in self.proxy_sources:
            if os.path.exists(source['filename']):
                with open(source['filename'], 'r') as f:
                    proxies = f.read().strip().split('\n')
                    all_proxies.extend([p.strip() for p in proxies if p.strip()])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_proxies = []
        for proxy in all_proxies:
            if proxy not in seen:
                seen.add(proxy)
                unique_proxies.append(proxy)
        
        with open('all_proxies.txt', 'w') as f:
            f.write('\n'.join(unique_proxies))
        
        print(f"Combined {len(unique_proxies)} unique proxies into all_proxies.txt")
        return len(unique_proxies)
    
    def get_proxy_stats(self):
        """Get statistics about loaded proxies"""
        if not os.path.exists('all_proxies.txt'):
            return None
        
        with open('all_proxies.txt', 'r') as f:
            proxies = f.read().strip().split('\n')
        
        stats = {
            'total': len(proxies),
            'http': 0,
            'socks4': 0,
            'socks5': 0,
            'https': 0
        }
        
        for proxy in proxies:
            proxy = proxy.lower()
            if proxy.startswith('http://'):
                stats['http'] += 1
            elif proxy.startswith('https://'):
                stats['https'] += 1
            elif proxy.startswith('socks4://'):
                stats['socks4'] += 1
            elif proxy.startswith('socks5://'):
                stats['socks5'] += 1
            else:
                stats['http'] += 1  # Assume HTTP if no protocol
        
        return stats

if __name__ == "__main__":
    manager = ProxyManager()
    
    print("Proxy Manager for Regenerative Addresses Tool")
    print("=" * 50)
    
    # Download proxies
    total = manager.download_proxies()
    
    # Show statistics
    stats = manager.get_proxy_stats()
    if stats:
        print("\nProxy Statistics:")
        print(f"Total: {stats['total']}")
        print(f"HTTP: {stats['http']}")
        print(f"HTTPS: {stats['https']}")
        print(f"SOCKS4: {stats['socks4']}")
        print(f"SOCKS5: {stats['socks5']}")
    
    print(f"\nCompleted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
