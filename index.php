<?php
/**
 * Main entry point for Regenerative Addresses Tool PHP interface
 * Educational and legitimate security testing purposes only
 */

// Define APP_DIR if not defined
if (!defined('APP_DIR')) {
    define('APP_DIR', __DIR__ . '/src');
}

// Start session
session_start();

// Load configuration
$config = require APP_DIR . '/config/config.php';

// Include core files
require APP_DIR . '/goat.php';
require APP_DIR . '/controller.php';
require APP_DIR . '/model.php';
require APP_DIR . '/view.php';

// Initialize the application
$app = new goat($config);

// Handle session timeout
if (isset($_SESSION['login_time']) && (time() - $_SESSION['login_time']) > $config['session_timeout']) {
    // Clear session
    session_destroy();
    // Redirect to login
    header('Location: ' . $config['base_url'] . 'login');
    exit;
}

// Auto-update check
if ($config['features']['auto_update'] && isset($_SESSION['last_update_check'])) {
    if (time() - $_SESSION['last_update_check'] > 86400) { // Check once per day
        // Update check logic here
        $_SESSION['last_update_check'] = time();
    }
} else {
    $_SESSION['last_update_check'] = time();
}
?>
