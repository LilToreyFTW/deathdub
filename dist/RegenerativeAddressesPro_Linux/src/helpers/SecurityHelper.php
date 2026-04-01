<?php

/**
 * Security Helper
 * PSR-2 compliant
 */

class SecurityHelper
{
    /**
     * Generate secure random string
     *
     * @param int $length String length
     * @return string
     */
    public static function generateRandomString($length = 32)
    {
        return bin2hex(random_bytes($length / 2));
    }

    /**
     * Encrypt data
     *
     * @param string $data Data to encrypt
     * @param string $key Encryption key
     * @return string|bool Encrypted data or false on failure
     */
    public static function encrypt($data, $key)
    {
        try {
            $iv = random_bytes(openssl_cipher_iv_length('aes-256-cbc'));
            $encrypted = openssl_encrypt($data, 'aes-256-cbc', $key, 0, $iv);
            return base64_encode($iv . $encrypted);
        } catch (Exception $e) {
            error_log('Encryption failed: ' . $e->getMessage());
            return false;
        }
    }

    /**
     * Decrypt data
     *
     * @param string $data Data to decrypt
     * @param string $key Decryption key
     * @return string|bool Decrypted data or false on failure
     */
    public static function decrypt($data, $key)
    {
        try {
            $data = base64_decode($data);
            $iv = substr($data, 0, openssl_cipher_iv_length('aes-256-cbc'));
            $encrypted = substr($data, openssl_cipher_iv_length('aes-256-cbc'));
            return openssl_decrypt($encrypted, 'aes-256-cbc', $key, 0, $iv);
        } catch (Exception $e) {
            error_log('Decryption failed: ' . $e->getMessage());
            return false;
        }
    }

    /**
     * Generate HMAC hash
     *
     * @param string $data Data to hash
     * @param string $key Hash key
     * @return string HMAC hash
     */
    public static function hmac($data, $key)
    {
        return hash_hmac('sha256', $data, $key);
    }

    /**
     * Validate data integrity
     *
     * @param string $data Original data
     * @param string $hash HMAC hash
     * @param string $key Hash key
     * @return bool
     */
    public static function validateIntegrity($data, $hash, $key)
    {
        return hash_equals(self::hmac($data, $key), $hash);
    }

    /**
     * Sanitize filename
     *
     * @param string $filename Filename
     * @return string Sanitized filename
     */
    public static function sanitizeFilename($filename)
    {
        $filename = preg_replace('/[^a-zA-Z0-9._-]/', '_', $filename);
        $filename = preg_replace('/__+/', '_', $filename);
        $filename = trim($filename, '_');
        return empty($filename) ? 'unnamed_file' : $filename;
    }

    /**
     * Validate file type
     *
     * @param string $filename Filename
     * @param array $allowedTypes Allowed file types
     * @return bool
     */
    public static function validateFileType($filename, $allowedTypes = [])
    {
        if (empty($allowedTypes)) {
            $allowedTypes = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'txt', 'csv', 'json'];
        }

