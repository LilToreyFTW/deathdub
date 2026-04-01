<?php

/**
 * Configuration for Regenerative Addresses Tool
 * Removed unused file assets.php
 */

return [
    // Application settings
    'app_name' => 'Regenerative Addresses Tool',
    'app_version' => '1.0.0',
    'debug_mode' => false,
    
    // Database configuration
    'db' => [
        'host' => 'localhost',
        'dbname' => 'regenerative_addresses',
        'username' => 'root',
        'password' => '',
        'charset' => 'utf8mb4'
    ],
    
    // Routing
    'default_controller' => 'main',
    'error_controller' => 'errors',
    'error_type' => [
        '404' => 'not_found',
        '403' => 'forbidden',
        '500' => 'server_error'
    ],
    
    // URLs
    'base_url' => 'http://localhost/regenerative-addresses/',
    'assets_url' => 'http://localhost/regenerative-addresses/assets/',
    
    // Session settings
    'session_timeout' => 300,
    'session_name' => 'regen_session',
    
    // Security
    'csrf_token_name' => 'csrf_token',
    'display_login_error' => false,
    
    // File paths
    'upload_dir' => 'uploads/',
    'log_dir' => 'logs/',
    'cache_dir' => 'cache/',
    
    // Email settings
    'email' => [
        'from' => 'noreply@regenerative-addresses.com',
        'from_name' => 'Regenerative Addresses Tool'
    ],
    
    // API settings
    'api' => [
        'rate_limit' => 100,
        'rate_limit_period' => 3600
    ],
    
    // Features
    'features' => [
        'registration' => true,
        'email_verification' => false,
        'password_reset' => true,
        'proxy_support' => true,
        'kali_tools' => true,
        'auto_update' => true
    ],
    
    // Logging
    'log_file' => 'logs/app.log',
    'log_level' => 'INFO',
    
    // Cache settings
    'cache_enabled' => true,
    'cache_ttl' => 3600,
    
    // Proxy settings
    'proxy_files' => [
        'all_proxies.txt',
        'proxies.txt',
        'https_proxies.txt',
        'socks4_proxies.txt',
        'socks5_proxies.txt'
    ],
    
    // Kali tools paths
    'kali_tools' => [
        'responder' => '/usr/bin/responder',
        'john' => '/usr/bin/john',
        'hashcat' => '/usr/bin/hashcat',
        'hydra' => '/usr/bin/hydra',
        'sqlmap' => '/usr/bin/sqlmap',
        'nmap' => '/usr/bin/nmap',
        'impacket' => '/usr/share/impacket',
        'crunch' => '/usr/bin/crunch'
    ],
    
    // GitHub settings for auto-update
    'github' => [
        'repo' => 'https://github.com/LilToreyFTW/deathdub',
        'branch' => 'main'
    ]
];
