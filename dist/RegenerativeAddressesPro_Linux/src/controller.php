<?php

/**
 * Controller Class for Regenerative Addresses Tool
 * Fixed redirect functionality
 */

class Controller
{
    /**
     * Behaviors
     *
     * @var array
     */
    private $_behaviors = [];

    /**
     * Constructor
     */
    public function __construct()
    {
        $this->beforeRequest();
    }

    /**
     * Get behaviors
     *
     * @return array
     */
    public function behaviors()
    {
        return [];
    }

    /**
     * Load model
     *
     * @param string $name Model name
     * @return Model
     */
    public function loadModel($name)
    {
        require APP_DIR . '/models/' . strtolower($name) . '.php';

        $model = new $name();

        return $model;
    }

    /**
     * Load view
     *
     * @param string $name View name
     * @return View
     */
    public function loadView($name)
    {
        $view = new View($name);

        return $view;
    }

    /**
     * Load plugin
     *
     * @param string $name Plugin name
     * @return void
     */
    public function loadPlugin($name)
    {
        require APP_DIR . '/plugins/' . strtolower($name) . '.php';
    }

    /**
     * Load helper
     *
     * @param string $name Helper name
     * @return mixed
     */
    public function loadHelper($name)
    {
        require APP_DIR . '/helpers/' . strtolower($name) . '.php';
        $helper = new $name();
        return $helper;
    }

    /**
     * Redirect to location
     * Fixed redirect functionality
     *
     * @param string $loc Location to redirect to
     * @return void
     */
    public function redirect($loc)
    {
        // Clean output buffer before redirect
        if (ob_get_length() > 0) {
            ob_end_clean();
        }

        // Build full URL
        $base_url = goat::$app->config['base_url'] ?? '';
        $redirect_url = rtrim($base_url, '/') . '/' . ltrim($loc, '/');

        // Perform redirect
        header('Location: ' . $redirect_url);
        exit();
    }

    /**
     * Get current route
     *
     * @return string Current route
     */
    public function route()
    {
        return $_SERVER['REQUEST_URI'] ?? '';
    }

    /**
     * Before request handler
     * Check behaviors
     *
     * @return void
     */
    private function beforeRequest()
    {
        // This is overridden, then check if data is set
        $this->_behaviors = $this->behaviors();

        // Requires logging
        if (isset($this->_behaviors['access'])) {
            // All auth users, no matters what role
            if (isset($this->_behaviors['access']['rules']['isLogged']) &&
                $this->_behaviors['access']['rules']['isLogged'] == 'true') {
                
                // Load the helper, might pass error as param
                $helper = $this->loadHelper('AuthVerify');
                $resp = $helper->verify();

                if (isset($resp['Error'])) {
                    if (isset(goat::$app->config['display_login_error']) &&
                        goat::$app->config['display_login_error'] == 'true') {
                        goat::$app->setFlash('_login_error', $resp);
                    }
                    
                    $error_controller = goat::$app->config['error_controller'] ?? 'errors';
                    $error_type = goat::$app->config['error_type']['403'] ?? 'forbidden';
                    
                    $template = $this->redirect($error_controller . '/' . $error_type);
                    $template->render();
                }
            }
        }
    }

