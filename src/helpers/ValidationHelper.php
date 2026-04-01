<?php

/**
 * Validation Helper
 * PSR-2 compliant
 */

class ValidationHelper
{
    /**
     * Validate required fields
     *
     * @param array $data Data to validate
     * @param array $required Required fields
     * @return array Validation result
     */
    public static function validateRequired($data, $required)
    {
        $errors = [];

        foreach ($required as $field) {
            if (!isset($data[$field]) || empty($data[$field])) {
                $errors[$field] = "Field {$field} is required";
            }
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Validate email
     *
     * @param string $email Email address
     * @return array Validation result
     */
    public static function validateEmail($email)
    {
        $errors = [];

        if (empty($email)) {
            $errors['email'] = 'Email address is required';
        } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $errors['email'] = 'Invalid email address format';
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Validate password
     *
     * @param string $password Password
     * @param array $options Validation options
     * @return array Validation result
     */
    public static function validatePassword($password, $options = [])
    {
        $errors = [];
        $defaultOptions = [
            'min_length' => 8,
            'max_length' => 128,
            'require_uppercase' => true,
            'require_lowercase' => true,
            'require_numbers' => true,
            'require_special' => true
        ];

        $options = array_merge($defaultOptions, $options);

        if (empty($password)) {
            $errors['password'] = 'Password is required';
        } else {
            if (strlen($password) < $options['min_length']) {
                $errors['password'] = "Password must be at least {$options['min_length']} characters long";
            }

            if (strlen($password) > $options['max_length']) {
                $errors['password'] = "Password must not exceed {$options['max_length']} characters";
            }

            if ($options['require_uppercase'] && !preg_match('/[A-Z]/', $password)) {
                $errors['password'] = 'Password must contain at least one uppercase letter';
            }

            if ($options['require_lowercase'] && !preg_match('/[a-z]/', $password)) {
                $errors['password'] = 'Password must contain at least one lowercase letter';
            }

            if ($options['require_numbers'] && !preg_match('/[0-9]/', $password)) {
                $errors['password'] = 'Password must contain at least one number';
            }

            if ($options['require_special'] && !preg_match('/[!@#$%^&*(),.?":{}|<>]/', $password)) {
                $errors['password'] = 'Password must contain at least one special character';
            }
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Validate username
     *
     * @param string $username Username
     * @param array $options Validation options
     * @return array Validation result
     */
    public static function validateUsername($username, $options = [])
    {
        $errors = [];
        $defaultOptions = [
            'min_length' => 3,
            'max_length' => 20,
            'allowed_chars' => 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'
        ];

        $options = array_merge($defaultOptions, $options);

        if (empty($username)) {
            $errors['username'] = 'Username is required';
        } else {
            if (strlen($username) < $options['min_length']) {
                $errors['username'] = "Username must be at least {$options['min_length']} characters long";
            }

            if (strlen($username) > $options['max_length']) {
                $errors['username'] = "Username must not exceed {$options['max_length']} characters";
            }

            if (!preg_match('/^[' . preg_quote($options['allowed_chars'], '/') . ']+$/', $username)) {
                $errors['username'] = 'Username contains invalid characters';
            }
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Validate URL
     *
     * @param string $url URL
     * @param array $options Validation options
     * @return array Validation result
     */
    public static function validateUrl($url, $options = [])
    {
        $errors = [];
        $defaultOptions = [
            'require_protocol' => true,
            'allowed_protocols' => ['http', 'https']
        ];

        $options = array_merge($defaultOptions, $options);

        if (empty($url)) {
            $errors['url'] = 'URL is required';
        } else {
            if (!filter_var($url, FILTER_VALIDATE_URL)) {
                $errors['url'] = 'Invalid URL format';
            } else {
                $parsed = parse_url($url);
                
                if ($options['require_protocol'] && !in_array($parsed['scheme'], $options['allowed_protocols'])) {
                    $errors['url'] = 'URL must use ' . implode(' or ', $options['allowed_protocols']) . ' protocol';
                }

                if (empty($parsed['host'])) {
                    $errors['url'] = 'URL must contain a valid domain';
                }
            }
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Validate numeric value
     *
     * @param mixed $value Value to validate
     * @param array $options Validation options
     * @return array Validation result
     */
    public static function validateNumeric($value, $options = [])
    {
        $errors = [];
        $defaultOptions = [
            'min' => null,
            'max' => null,
            'integer_only' => false
        ];

        $options = array_merge($defaultOptions, $options);

        if (!is_numeric($value)) {
            $errors['numeric'] = 'Value must be numeric';
        } else {
            $numValue = $options['integer_only'] ? (int)$value : (float)$value;

            if ($options['min'] !== null && $numValue < $options['min']) {
                $errors['numeric'] = "Value must be at least {$options['min']}";
            }

            if ($options['max'] !== null && $numValue > $options['max']) {
                $errors['numeric'] = "Value must not exceed {$options['max']}";
            }
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Validate string length
     *
     * @param string $value String value
     * @param array $options Validation options
     * @return array Validation result
     */
    public static function validateLength($value, $options = [])
    {
        $errors = [];
        $defaultOptions = [
            'min' => null,
            'max' => null
        ];

        $options = array_merge($defaultOptions, $options);
        $length = strlen($value);

        if ($options['min'] !== null && $length < $options['min']) {
            $errors['length'] = "Value must be at least {$options['min']} characters long";
        }

        if ($options['max'] !== null && $length > $options['max']) {
            $errors['length'] = "Value must not exceed {$options['max']} characters";
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Validate date
     *
     * @param string $date Date string
     * @param string $format Expected date format
     * @return array Validation result
     */
    public static function validateDate($date, $format = 'Y-m-d')
    {
        $errors = [];

        if (empty($date)) {
            $errors['date'] = 'Date is required';
        } else {
            $d = DateTime::createFromFormat($format, $date);
            
            if (!$d || $d->format($format) !== $date) {
                $errors['date'] = "Invalid date format. Expected format: {$format}";
            }
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Validate file upload
     *
     * @param array $file File data from $_FILES
     * @param array $options Validation options
     * @return array Validation result
     */
    public static function validateFile($file, $options = [])
    {
        $errors = [];
        $defaultOptions = [
            'max_size' => 5242880, // 5MB
            'allowed_types' => ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'txt', 'csv'],
            'required' => true
        ];

        $options = array_merge($defaultOptions, $options);

        if ($options['required'] && (empty($file) || $file['error'] === UPLOAD_ERR_NO_FILE)) {
            $errors['file'] = 'File is required';
        } elseif (!empty($file) && $file['error'] !== UPLOAD_ERR_NO_FILE) {
            if ($file['error'] !== UPLOAD_ERR_OK) {
                $errors['file'] = 'File upload error: ' . self::getUploadErrorMessage($file['error']);
            } else {
                if ($file['size'] > $options['max_size']) {
                    $errors['file'] = 'File size exceeds maximum allowed size';
                }

                $extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
                if (!in_array($extension, $options['allowed_types'])) {
                    $errors['file'] = 'File type not allowed';
                }
            }
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Get upload error message
     *
     * @param int $error_code Upload error code
     * @return string Error message
     */
    private static function getUploadErrorMessage($error_code)
    {
        switch ($error_code) {
            case UPLOAD_ERR_INI_SIZE:
                return 'The uploaded file exceeds the upload_max_filesize directive in php.ini';
            case UPLOAD_ERR_FORM_SIZE:
                return 'The uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the HTML form';
            case UPLOAD_ERR_PARTIAL:
                return 'The uploaded file was only partially uploaded';
            case UPLOAD_ERR_NO_FILE:
                return 'No file was uploaded';
            case UPLOAD_ERR_NO_TMP_DIR:
                return 'Missing a temporary folder';
            case UPLOAD_ERR_CANT_WRITE:
                return 'Failed to write file to disk';
            case UPLOAD_ERR_EXTENSION:
                return 'A PHP extension stopped the file upload';
            default:
                return 'Unknown upload error';
        }
    }

    /**
     * Validate regex pattern
     *
     * @param string $value Value to validate
     * @param string $pattern Regex pattern
     * @param string $message Error message
     * @return array Validation result
     */
    public static function validateRegex($value, $pattern, $message = 'Invalid format')
    {
        $errors = [];

        if (!preg_match($pattern, $value)) {
            $errors['regex'] = $message;
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Validate phone number
     *
     * @param string $phone Phone number
     * @param string $country Country code
     * @return array Validation result
     */
    public static function validatePhone($phone, $country = 'US')
    {
        $errors = [];

        if (empty($phone)) {
            $errors['phone'] = 'Phone number is required';
        } else {
            // Remove all non-numeric characters
            $cleanPhone = preg_replace('/[^0-9]/', '', $phone);

            switch ($country) {
                case 'US':
                    if (!preg_match('/^1?[0-9]{10}$/', $cleanPhone)) {
                        $errors['phone'] = 'Invalid US phone number format';
                    }
                    break;
                default:
                    if (strlen($cleanPhone) < 10 || strlen($cleanPhone) > 15) {
                        $errors['phone'] = 'Invalid phone number format';
                    }
                    break;
            }
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }

    /**
     * Sanitize and validate input
     *
     * @param array $data Input data
     * @param array $rules Validation rules
     * @return array Validation result
     */
    public static function validateAndSanitize($data, $rules)
    {
        $sanitized = [];
        $errors = [];

        foreach ($rules as $field => $fieldRules) {
            $value = $data[$field] ?? null;

            // Sanitize
            if (isset($fieldRules['sanitize'])) {
                switch ($fieldRules['sanitize']) {
                    case 'email':
                        $value = filter_var($value, FILTER_SANITIZE_EMAIL);
                        break;
                    case 'url':
                        $value = filter_var($value, FILTER_SANITIZE_URL);
                        break;
                    case 'string':
                        $value = htmlspecialchars(trim($value), ENT_QUOTES, 'UTF-8');
                        break;
                    case 'int':
                        $value = filter_var($value, FILTER_SANITIZE_NUMBER_INT);
                        break;
                    case 'float':
                        $value = filter_var($value, FILTER_SANITIZE_NUMBER_FLOAT);
                        break;
                }
            }

            $sanitized[$field] = $value;

            // Validate
            if (isset($fieldRules['required']) && $fieldRules['required'] && empty($value)) {
                $errors[$field] = "Field {$field} is required";
                continue;
            }

            if (!empty($value)) {
                foreach ($fieldRules as $rule => $ruleValue) {
                    if ($rule === 'required' || $rule === 'sanitize') {
                        continue;
                    }

                    switch ($rule) {
                        case 'email':
                            $result = self::validateEmail($value);
                            break;
                        case 'password':
                            $result = self::validatePassword($value, $ruleValue);
                            break;
                        case 'username':
                            $result = self::validateUsername($value, $ruleValue);
                            break;
                        case 'url':
                            $result = self::validateUrl($value, $ruleValue);
                            break;
                        case 'numeric':
                            $result = self::validateNumeric($value, $ruleValue);
                            break;
                        case 'length':
                            $result = self::validateLength($value, $ruleValue);
                            break;
                        case 'date':
                            $result = self::validateDate($value, $ruleValue);
                            break;
                        case 'regex':
                            $result = self::validateRegex($value, $ruleValue['pattern'], $ruleValue['message'] ?? 'Invalid format');
                            break;
                        case 'phone':
                            $result = self::validatePhone($value, $ruleValue);
                            break;
                        default:
                            $result = ['valid' => true, 'errors' => []];
                            break;
                    }

                    if (!$result['valid']) {
                        $errors[$field] = $result['errors'][array_keys($result['errors'])[0]];
                        break;
                    }
                }
            }
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors,
            'sanitized' => $sanitized
        ];
    }
}
