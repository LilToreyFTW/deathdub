<?php
/**
 * Regenerative Addresses Tool - Professional PHP API
 * Complete REST API for link regeneration and proxy management
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

// Database configuration
$db_config = [
    'host' => 'localhost',
    'dbname' => 'regenerative_addresses',
    'username' => 'root',
    'password' => ''
];

// Connect to database
try {
    $pdo = new PDO(
        "mysql:host={$db_config['host']};dbname={$db_config['dbname']};charset=utf8mb4",
        $db_config['username'],
        $db_config['password'],
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
        ]
    );
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Database connection failed']);
    exit;
}

// Get request method and action
$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? '';

// Request body for POST/PUT
$input = json_decode(file_get_contents('php://input'), true) ?? [];

// Authentication check
function authenticate() {
    $headers = getallheaders();
    $token = $headers['Authorization'] ?? '';
    
    // Simple token validation (implement proper JWT in production)
    if (empty($token)) {
        http_response_code(401);
        echo json_encode(['error' => 'Unauthorized']);
        exit;
    }
    
    return true;
}

// Response helper
function respond($data, $status = 200) {
    http_response_code($status);
    echo json_encode($data, JSON_PRETTY_PRINT);
    exit;
}

// Link Regeneration Class
class LinkRegenerator {
    private $techniques = [
        'add_parameters' => 'Add UTM tracking parameters',
        'change_subdomain' => 'Change URL subdomain',
        'add_path_segments' => 'Add random path segments',
        'change_tld' => 'Change top-level domain',
        'add_tracking_params' => 'Add custom tracking parameters',
        'shorten_url_style' => 'Convert to shortened URL style',
        'affiliate_style' => 'Convert to affiliate link format',
        'case_variation' => 'Change character case randomly',
        'encode_special' => 'Encode special characters',
        'mirror_domain' => 'Create mirrored domain variant'
    ];
    
    public function getTechniques() {
        return $this->techniques;
    }
    
    public function regenerate($url, $technique) {
        if (!isset($this->techniques[$technique])) {
            throw new Exception('Unknown technique: ' . $technique);
        }
        
        $method = '_technique_' . $technique;
        if (method_exists($this, $method)) {
            return $this->$method($url);
        }
        return $url;
    }
    
    private function _technique_add_parameters($url) {
        $params = [
            'utm_source=' . $this->randomString(8),
            'utm_medium=' . $this->randomString(6),
            'utm_campaign=' . $this->randomString(10),
            'utm_content=' . $this->randomString(8)
        ];
        $separator = strpos($url, '?') !== false ? '&' : '?';
        return $url . $separator . implode('&', $params);
    }
    
    private function _technique_change_subdomain($url) {
        $subdomains = ['www', 'm', 'mobile', 'app', 'api', 'secure', 'cdn', 'static'];
        $new_subdomain = $subdomains[array_rand($subdomains)];
        
        if (strpos($url, '://') !== false) {
            $parts = explode('://', $url);
            $domain_parts = explode('.', $parts[1]);
            if (count($domain_parts) > 2) {
                $domain_parts[0] = $new_subdomain;
                return $parts[0] . '://' . implode('.', $domain_parts);
            }
        }
        return $url;
    }
    
    private function _technique_add_path_segments($url) {
        $segments = [$this->randomString(8), $this->randomString(12)];
        return rtrim($url, '/') . '/' . implode('/', $segments);
    }
    
    private function _technique_change_tld($url) {
        $tlds = ['.com', '.net', '.org', '.info', '.co', '.io', '.me'];
        
        if (strpos($url, '://') !== false) {
            $parts = explode('://', $url);
            $domain = explode('/', $parts[1])[0];
            $domain_parts = explode('.', $domain);
            
            if (count($domain_parts) > 1) {
                $current_tld = '.' . end($domain_parts);
                $available_tlds = array_diff($tlds, [$current_tld]);
                
                if (!empty($available_tlds)) {
                    $new_tld = $available_tlds[array_rand($available_tlds)];
                    $domain_parts[count($domain_parts) - 1] = ltrim($new_tld, '.');
                    $new_domain = implode('.', $domain_parts);
                    return $parts[0] . '://' . $new_domain;
                }
            }
        }
        return $url;
    }
    
    private function _technique_add_tracking_params($url) {
        $params = [
            'tid=' . $this->randomString(8),
            'sid=' . $this->randomString(16),
            'ts=' . time()
        ];
        $separator = strpos($url, '?') !== false ? '&' : '?';
        return $url . $separator . implode('&', $params);
    }
    
    private function _technique_shorten_url_style($url) {
        $shorteners = ['bit.ly', 'tinyurl.com', 'short.ly', 't.co'];
        $shortener = $shorteners[array_rand($shorteners)];
        $shortCode = $this->randomString(6);
        return "https://{$shortener}/{$shortCode}";
    }
    
    private function _technique_affiliate_style($url) {
        $affiliateId = $this->randomString(8);
        $separator = strpos($url, '?') !== false ? '&' : '?';
        return $url . $separator . "aff={$affiliateId}&ref=partner";
    }
    
    private function _technique_case_variation($url) {
        $result = '';
        for ($i = 0; $i < strlen($url); $i++) {
            $char = $url[$i];
            if (ctype_alpha($char) && rand(0, 1)) {
                $result .= ctype_lower($char) ? strtoupper($char) : strtolower($char);
            } else {
                $result .= $char;
            }
        }
        return $result;
    }
    
    private function _technique_encode_special($url) {
        $special = [' ' => '%20', '?' => '%3F', '&' => '%26', '=' => '%3D'];
        foreach ($special as $char => $encoded) {
            if (rand(0, 1)) {
                $url = str_replace($char, $encoded, $url);
            }
        }
        return $url;
    }
    
    private function _technique_mirror_domain($url) {
        if (strpos($url, '://') !== false) {
            $parts = explode('://', $url);
            $domain = explode('/', $parts[1])[0];
            $mirrors = ['mirror1', 'mirror2', 'cdn', 'edge'];
            $mirror = $mirrors[array_rand($mirrors)];
            $newDomain = $mirror . '.' . $domain;
            return $parts[0] . '://' . $newDomain;
        }
        return $url;
    }
    
    private function randomString($length = 8) {
        $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        $result = '';
        for ($i = 0; $i < $length; $i++) {
            $result .= $chars[rand(0, strlen($chars) - 1)];
        }
        return $result;
    }
}

// Proxy Manager Class
class ProxyManager {
    private $pdo;
    
    public function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    public function getAll($limit = 1000, $status = null) {
        $sql = "SELECT * FROM proxies";
        $params = [];
        
        if ($status) {
            $sql .= " WHERE status = ?";
            $params[] = $status;
        }
        
        $sql .= " ORDER BY last_checked DESC LIMIT ?";
        $params[] = $limit;
        
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll();
    }
    
    public function add($address, $type = 'http') {
        try {
            $stmt = $this->pdo->prepare("INSERT IGNORE INTO proxies (address, type) VALUES (?, ?)");
            $stmt->execute([$address, $type]);
            return $stmt->rowCount() > 0;
        } catch (PDOException $e) {
            return false;
        }
    }
    
    public function updateStatus($address, $status, $responseTime = null) {
        $stmt = $this->pdo->prepare(
            "UPDATE proxies SET status = ?, response_time = ?, last_checked = NOW() WHERE address = ?"
        );
        return $stmt->execute([$status, $responseTime, $address]);
    }
    
    public function testProxy($proxy, $timeout = 10) {
        $result = [
            'proxy' => $proxy,
            'status' => 'unknown',
            'response_time' => null,
            'error' => null
        ];
        
        if (strpos($proxy, ':') === false) {
            $result['status'] = 'invalid';
            $result['error'] = 'Invalid proxy format';
            return $result;
        }
        
        list($host, $port) = explode(':', $proxy);
        $port = intval($port);
        
        $startTime = microtime(true);
        $socket = @fsockopen($host, $port, $errno, $errstr, $timeout);
        $responseTime = (microtime(true) - $startTime) * 1000;
        
        if ($socket) {
            fclose($socket);
            $result['status'] = 'active';
            $result['response_time'] = round($responseTime, 2);
        } else {
            $result['status'] = 'inactive';
            $result['error'] = "Connection failed: $errstr";
        }
        
        return $result;
    }
    
    public function getStats() {
        $stats = [];
        
        $stmt = $this->pdo->query("SELECT COUNT(*) as total FROM proxies");
        $stats['total'] = $stmt->fetch()['total'];
        
        $stmt = $this->pdo->query("SELECT COUNT(*) as active FROM proxies WHERE status = 'active'");
        $stats['active'] = $stmt->fetch()['active'];
        
        $stmt = $this->pdo->query("SELECT COUNT(*) as inactive FROM proxies WHERE status = 'inactive'");
        $stats['inactive'] = $stmt->fetch()['inactive'];
        
        $stmt = $this->pdo->query("SELECT AVG(response_time) as avg_time FROM proxies WHERE status = 'active'");
        $stats['avg_response_time'] = round($stmt->fetch()['avg_time'] ?? 0, 2);
        
        return $stats;
    }
}

// Route handling
try {
    $linkRegen = new LinkRegenerator();
    $proxyManager = new ProxyManager($pdo);
    
    switch ($action) {
        // Link Regeneration Endpoints
        case 'techniques':
            respond(['techniques' => $linkRegen->getTechniques()]);
            break;
            
        case 'regenerate':
            if ($method !== 'POST') {
                respond(['error' => 'Method not allowed'], 405);
            }
            
            $url = $input['url'] ?? '';
            $technique = $input['technique'] ?? 'add_parameters';
            
            if (empty($url)) {
                respond(['error' => 'URL is required'], 400);
            }
            
            try {
                $regenerated = $linkRegen->regenerate($url, $technique);
                
                // Save to database
                $stmt = $pdo->prepare(
                    "INSERT INTO links (original_url, regenerated_url, technique) VALUES (?, ?, ?)"
                );
                $stmt->execute([$url, $regenerated, $technique]);
                $linkId = $pdo->lastInsertId();
                
                respond([
                    'success' => true,
                    'id' => $linkId,
                    'original' => $url,
                    'regenerated' => $regenerated,
                    'technique' => $technique,
                    'timestamp' => date('Y-m-d H:i:s')
                ]);
            } catch (Exception $e) {
                respond(['error' => $e->getMessage()], 400);
            }
            break;
            
        case 'batch_regenerate':
            if ($method !== 'POST') {
                respond(['error' => 'Method not allowed'], 405);
            }
            
            $url = $input['url'] ?? '';
            $techniques = $input['techniques'] ?? array_keys($linkRegen->getTechniques());
            
            if (empty($url)) {
                respond(['error' => 'URL is required'], 400);
            }
            
            $results = [];
            foreach ($techniques as $technique) {
                try {
                    $regenerated = $linkRegen->regenerate($url, $technique);
                    
                    $stmt = $pdo->prepare(
                        "INSERT INTO links (original_url, regenerated_url, technique) VALUES (?, ?, ?)"
                    );
                    $stmt->execute([$url, $regenerated, $technique]);
                    
                    $results[] = [
                        'technique' => $technique,
                        'original' => $url,
                        'regenerated' => $regenerated
                    ];
                } catch (Exception $e) {
                    $results[] = [
                        'technique' => $technique,
                        'error' => $e->getMessage()
                    ];
                }
            }
            
            respond([
                'success' => true,
                'count' => count($results),
                'results' => $results
            ]);
            break;
            
        case 'links':
            if ($method === 'GET') {
                $limit = intval($_GET['limit'] ?? 100);
                $stmt = $pdo->prepare("SELECT * FROM links ORDER BY created_at DESC LIMIT ?");
                $stmt->execute([$limit]);
                respond(['links' => $stmt->fetchAll()]);
            }
            break;
            
        // Proxy Management Endpoints
        case 'proxies':
            if ($method === 'GET') {
                $limit = intval($_GET['limit'] ?? 1000);
                $status = $_GET['status'] ?? null;
                respond(['proxies' => $proxyManager->getAll($limit, $status)]);
            } elseif ($method === 'POST') {
                $address = $input['address'] ?? '';
                $type = $input['type'] ?? 'http';
                
                if (empty($address)) {
                    respond(['error' => 'Proxy address is required'], 400);
                }
                
                $added = $proxyManager->add($address, $type);
                respond([
                    'success' => $added,
                    'message' => $added ? 'Proxy added' : 'Proxy already exists'
                ]);
            }
            break;
            
        case 'test_proxy':
            if ($method !== 'POST') {
                respond(['error' => 'Method not allowed'], 405);
            }
            
            $proxy = $input['proxy'] ?? '';
            $timeout = intval($input['timeout'] ?? 10);
            
            if (empty($proxy)) {
                respond(['error' => 'Proxy address is required'], 400);
            }
            
            $result = $proxyManager->testProxy($proxy, $timeout);
            
            // Update database
            $proxyManager->updateStatus(
                $proxy,
                $result['status'],
                $result['response_time']
            );
            
            respond($result);
            break;
            
        case 'test_proxies':
            if ($method !== 'POST') {
                respond(['error' => 'Method not allowed'], 405);
            }
            
            $proxies = $input['proxies'] ?? [];
            $timeout = intval($input['timeout'] ?? 10);
            
            $results = [];
            foreach ($proxies as $proxy) {
                $result = $proxyManager->testProxy($proxy, $timeout);
                $proxyManager->updateStatus(
                    $proxy,
                    $result['status'],
                    $result['response_time']
                );
                $results[] = $result;
            }
            
            respond([
                'success' => true,
                'count' => count($results),
                'results' => $results
            ]);
            break;
            
        case 'proxy_stats':
            respond(['stats' => $proxyManager->getStats()]);
            break;
            
        // Statistics
        case 'stats':
            $stats = [];
            
            $stmt = $pdo->query("SELECT COUNT(*) as count FROM users");
            $stats['total_users'] = $stmt->fetch()['count'];
            
            $stmt = $pdo->query("SELECT COUNT(*) as count FROM links");
            $stats['total_links'] = $stmt->fetch()['count'];
            
            $stmt = $pdo->query("SELECT COUNT(*) as count FROM proxies");
            $stats['total_proxies'] = $stmt->fetch()['count'];
            
            $stmt = $pdo->query("SELECT COUNT(*) as count FROM proxies WHERE status = 'active'");
            $stats['active_proxies'] = $stmt->fetch()['count'];
            
            respond(['stats' => $stats]);
            break;
            
        default:
            respond(['error' => 'Unknown action'], 404);
    }
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Internal server error: ' . $e->getMessage()]);
}