    /**
     * Validate input data
     *
     * @param array $data Data to validate
     * @param array $rules Validation rules
     * @return array Validation result
     */
    public function validate($data, $rules)
    {
        $errors = [];

        foreach ($rules as $field => $field_rules) {
            $value = $data[$field] ?? null;

            foreach ($field_rules as $rule => $rule_value) {
                switch ($rule) {
                    case 'required':
                        if (empty($value)) {
                            $errors[$field][] = "Field {$field} is required";
                        }
                        break;

                    case 'email':
                        if (!empty($value) && !filter_var($value, FILTER_VALIDATE_EMAIL)) {
                            $errors[$field][] = "Field {$field} must be a valid email";
                        }
                        break;

                    case 'min_length':
                        if (!empty($value) && strlen($value) < $rule_value) {
                            $errors[$field][] = "Field {$field} must be at least {$rule_value} characters";
                        }
                        break;

                    case 'max_length':
                        if (!empty($value) && strlen($value) > $rule_value) {
                            $errors[$field][] = "Field {$field} must not exceed {$rule_value} characters";
                        }
                        break;

                    case 'numeric':
                        if (!empty($value) && !is_numeric($value)) {
                            $errors[$field][] = "Field {$field} must be numeric";
                        }
                        break;

                    case 'alpha':
                        if (!empty($value) && !ctype_alpha($value)) {
                            $errors[$field][] = "Field {$field} must contain only letters";
                        }
                        break;

                    case 'alphanumeric':
                        if (!empty($value) && !ctype_alnum($value)) {
                            $errors[$field][] = "Field {$field} must contain only letters and numbers";
                        }
                        break;

                    case 'regex':
                        if (!empty($value) && !preg_match($rule_value, $value)) {
                            $errors[$field][] = "Field {$field} format is invalid";
                        }
                        break;
                }
            }
        }

        return [
            'success' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Send JSON response
     *
     * @param mixed $data Response data
     * @param int $status HTTP status code
     * @return void
     */
    public function sendJsonResponse($data, $status = 200)
    {
        // Clean output buffer
        if (ob_get_length() > 0) {
            ob_end_clean();
        }

        http_response_code($status);
        header('Content-Type: application/json');
        echo json_encode($data);
        exit();
    }

    /**
     * Send error response
     *
     * @param string $message Error message
     * @param int $status HTTP status code
     * @return void
     */
    public function sendErrorResponse($message, $status = 400)
    {
        $this->sendJsonResponse([
            'success' => false,
            'error' => $message
        ], $status);
    }

    /**
     * Send success response
     *
     * @param mixed $data Response data
     * @return void
     */
    public function sendSuccessResponse($data = null)
    {
        $response = ['success' => true];
        
        if ($data !== null) {
            $response['data'] = $data;
        }

        $this->sendJsonResponse($response);
    }

    /**
     * Get POST data with validation
     *
     * @param string $key Data key
     * @param mixed $default Default value
     * @param callable $filter Filter function
     * @return mixed POST data
     */
    public function getPostData($key = null, $default = null, $filter = null)
    {
        if ($key === null) {
            return $_POST;
        }

        $value = isset($_POST[$key]) ? $_POST[$key] : $default;

        if ($filter !== null && is_callable($filter)) {
            $value = $filter($value);
        }

        return $value;
    }

    /**
     * Get GET data with validation
     *
     * @param string $key Data key
     * @param mixed $default Default value
     * @param callable $filter Filter function
     * @return mixed GET data
     */
    public function getGetData($key = null, $default = null, $filter = null)
    {
        if ($key === null) {
            return $_GET;
        }

        $value = isset($_GET[$key]) ? $_GET[$key] : $default;

        if ($filter !== null && is_callable($filter)) {
            $value = $filter($value);
        }

        return $value;
    }

    /**
     * Check if request is POST
     *
     * @return bool True if POST request
     */
    public function isPost()
    {
        return $_SERVER['REQUEST_METHOD'] === 'POST';
    }

    /**
     * Check if request is GET
     *
     * @return bool True if GET request
     */
    public function isGet()
    {
        return $_SERVER['REQUEST_METHOD'] === 'GET';
    }

    /**
     * Check if request is AJAX
     *
     * @return bool True if AJAX request
     */
    public function isAjax()
    {
        return isset($_SERVER['HTTP_X_REQUESTED_WITH']) &&
               strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest';
    }

    /**
     * Set page title
     *
     * @param string $title Page title
     * @return void
     */
    public function setPageTitle($title)
    {
        goat::$app->setConfig('page_title', $title);
    }

    /**
     * Get page title
     *
     * @return string Page title
     */
    public function getPageTitle()
    {
        return goat::$app->getConfig('page_title', 'Regenerative Addresses Tool');
    }

    /**
     * Add CSS file
     *
     * @param string $css_file CSS file path
     * @return void
     */
    public function addCss($css_file)
    {
        $css_files = goat::$app->getConfig('css_files', []);
        $css_files[] = $css_file;
        goat::$app->setConfig('css_files', $css_files);
    }

    /**
     * Add JavaScript file
     *
     * @param string $js_file JavaScript file path
     * @return void
     */
    public function addJs($js_file)
    {
        $js_files = goat::$app->getConfig('js_files', []);
        $js_files[] = $js_file;
        goat::$app->setConfig('js_files', $js_files);
    }
}
