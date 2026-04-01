<?php

/**
 * Proxy Model
 * PSR-2 compliant
 */

class Proxy extends Model
{
    /**
     * Table name
     *
     * @var string
     */
    protected $table = 'proxies';

    /**
     * Add new proxy
     *
     * @param array $proxyData Proxy data
     * @return int|bool Proxy ID or false on failure
     */
    public function addProxy($proxyData)
    {
        $proxyData['created_at'] = date('Y-m-d H:i:s');
        $proxyData['updated_at'] = date('Y-m-d H:i:s');

        return $this->insert($proxyData);
    }

    /**
     * Get proxy by ID
     *
     * @param int $proxyId Proxy ID
     * @return array|bool Proxy data or false on failure
     */
    public function getProxyById($proxyId)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' WHERE id = ?';
        return $this->query($sql, [$proxyId], ['fetch' => 'one']);
    }

    /**
     * Get proxy by address
     *
     * @param string $address Proxy address (host:port)
     * @return array|bool Proxy data or false on failure
     */
    public function getProxyByAddress($address)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' WHERE address = ?';
        return $this->query($sql, [$address], ['fetch' => 'one']);
    }

    /**
     * Get all proxies with pagination
     *
     * @param int $limit Limit results
     * @param int $offset Offset
     * @param array $filters Filters
     * @return array Proxies
     */
    public function getAllProxies($limit = 50, $offset = 0, $filters = [])
    {
        $sql = 'SELECT * FROM ' . $this->table . ' WHERE 1=1';
        $params = [];

        // Apply filters
        if (!empty($filters['type'])) {
            $sql .= ' AND type = ?';
            $params[] = $filters['type'];
        }

        if (!empty($filters['status'])) {
            $sql .= ' AND status = ?';
            $params[] = $filters['status'];
        }

        if (!empty($filters['country'])) {
            $sql .= ' AND country = ?';
            $params[] = $filters['country'];
        }

        $sql .= ' ORDER BY created_at DESC LIMIT ? OFFSET ?';
        $params[] = $limit;
        $params[] = $offset;

        return $this->query($sql, $params);
    }

    /**
     * Get active proxies
     *
     * @param string $type Proxy type (optional)
     * @param int $limit Limit results
     * @return array Active proxies
     */
    public function getActiveProxies($type = null, $limit = 100)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' WHERE status = "active"';
        $params = [];

        if ($type) {
            $sql .= ' AND type = ?';
            $params[] = $type;
        }

        $sql .= ' ORDER BY last_checked DESC LIMIT ?';
        $params[] = $limit;

        return $this->query($sql, $params);
    }

    /**
     * Get random proxy
     *
     * @param string $type Proxy type (optional)
     * @param string $country Country code (optional)
     * @return array|bool Proxy data or false on failure
     */
    public function getRandomProxy($type = null, $country = null)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' WHERE status = "active"';
        $params = [];

        if ($type) {
            $sql .= ' AND type = ?';
            $params[] = $type;
        }

        if ($country) {
            $sql .= ' AND country = ?';
            $params[] = $country;
        }

        $sql .= ' ORDER BY RAND() LIMIT 1';

        return $this->query($sql, $params, ['fetch' => 'one']);
    }

    /**
     * Update proxy status
     *
     * @param int $proxyId Proxy ID
     * @param string $status New status
     * @param array $additionalData Additional data to update
     * @return bool Success status
     */
    public function updateProxyStatus($proxyId, $status, $additionalData = [])
    {
        $data = array_merge([
            'status' => $status,
            'last_checked' => date('Y-m-d H:i:s'),
            'updated_at' => date('Y-m-d H:i:s')
        ], $additionalData);

        return $this->update($data, 'id = ?', [$proxyId]);
    }

    /**
     * Update proxy check results
     *
     * @param int $proxyId Proxy ID
     * @param bool $isWorking Is proxy working
     * @param int $responseTime Response time in milliseconds
     * @param string $country Country code
     * @return bool Success status
     */
    public function updateProxyCheck($proxyId, $isWorking, $responseTime = null, $country = null)
    {
        $data = [
            'last_checked' => date('Y-m-d H:i:s'),
            'updated_at' => date('Y-m-d H:i:s'),
            'status' => $isWorking ? 'active' : 'inactive'
        ];

        if ($responseTime !== null) {
            $data['response_time'] = $responseTime;
        }

        if ($country) {
            $data['country'] = $country;
        }

        if ($isWorking) {
            $data['consecutive_failures'] = 0;
            $data['last_success'] = date('Y-m-d H:i:s');
        } else {
            $data['consecutive_failures'] = 'COALESCE(consecutive_failures, 0) + 1';
        }

        return $this->update($data, 'id = ?', [$proxyId]);
    }

    /**
     * Delete proxy
     *
     * @param int $proxyId Proxy ID
     * @return bool Success status
     */
    public function deleteProxy($proxyId)
    {
        return $this->delete('id = ?', [$proxyId]);
    }

    /**
     * Search proxies
     *
     * @param string $query Search query
     * @param int $limit Limit results
     * @return array Search results
     */
    public function searchProxies($query, $limit = 50)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' 
                WHERE address LIKE ? OR country LIKE ? OR type LIKE ?
                ORDER BY created_at DESC
                LIMIT ?';

        $searchTerm = '%' . $query . '%';
        return $this->query($sql, [$searchTerm, $searchTerm, $searchTerm, $limit]);
    }

    /**
     * Get proxy statistics
     *
     * @return array Proxy statistics
     */
    public function getProxyStatistics()
    {
        $sql = 'SELECT 
                    COUNT(*) as total_proxies,
                    COUNT(CASE WHEN status = "active" THEN 1 END) as active_proxies,
                    COUNT(CASE WHEN status = "inactive" THEN 1 END) as inactive_proxies,
                    COUNT(CASE WHEN status = "checking" THEN 1 END) as checking_proxies,
                    COUNT(DISTINCT type) as unique_types,
                    COUNT(DISTINCT country) as unique_countries,
                    AVG(response_time) as avg_response_time,
                    COUNT(CASE WHEN last_checked >= DATE_SUB(NOW(), INTERVAL 1 HOUR) THEN 1 END) as recently_checked
                FROM ' . $this->table;

        return $this->query($sql, [], ['fetch' => 'one']);
    }

    /**
     * Get proxy statistics by type
     *
     * @return array Type statistics
     */
    public function getProxyStatisticsByType()
    {
        $sql = 'SELECT type, 
                       COUNT(*) as total,
                       COUNT(CASE WHEN status = "active" THEN 1 END) as active,
                       AVG(response_time) as avg_response_time
                FROM ' . $this->table . ' 
                GROUP BY type 
                ORDER BY active DESC';

        return $this->query($sql);
    }

    /**
     * Get proxy statistics by country
     *
     * @param int $limit Limit results
     * @return array Country statistics
     */
    public function getProxyStatisticsByCountry($limit = 20)
    {
        $sql = 'SELECT country, 
                       COUNT(*) as total,
                       COUNT(CASE WHEN status = "active" THEN 1 END) as active,
                       AVG(response_time) as avg_response_time
                FROM ' . $this->table . ' 
                WHERE country IS NOT NULL AND country != ""
                GROUP BY country 
                ORDER BY active DESC
                LIMIT ?';

        return $this->query($sql, [$limit]);
    }

    /**
     * Get proxies that need checking
     *
     * @param int $interval Check interval in minutes
     * @param int $limit Limit results
     * @return array Proxies to check
     */
    public function getProxiesNeedingCheck($interval = 60, $limit = 100)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' 
                WHERE status = "active" 
                AND (last_checked IS NULL OR last_checked <= DATE_SUB(NOW(), INTERVAL ? MINUTE))
                ORDER BY last_checked ASC
                LIMIT ?';

        return $this->query($sql, [$interval, $limit]);
    }

    /**
     * Get failed proxies
     *
     * @param int $failureThreshold Failure threshold
     * @param int $limit Limit results
     * @return array Failed proxies
     */
    public function getFailedProxies($failureThreshold = 3, $limit = 50)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' 
                WHERE consecutive_failures >= ?
                ORDER BY consecutive_failures DESC, last_checked DESC
                LIMIT ?';

        return $this->query($sql, [$failureThreshold, $limit]);
    }

    /**
     * Import proxies from array
     *
     * @param array $proxies Proxy data array
     * @param string $type Proxy type
     * @return array Import results
     */
    public function importProxies($proxies, $type = 'http')
    {
        $imported = 0;
        $duplicates = 0;
        $errors = 0;

        foreach ($proxies as $proxyAddress) {
            $proxyAddress = trim($proxyAddress);
            if (empty($proxyAddress)) {
                continue;
            }

            // Check if proxy already exists
            if ($this->getProxyByAddress($proxyAddress)) {
                $duplicates++;
                continue;
            }

            // Parse proxy address
            $parts = explode(':', $proxyAddress);
            if (count($parts) < 2) {
                $errors++;
                continue;
            }

            $host = $parts[0];
            $port = $parts[1];

            // Validate port
            if (!is_numeric($port) || $port < 1 || $port > 65535) {
                $errors++;
                continue;
            }

            $proxyData = [
                'address' => $proxyAddress,
                'host' => $host,
                'port' => $port,
                'type' => $type,
                'status' => 'inactive',
                'consecutive_failures' => 0
            ];

            if ($this->addProxy($proxyData)) {
                $imported++;
            } else {
                $errors++;
            }
        }

        return [
            'imported' => $imported,
            'duplicates' => $duplicates,
            'errors' => $errors,
            'total' => count($proxies)
        ];
    }

    /**
     * Export proxies to array
     *
     * @param array $filters Filters
     * @return array Proxies
     */
    public function exportProxies($filters = [])
    {
        $sql = 'SELECT address FROM ' . $this->table . ' WHERE 1=1';
        $params = [];

        // Apply filters
        if (!empty($filters['type'])) {
            $sql .= ' AND type = ?';
            $params[] = $filters['type'];
        }

        if (!empty($filters['status'])) {
            $sql .= ' AND status = ?';
            $params[] = $filters['status'];
        }

        if (!empty($filters['country'])) {
            $sql .= ' AND country = ?';
            $params[] = $filters['country'];
        }

        $sql .= ' ORDER BY address';

        $results = $this->query($sql, $params);
        return array_column($results, 'address');
    }

    /**
     * Count total proxies
     *
     * @param array $filters Filters
     * @return int Total count
     */
    public function getTotalProxiesCount($filters = [])
    {
        $sql = 'SELECT COUNT(*) as count FROM ' . $this->table . ' WHERE 1=1';
        $params = [];

        // Apply filters
        if (!empty($filters['type'])) {
            $sql .= ' AND type = ?';
            $params[] = $filters['type'];
        }

        if (!empty($filters['status'])) {
            $sql .= ' AND status = ?';
            $params[] = $filters['status'];
        }

        if (!empty($filters['country'])) {
            $sql .= ' AND country = ?';
            $params[] = $filters['country'];
        }

        $result = $this->query($sql, $params, ['fetch' => 'one']);
        return $result['count'];
    }
}
