<?php

/**
 * Goat Framework Class for Regenerative Addresses Tool
 * Checks output buffer length before clean
 */

class goat
{
    /**
     * Application instance
     *
     * @var goat
     */
    public static $app;

    /**
     * Configuration
     *
     * @var array
     */
    public $config;

    /**
     * Matched controller
     *
     * @var string
     */
    protected $matched_controller;

    /**
     * Matched action
     *
     * @var string
     */
    protected $matched_action;

    /**
     * Constructor
     *
     * @param array $config Application configuration
     */
    public function __construct($config)
    {
        // Set our defaults
        $this::$app = $this;
        $this->config = $config;
        $controller = $config['default_controller'];
        $action = 'index';
        $url = '';

        // Get request url and script url
        $request_url = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '';
        $script_url = isset($_SERVER['PHP_SELF']) ? $_SERVER['PHP_SELF'] : '';

        // Get our url path and trim the / of the left and the right
        if ($request_url != $script_url && $request_url . '.php' != $script_url) {
            $url = trim(
                preg_replace(
                    '/' . str_replace('/', '\/', str_replace('index.php', '', $script_url)) . '/',
                    '',
                    $request_url,
                    1
                ),
                '/'
            );
        }

        // Split the url into segments
        $segments = explode('/', $url);

        // Do our default checks
        if (isset($segments[0]) && $segments[0] != '') {
            if (strstr($segments[0], '.')) {
                $_t = explode('.', $segments[0]);
                $controller = $_t[0];
            } else {
                $controller = $segments[0];
            }
        }

        if (isset($segments[1]) && $segments[1] != '') {
            $action = $segments[1];
        }

        if (strstr($segments[0], '?') && strstr($segments[0], '=')) {
            $controller = explode('?', $segments[0])[0];
        }

        $path = APP_DIR . '/controllers/' . $controller . '.php';

        if (file_exists($path)) {
            require_once $path;
        } else {
            $controller = $this->config['error_controller'];
            require_once APP_DIR . '/controllers/' . $controller . '.php';
        }

        // Check the action exists
        if (!method_exists($controller, $action)) {
            $controller = $this->config['error_controller'];
            require_once APP_DIR . '/controllers/' . $controller . '.php';
            $action = 'index';
        }

        // Create object and call method
        $obj = new $controller();

        $this->matched_controller = $controller;
        $this->matched_action = $action;

        return call_user_func_array([$obj, $action], array_slice($segments, 2));
    }

    /**
     * Clean page output
     * Checks output buffer length before clean
     *
     * @return bool
     */
    public function cleanPage()
    {
        // Check the output buffer length before clean
        if (ob_get_length() > 0) {
            ob_end_clean();
        }

        return true;
    }

    /**
     * Set flash message
     *
     * @param string $key Flash key
     * @param mixed $mixed Flash value
     * @param int $views Number of views to keep
     * @return void
     */
    public function setFlash($key, $mixed, $views = 0)
    {
        $_SESSION['_flash'][$key] = $mixed;
        $_SESSION['_flash'][$key . '_views'] = $views;
    }

    /**
     * Get flash message
     *
     * @param string $key Flash key
     * @param bool $ignore Ignore delete behavior
     * @return mixed|null Flash value
     */
    public function getFlash($key, $ignore = false)
    {
        if (!isset($_SESSION['_flash'][$key])) {
            return null;
        }

        $flash = $_SESSION['_flash'][$key];

        if (!$ignore) {
            $_views = $_SESSION['_flash'][$key . '_views'];
            if ($_views == 0) {
                unset($_SESSION['_flash'][$key . '_views']);
                unset($_SESSION['_flash'][$key]);
            } else {
                $_views = (int) $_views - 1;
                $_SESSION['_flash'][$key . '_views'] = $_views;
            }
        }

        return $flash;
    }

    /**
     * Clear all flash messages
     *
     * @return bool Success status
     */
    public function clearFlash()
    {
        unset($_SESSION['_flash']);

        return true;
    }

