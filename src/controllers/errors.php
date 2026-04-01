<?php

/**
 * Errors Controller
 * Sends HTTP Status in error pages
 */

class errors extends Controller
{
    /**
     * 404 Not Found Error
     */
    public function not_found()
    {
        // Send HTTP Status 404
        http_response_code(404);
        
        $view = $this->loadView('error');
        return $view->render([
            'error_code' => 404,
            'error_title' => 'Page Not Found',
            'error_message' => 'The requested page could not be found.',
            'error_description' => 'The URL you requested does not exist on this server.'
        ]);
    }

    /**
     * 403 Forbidden Error
     */
    public function forbidden()
    {
        // Send HTTP Status 403
        http_response_code(403);
        
        $view = $this->loadView('error');
        return $view->render([
            'error_code' => 403,
            'error_title' => 'Access Forbidden',
            'error_message' => 'You do not have permission to access this resource.',
            'error_description' => 'Please contact the administrator if you believe this is an error.'
        ]);
    }

    /**
     * 500 Server Error
     */
    public function server_error()
    {
        // Send HTTP Status 500
        http_response_code(500);
        
        $view = $this->loadView('error');
        return $view->render([
            'error_code' => 500,
            'error_title' => 'Internal Server Error',
            'error_message' => 'An unexpected error occurred.',
            'error_description' => 'The server encountered an error and could not complete your request.'
        ]);
    }

    /**
     * 400 Bad Request Error
     */
    public function bad_request()
    {
        // Send HTTP Status 400
        http_response_code(400);
        
        $view = $this->loadView('error');
        return $view->render([
            'error_code' => 400,
            'error_title' => 'Bad Request',
            'error_message' => 'The request was invalid.',
            'error_description' => 'Please check your request and try again.'
        ]);
    }

    /**
     * 401 Unauthorized Error
     */
    public function unauthorized()
    {
        // Send HTTP Status 401
        http_response_code(401);
        
        $view = $this->loadView('error');
        return $view->render([
            'error_code' => 401,
            'error_title' => 'Unauthorized',
            'error_message' => 'Authentication required.',
            'error_description' => 'Please log in to access this resource.'
        ]);
    }

    /**
     * 429 Too Many Requests Error
     */
    public function rate_limit()
    {
        // Send HTTP Status 429
        http_response_code(429);
        
        $view = $this->loadView('error');
        return $view->render([
            'error_code' => 429,
            'error_title' => 'Too Many Requests',
            'error_message' => 'Rate limit exceeded.',
            'error_description' => 'Please wait before making another request.'
        ]);
    }

    /**
     * 503 Service Unavailable Error
     */
    public function service_unavailable()
    {
        // Send HTTP Status 503
        http_response_code(503);
        
        $view = $this->loadView('error');
        return $view->render([
            'error_code' => 503,
            'error_title' => 'Service Unavailable',
            'error_message' => 'The service is temporarily unavailable.',
            'error_description' => 'Please try again later.'
        ]);
    }

    /**
     * Generic Error Handler
     */
    public function generic($error_code = 500, $error_message = 'An error occurred')
    {
        // Send HTTP Status
        http_response_code($error_code);
        
        $view = $this->loadView('error');
        return $view->render([
            'error_code' => $error_code,
            'error_title' => 'Error',
            'error_message' => $error_message,
            'error_description' => 'An error occurred while processing your request.'
        ]);
    }

    /**
     * JSON Error Response
     */
    public function json_error($error_code = 400, $error_message = 'Error', $data = [])
    {
        // Send HTTP Status
        http_response_code($error_code);
        
        // Clean output buffer
        if (ob_get_length() > 0) {
            ob_end_clean();
        }
        
        // Send JSON response
        header('Content-Type: application/json');
        echo json_encode([
            'success' => false,
            'error' => $error_message,
            'error_code' => $error_code,
            'data' => $data
        ]);
        exit();
    }

    /**
     * Maintenance Mode
     */
    public function maintenance()
    {
        // Send HTTP Status 503
        http_response_code(503);
        
        $view = $this->loadView('maintenance');
        return $view->render([
            'error_code' => 503,
            'error_title' => 'Maintenance Mode',
            'error_message' => 'Site is under maintenance.',
            'error_description' => 'We are currently performing maintenance. Please check back soon.'
        ]);
    }
}
