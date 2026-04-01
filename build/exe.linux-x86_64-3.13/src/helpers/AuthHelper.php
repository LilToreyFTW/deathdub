<?php

/**
 * Authentication Helper
 * PSR-2 compliant
 */

class AuthHelper
{
    /**
     * User session key
     *
     * @var string
     */
    const SESSION_KEY = 'user_id';

    /**
     * Check if user is logged in
     *
     * @return bool
     */
    public static function isLoggedIn()
    {
        return isset($_SESSION[self::SESSION_KEY]) && !empty($_SESSION[self::SESSION_KEY]);
    }

    /**
     * Get current user ID
     *
     * @return int|null
     */
    public static function getUserId()
    {
        return self::isLoggedIn() ? $_SESSION[self::SESSION_KEY] : null;
    }

    /**
     * Set user session
     *
     * @param int $userId User ID
     * @return void
     */
    public static function setUserSession($userId)
    {
        $_SESSION[self::SESSION_KEY] = (int)$userId;
        $_SESSION['login_time'] = time();
    }

    /**
     * Clear user session
     *
     * @return void
     */
    public static function clearUserSession()
    {
        unset($_SESSION[self::SESSION_KEY]);
        unset($_SESSION['login_time']);
    }

    /**
     * Check session timeout
     *
     * @param int $timeout Timeout in seconds
     * @return bool
     */
    public static function isSessionExpired($timeout = 300)
    {
        if (!self::isLoggedIn()) {
            return true;
        }

        $loginTime = $_SESSION['login_time'] ?? 0;
        return (time() - $loginTime) > $timeout;
    }

    /**
     * Hash password
     *
     * @param string $password Password
     * @return string Hashed password
     */
    public static function hashPassword($password)
    {
        return password_hash($password, PASSWORD_DEFAULT);
    }

    /**
     * Verify password
     *
     * @param string $password Password
     * @param string $hash Hashed password
     * @return bool
     */
    public static function verifyPassword($password, $hash)
    {
        return password_verify($password, $hash);
    }

    /**
     * Generate secure token
     *
     * @param int $length Token length
     * @return string
     */
    public static function generateToken($length = 32)
    {
        return bin2hex(random_bytes($length));
    }

    /**
     * Generate CSRF token
     *
     * @return string
     */
    public static function generateCsrfToken()
    {
        if (!isset($_SESSION['csrf_token'])) {
            $_SESSION['csrf_token'] = self::generateToken(32);
        }

        return $_SESSION['csrf_token'];
    }

    /**
     * Validate CSRF token
     *
     * @param string $token Token to validate
     * @return bool
     */
    public static function validateCsrfToken($token)
    {
        if (!isset($_SESSION['csrf_token'])) {
            return false;
        }

        return hash_equals($_SESSION['csrf_token'], $token);
    }

    /**
     * Require login
     *
     * @param string $redirect Redirect URL
     * @return void
     */
    public static function requireLogin($redirect = '/login')
    {
        if (!self::isLoggedIn() || self::isSessionExpired()) {
            self::clearUserSession();
            header('Location: ' . $redirect);
            exit();
        }
    }

    /**
     * Get user IP address
     *
     * @return string
     */
    public static function getUserIp()
    {
        $ip = '';

        if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
            $ip = $_SERVER['HTTP_CLIENT_IP'];
        } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
            $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
        } else {
            $ip = $_SERVER['REMOTE_ADDR'];
        }

        return filter_var($ip, FILTER_VALIDATE_IP) ? $ip : '127.0.0.1';
    }

    /**
     * Log user activity
     *
     * @param string $action Action
     * @param array $details Additional details
     * @return void
     */
    public static function logActivity($action, $details = [])
    {
        $logEntry = [
            'timestamp' => date('Y-m-d H:i:s'),
            'user_id' => self::getUserId(),
            'ip' => self::getUserIp(),
            'action' => $action,
            'details' => $details
        ];

        $logFile = 'logs/user_activity.log';
        $logDir = dirname($logFile);

        if (!is_dir($logDir)) {
            mkdir($logDir, 0755, true);
        }

        file_put_contents($logFile, json_encode($logEntry) . PHP_EOL, FILE_APPEND | LOCK_EX);
    }

    /**
     * Validate password strength
     *
     * @param string $password Password
     * @return array Validation result
     */
    public static function validatePasswordStrength($password)
    {
        $errors = [];

        if (strlen($password) < 8) {
            $errors[] = 'Password must be at least 8 characters long';
        }

        if (!preg_match('/[A-Z]/', $password)) {
            $errors[] = 'Password must contain at least one uppercase letter';
        }

        if (!preg_match('/[a-z]/', $password)) {
            $errors[] = 'Password must contain at least one lowercase letter';
        }

        if (!preg_match('/[0-9]/', $password)) {
            $errors[] = 'Password must contain at least one digit';
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Generate remember me token
     *
     * @return array Token data
     */
    public static function generateRememberMeToken()
    {
        $selector = self::generateToken(16);
        $validator = self::generateToken(32);
        $token = $selector . $validator;

        return [
            'selector' => $selector,
            'validator' => $validator,
            'token' => $token
        ];
    }

    /**
     * Sanitize input
     *
     * @param string $input Input string
     * @return string Sanitized input
     */
    public static function sanitizeInput($input)
    {
        return htmlspecialchars(trim($input), ENT_QUOTES, 'UTF-8');
    }

    /**
     * Validate email
     *
     * @param string $email Email address
     * @return bool
     */
    public static function validateEmail($email)
    {
        return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    }

    /**
     * Check rate limiting
     *
     * @param string $key Rate limit key
     * @param int $limit Request limit
     * @param int $window Time window in seconds
     * @return bool
     */
    public static function checkRateLimit($key, $limit = 10, $window = 60)
    {
        $cacheKey = 'rate_limit_' . md5($key);
        $current = $_SESSION[$cacheKey] ?? ['count' => 0, 'reset_time' => time() + $window];

        // Reset if window expired
        if (time() > $current['reset_time']) {
            $current = ['count' => 0, 'reset_time' => time() + $window];
        }

        // Check limit
        if ($current['count'] >= $limit) {
            return false;
        }

        // Increment count
        $current['count']++;
        $_SESSION[$cacheKey] = $current;

        return true;
    }
}
