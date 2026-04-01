#!/usr/bin/env python3
"""
GitHub Repository Updater
Updates GitHub repositories, releases, and websites
"""

import requests
import json
import subprocess
import os
import time
from datetime import datetime
import base64
import hashlib

class GitHubUpdater:
    def __init__(self, github_token=None):
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        } if self.github_token else {}
    
    def get_user_repos(self, username="LilToreyFTW"):
        """Get all repositories for a user"""
        url = f"{self.base_url}/users/{username}/repos"
        repos = []
        page = 1
        
        while True:
            params = {'per_page': 100, 'page': page}
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"Error fetching repos: {response.status_code}")
                break
            
            page_repos = response.json()
            if not page_repos:
                break
            
            repos.extend(page_repos)
            page += 1
        
        return repos
    
    def update_repo_description(self, repo_name, description):
        """Update repository description"""
        url = f"{self.base_url}/repos/LilToreyFTW/{repo_name}"
        data = {
            'name': repo_name,
            'description': description
        }
        
        response = requests.patch(url, headers=self.headers, json=data)
        return response.status_code == 200
    
    def create_or_update_release(self, repo_name, tag_name, release_name, release_body, draft=False):
        """Create or update a GitHub release"""
        url = f"{self.base_url}/repos/LilToreyFTW/{repo_name}/releases"
        
        # Check if release exists
        releases_url = f"{self.base_url}/repos/LilToreyFTW/{repo_name}/releases/tags/{tag_name}"
        existing_response = requests.get(releases_url, headers=self.headers)
        
        if existing_response.status_code == 200:
            # Update existing release
            release_id = existing_response.json()['id']
            update_url = f"{url}/{release_id}"
            response = requests.patch(update_url, headers=self.headers, json={
                'tag_name': tag_name,
                'name': release_name,
                'body': release_body,
                'draft': draft
            })
        else:
            # Create new release
            response = requests.post(url, headers=self.headers, json={
                'tag_name': tag_name,
                'name': release_name,
                'body': release_body,
                'draft': draft
            })
        
        return response.status_code == 201 or response.status_code == 200
    
    def get_repo_stats(self, repo_name):
        """Get repository statistics"""
        url = f"{self.base_url}/repos/LilToreyFTW/{repo_name}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'stars': data['stargazers_count'],
                'forks': data['forks_count'],
                'watchers': data['watchers_count'],
                'open_issues': data['open_issues_count'],
                'language': data['language'],
                'size': data['size'],
                'created_at': data['created_at'],
                'updated_at': data['updated_at']
            }
        return None
    
    def update_repo_topics(self, repo_name, topics):
        """Update repository topics"""
        url = f"{self.base_url}/repos/LilToreyFTW/{repo_name}/topics"
        data = {'names': topics}
        
        response = requests.put(url, headers=self.headers, json=data)
        return response.status_code == 200

def main():
    """Main execution function"""
    print("🚀 GitHub Repository Updater")
    print("=" * 50)
    
    # Initialize updater
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN environment variable not set")
        print("Please set your GitHub token:")
        print("export GITHUB_TOKEN='your_token_here'")
        return
    
    updater = GitHubUpdater(github_token)
    
    # Get repositories
    repos = updater.get_user_repos()
    print(f"Found {len(repos)} repositories")
    
    # Update each repository
    for repo in repos:
        repo_name = repo['name']
        
        if repo['archived']:
            print(f"⏭️ Skipping archived repo: {repo_name}")
            continue
        
        print(f"🔄 Updating {repo_name}...")
        
        # Update description
        if not repo['description'] or len(repo['description']) < 10:
            new_description = f"Professional {repo_name} - Advanced features and modern implementation"
            if updater.update_repo_description(repo_name, new_description):
                print(f"✅ Updated description for {repo_name}")
        
        # Update topics
        topics = ['python', 'security', 'networking', 'automation', 'professional']
        if updater.update_repo_topics(repo_name, topics):
            print(f"✅ Updated topics for {repo_name}")
        
        # Create release
        version = "3.0.0"
        stats = updater.get_repo_stats(repo_name)
        
        release_body = f"""# 🚀 Release {version}

## 📊 Repository Statistics
- ⭐ Stars: {stats['stars'] if stats else 0}
- 🍴 Forks: {stats['forks'] if stats else 0}
- 👀 Watchers: {stats['watchers'] if stats else 0}
- 🐛 Open Issues: {stats['open_issues'] if stats else 0}
- 💻 Primary Language: {stats['language'] if stats else 'Unknown'}

## 🆕 What's New in {version}

### 🔐 Security Enhancements
- Enhanced authentication mechanisms
- Improved data encryption
- Security vulnerability patches
- Access control improvements

### 🚀 Performance Improvements
- Optimized database queries
- Reduced memory usage
- Faster response times
- Improved caching mechanisms

### 🎨 User Interface Updates
- Modernized design elements
- Better user experience
- Responsive design improvements
- Accessibility enhancements

### 🔧 Technical Improvements
- Code refactoring and optimization
- Better error handling
- Improved logging system
- Enhanced debugging capabilities

### 📦 New Features
- Advanced monitoring capabilities
- Automated deployment options
- Enhanced API endpoints
- Better configuration management

## 🛠️ Installation

### Quick Start
```bash
git clone https://github.com/LilToreyFTW/{repo_name}.git
cd {repo_name}
pip install -r requirements.txt
python3 main.py
```

### Docker Setup
```bash
docker build -t {repo_name}:{version} .
docker run -d --name {repo_name} -p 8080:8080 {repo_name}:{version}
```

## 🔗 Links

- 📖 [Documentation](https://github.com/LilToreyFTW/{repo_name}/wiki)
- 🐛 [Issue Tracker](https://github.com/LilToreyFTW/{repo_name}/issues)
- 💬 [Discussions](https://github.com/LilToreyFTW/{repo_name}/discussions)

---

**Release Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Version**: {version}
"""
        
        if updater.create_or_update_release(repo_name, f"v{version}", f"Release {version}", release_body):
            print(f"✅ Created release v{version} for {repo_name}")
        
        time.sleep(1)  # Rate limiting
    
    print("\n🎉 Repository update process completed!")

if __name__ == "__main__":
    main()