        $extension = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
        return in_array($extension, $allowedTypes);
    }

    /**
     * Validate file size
     *
     * @param int $size File size in bytes
     * @param int $maxSize Maximum allowed size in bytes
     * @return bool
     */
    public static function validateFileSize($size, $maxSize = 5242880)
    {
        return $size <= $maxSize;
    }

    /**
     * Generate secure file path
     *
     * @param string $filename Filename
     * @param string $directory Directory
     * @return string Secure file path
     */
    public static function generateSecurePath($filename, $directory = 'uploads')
    {
        $sanitized = self::sanitizeFilename($filename);
        $randomPrefix = self::generateRandomString(8);
        $subDir = substr($randomPrefix, 0, 2);
        
        $fullDir = $directory . '/' . $subDir;
        if (!is_dir($fullDir)) {
            mkdir($fullDir, 0755, true);
        }

        return $fullDir . '/' . $randomPrefix . '_' . $sanitized;
    }

    /**
     * Filter input
     *
     * @param mixed $input Input data
     * @param string $type Filter type
     * @param array $options Filter options
     * @return mixed Filtered data
     */
    public static function filterInput($input, $type = 'string', $options = [])
    {
        switch ($type) {
            case 'email':
                return filter_var($input, FILTER_VALIDATE_EMAIL);
            case 'url':
                return filter_var($input, FILTER_VALIDATE_URL);
            case 'int':
                return filter_var($input, FILTER_VALIDATE_INT, $options);
            case 'float':
                return filter_var($input, FILTER_VALIDATE_FLOAT);
            case 'boolean':
                return filter_var($input, FILTER_VALIDATE_BOOLEAN);
            case 'ip':
                return filter_var($input, FILTER_VALIDATE_IP);
            case 'string':
            default:
                return htmlspecialchars(trim($input), ENT_QUOTES, 'UTF-8');
        }
    }

    /**
     * Check for SQL injection patterns
     *
     * @param string $input Input string
     * @return bool True if suspicious
     */
    public static function detectSqlInjection($input)
    {
        $patterns = [
            '/(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|EXEC|ALTER|CREATE)\b)/i',
            '/(--|#|\/\*|\*\/|;)/',
            '/(\b(OR|AND)\s+\d+\s*=\s*\d+)/i',
            '/(\b(OR|AND)\s+["\'][^"\']+["\']\s*=\s*["\'][^"\']+["\'])/i'
        ];

        foreach ($patterns as $pattern) {
            if (preg_match($pattern, $input)) {
                return true;
            }
        }

        return false;
    }

    /**
     * Check for XSS patterns
     *
     * @param string $input Input string
     * @return bool True if suspicious
     */
    public static function detectXss($input)
    {
        $patterns = [
            '/<script[^>]*>.*?<\/script>/i',
            '/<iframe[^>]*>.*?<\/iframe>/i',
            '/<object[^>]*>.*?<\/object>/i',
            '/<embed[^>]*>.*?<\/embed>/i',
            '/javascript:/i',
            '/on\w+\s*=/i'
        ];

        foreach ($patterns as $pattern) {
            if (preg_match($pattern, $input)) {
                return true;
            }
        }

        return false;
    }

    /**
     * Generate password hash
     *
     * @param string $password Password
     * @param array $options Hash options
     * @return string Hashed password
     */
    public static function generatePasswordHash($password, $options = [])
    {
        $defaultOptions = [
            'cost' => 12
        ];

        $options = array_merge($defaultOptions, $options);
        return password_hash($password, PASSWORD_BCRYPT, $options);
    }

    /**
     * Verify password
     *
     * @param string $password Password
     * @param string $hash Hash
     * @return bool
     */
    public static function verifyPassword($password, $hash)
    {
        return password_verify($password, $hash);
    }

    /**
     * Check if password needs rehashing
     *
     * @param string $hash Password hash
     * @param array $options Hash options
     * @return bool
     */
    public static function passwordNeedsRehash($hash, $options = [])
    {
        return password_needs_rehash($hash, PASSWORD_BCRYPT, $options);
    }

    /**
     * Generate API key
     *
     * @param int $length Key length
     * @return string API key
     */
    public static function generateApiKey($length = 32)
    {
        return 'api_' . self::generateRandomString($length);
    }

    /**
     * Validate API key
     *
     * @param string $apiKey API key
     * @return bool
     */
    public static function validateApiKey($apiKey)
    {
        return preg_match('/^api_[a-f0-9]{32,64}$/', $apiKey);
    }

    /**
     * Log security event
     *
     * @param string $event Event type
     * @param array $details Event details
     * @return void
     */
    public static function logSecurityEvent($event, $details = [])
    {
        $logEntry = [
            'timestamp' => date('Y-m-d H:i:s'),
            'event' => $event,
            'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
            'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'unknown',
            'details' => $details
        ];

        $logFile = 'logs/security.log';
        $logDir = dirname($logFile);

        if (!is_dir($logDir)) {
            mkdir($logDir, 0755, true);
        }

        file_put_contents($logFile, json_encode($logEntry) . PHP_EOL, FILE_APPEND | LOCK_EX);
    }

    /**
     * Check for suspicious activity
     *
     * @param string $ip IP address
     * @param string $action Action
     * @param int $threshold Threshold
     * @param int $window Time window in seconds
     * @return bool
     */
    public static function checkSuspiciousActivity($ip, $action, $threshold = 10, $window = 300)
    {
        $cacheKey = 'suspicious_' . md5($ip . $action);
        $current = $_SESSION[$cacheKey] ?? ['count' => 0, 'reset_time' => time() + $window];

        if (time() > $current['reset_time']) {
            $current = ['count' => 0, 'reset_time' => time() + $window];
        }

        if ($current['count'] >= $threshold) {
            self::logSecurityEvent('suspicious_activity', [
                'ip' => $ip,
                'action' => $action,
                'count' => $current['count']
            ]);
            return true;
        }

        $current['count']++;
        $_SESSION[$cacheKey] = $current;

        return false;
    }
}
