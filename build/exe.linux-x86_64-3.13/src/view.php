<?php

/**
 * View Class for Regenerative Addresses Tool
 * Handles template rendering with Head and Footer
 */

class View
{
    private $view_name;
    private $data = [];
    private $head_content = '';
    private $footer_content = '';

    public function __construct($view_name)
    {
        $this->view_name = $view_name;
    }

    /**
     * Set data for the view
     */
    public function setData($data)
    {
        $this->data = $data;
        return $this;
    }

    /**
     * Set head content for template
     */
    public function setHead($content)
    {
        $this->head_content = $content;
        return $this;
    }

    /**
     * Set footer content for template
     */
    public function setFooter($content)
    {
        $this->footer_content = $content;
        return $this;
    }

    /**
     * Render the view with Head and Footer
     */
    public function render($data = [])
    {
        // Merge provided data with existing data
        $this->data = array_merge($this->data, $data);

        // Start output buffering
        ob_start();

        // Include head template
        $this->includeTemplate('head');

        // Include main view
        $this->includeTemplate($this->view_name);

        // Include footer template
        $this->includeTemplate('footer');

        // Get buffered content
        $content = ob_get_clean();

        // Output the rendered content
        echo $content;

        return $content;
    }

    /**
     * Include a template file
     */
    private function includeTemplate($template_name)
    {
        $template_file = APP_DIR . '/views/' . $template_name . '.php';
        
        if (file_exists($template_file)) {
            // Extract data to make variables available in template
            extract($this->data);
            
            // Include custom head/footer content if available
            if ($template_name === 'head' && !empty($this->head_content)) {
                echo $this->head_content;
            } elseif ($template_name === 'footer' && !empty($this->footer_content)) {
                echo $this->footer_content;
            } else {
                include $template_file;
            }
        } else {
            // Fallback content if template doesn't exist
            $this->renderFallbackContent($template_name);
        }
    }

    /**
     * Render fallback content for missing templates
     */
    private function renderFallbackContent($template_name)
    {
        switch ($template_name) {
            case 'head':
                echo '<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Regenerative Addresses Tool</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #333; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .footer { background: #333; color: white; padding: 20px; text-align: center; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Regenerative Addresses Tool</h1>
    </div>
    <div class="container">
        <div class="content">';
                break;

            case 'footer':
                echo '        </div>
        <div class="footer">
            <p>&copy; ' . date('Y') . ' Regenerative Addresses Tool - Educational Purpose Only</p>
        </div>
    </div>
</body>
</html>';
                break;

            default:
                echo '<p>Template "' . htmlspecialchars($template_name) . '" not found.</p>';
                break;
        }
    }

    /**
     * Render JSON response
     */
    public function renderJson($data)
    {
        header('Content-Type: application/json');
        echo json_encode($data);
    }

    /**
     * Render error page
     */
    public function renderError($message, $code = 500)
    {
        http_response_code($code);
        $this->setData([
            'error_message' => $message,
            'error_code' => $code
        ]);
        return $this->render('error');
    }

    /**
     * Get view name
     */
    public function getViewName()
    {
        return $this->view_name;
    }

    /**
     * Get data
     */
    public function getData()
    {
        return $this->data;
    }

    /**
     * Clean output buffer if needed
     */
    public function cleanBuffer()
    {
        if (ob_get_length() > 0) {
            ob_end_clean();
        }
        return true;
    }
}