    /**
     * Register inline JavaScript
     *
     * @param string $inlineJS JavaScript code
     * @return void
     */
    public function registerJs($inlineJS)
    {
        if (!empty($inlineJS)) {
            echo '<script type="text/javascript">' . $inlineJS . '</script>';
        }
    }

    /**
     * Get matched controller
     *
     * @return string Matched controller name
     */
    public function getMatchedController()
    {
        return $this->matched_controller;
    }

    /**
     * Get matched action
     *
     * @return string Matched action name
     */
    public function getMatchedAction()
    {
        return $this->matched_action;
    }

    /**
     * Get configuration value
     *
     * @param string $key Configuration key
     * @param mixed $default Default value
     * @return mixed Configuration value
     */
    public function getConfig($key, $default = null)
    {
        return isset($this->config[$key]) ? $this->config[$key] : $default;
    }

    /**
     * Set configuration value
     *
     * @param string $key Configuration key
     * @param mixed $value Configuration value
     * @return void
     */
    public function setConfig($key, $value)
    {
        $this->config[$key] = $value;
    }

    /**
     * Get base URL
     *
     * @return string Base URL
     */
    public function getBaseUrl()
    {
        return $this->config['base_url'] ?? '';
    }

    /**
     * Generate URL
     *
     * @param string $path URL path
     * @param array $params URL parameters
     * @return string Generated URL
     */
    public function generateUrl($path, $params = [])
    {
        $url = $this->getBaseUrl() . ltrim($path, '/');

        if (!empty($params)) {
            $url .= '?' . http_build_query($params);
        }

        return $url;
    }

    /**
     * Redirect to URL
     *
     * @param string $url Target URL
     * @return void
     */
    public function redirect($url)
    {
        // Clean output buffer before redirect
        $this->cleanPage();

        header('Location: ' . $url);
        exit();
    }

    /**
     * Check if request is AJAX
     *
     * @return bool True if AJAX request
     */
    public function isAjaxRequest()
    {
        return isset($_SERVER['HTTP_X_REQUESTED_WITH']) &&
               strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest';
    }

    /**
     * Get request method
     *
     * @return string Request method
     */
    public function getRequestMethod()
    {
        return $_SERVER['REQUEST_METHOD'] ?? 'GET';
    }

    /**
     * Get POST data
     *
     * @param string $key Data key
     * @param mixed $default Default value
     * @return mixed POST data
     */
    public function getPost($key = null, $default = null)
    {
        if ($key === null) {
            return $_POST;
        }

        return isset($_POST[$key]) ? $_POST[$key] : $default;
    }

    /**
     * Get GET data
     *
     * @param string $key Data key
     * @param mixed $default Default value
     * @return mixed GET data
     */
    public function getGet($key = null, $default = null)
    {
        if ($key === null) {
            return $_GET;
        }

        return isset($_GET[$key]) ? $_GET[$key] : $default;
    }

    /**
     * Log message
     *
     * @param string $message Log message
     * @param string $level Log level
     * @return void
     */
    public function log($message, $level = 'info')
    {
        $log_file = $this->getConfig('log_file', 'app.log');
        $timestamp = date('Y-m-d H:i:s');
        $log_entry = "[{$timestamp}] [{$level}] {$message}" . PHP_EOL;

        error_log($log_entry, 3, $log_file);
    }

    /**
     * Get client IP address
     *
     * @return string IP address
     */
    public function getClientIp()
    {
        $ip = null;

        if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
            $ip = $_SERVER['HTTP_CLIENT_IP'];
        } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
            $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
        } else {
            $ip = $_SERVER['REMOTE_ADDR'];
        }

        return $ip;
    }

    /**
     * Validate CSRF token
     *
     * @param string $token CSRF token
     * @return bool Valid token
     */
    public function validateCsrfToken($token)
    {
        if (!isset($_SESSION['csrf_token'])) {
            return false;
        }

        return hash_equals($_SESSION['csrf_token'], $token);
    }

    /**
     * Generate CSRF token
     *
     * @return string CSRF token
     */
    public function generateCsrfToken()
    {
        if (!isset($_SESSION['csrf_token'])) {
            $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
        }

        return $_SESSION['csrf_token'];
    }
}
