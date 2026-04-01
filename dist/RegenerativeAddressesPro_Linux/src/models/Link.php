<?php

/**
 * Link Model
 * PSR-2 compliant
 */

class Link extends Model
{
    /**
     * Table name
     *
     * @var string
     */
    protected $table = 'links';

    /**
     * Create new link
     *
     * @param array $linkData Link data
     * @return int|bool Link ID or false on failure
     */
    public function createLink($linkData)
    {
        $linkData['created_at'] = date('Y-m-d H:i:s');
        $linkData['updated_at'] = date('Y-m-d H:i:s');

        return $this->insert($linkData);
    }

    /**
     * Get link by ID
     *
     * @param int $linkId Link ID
     * @return array|bool Link data or false on failure
     */
    public function getLinkById($linkId)
    {
        $sql = 'SELECT l.*, u.username as created_by_username 
                FROM ' . $this->table . ' l
                LEFT JOIN users u ON l.created_by = u.id
                WHERE l.id = ?';

        return $this->query($sql, [$linkId], ['fetch' => 'one']);
    }

    /**
     * Get links by user
     *
     * @param int $userId User ID
     * @param int $limit Limit results
     * @param int $offset Offset
     * @return array Links
     */
    public function getLinksByUser($userId, $limit = 50, $offset = 0)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' 
                WHERE created_by = ? 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?';

        return $this->query($sql, [$userId, $limit, $offset]);
    }

    /**
     * Get all links with pagination
     *
     * @param int $limit Limit results
     * @param int $offset Offset
     * @param array $filters Filters
     * @return array Links
     */
    public function getAllLinks($limit = 50, $offset = 0, $filters = [])
    {
        $sql = 'SELECT l.*, u.username as created_by_username 
                FROM ' . $this->table . ' l
                LEFT JOIN users u ON l.created_by = u.id
                WHERE 1=1';

        $params = [];

        // Apply filters
        if (!empty($filters['technique'])) {
            $sql .= ' AND l.technique = ?';
            $params[] = $filters['technique'];
        }

        if (!empty($filters['created_by'])) {
            $sql .= ' AND l.created_by = ?';
            $params[] = $filters['created_by'];
        }

        if (!empty($filters['date_from'])) {
            $sql .= ' AND l.created_at >= ?';
            $params[] = $filters['date_from'];
        }

        if (!empty($filters['date_to'])) {
            $sql .= ' AND l.created_at <= ?';
            $params[] = $filters['date_to'];
        }

        $sql .= ' ORDER BY l.created_at DESC LIMIT ? OFFSET ?';
        $params[] = $limit;
        $params[] = $offset;

        return $this->query($sql, $params);
    }

    /**
     * Update link
     *
     * @param int $linkId Link ID
     * @param array $linkData Link data
     * @return bool Success status
     */
    public function updateLink($linkId, $linkData)
    {
        $linkData['updated_at'] = date('Y-m-d H:i:s');

        return $this->update($linkData, 'id = ?', [$linkId]);
    }

    /**
     * Delete link
     *
     * @param int $linkId Link ID
     * @return bool Success status
     */
    public function deleteLink($linkId)
    {
        return $this->delete('id = ?', [$linkId]);
    }

    /**
     * Search links
     *
     * @param string $query Search query
     * @param int $limit Limit results
     * @return array Search results
     */
    public function searchLinks($query, $limit = 50)
    {
        $sql = 'SELECT l.*, u.username as created_by_username 
                FROM ' . $this->table . ' l
                LEFT JOIN users u ON l.created_by = u.id
                WHERE l.original_url LIKE ? OR l.regenerated_url LIKE ?
                ORDER BY l.created_at DESC
                LIMIT ?';

        $searchTerm = '%' . $query . '%';
        return $this->query($sql, [$searchTerm, $searchTerm, $limit]);
    }

    /**
     * Get link statistics
     *
     * @param int $userId User ID (optional)
     * @return array Link statistics
     */
    public function getLinkStatistics($userId = null)
    {
        $sql = 'SELECT 
                    COUNT(*) as total_links,
                    COUNT(DISTINCT technique) as unique_techniques,
                    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as recent_links,
                    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as weekly_links,
                    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 1 DAY) THEN 1 END) as daily_links
                FROM ' . $this->table;

        $params = [];

        if ($userId) {
            $sql .= ' WHERE created_by = ?';
            $params[] = $userId;
        }

        return $this->query($sql, $params, ['fetch' => 'one']);
    }

    /**
     * Get technique statistics
     *
     * @param int $userId User ID (optional)
     * @return array Technique statistics
     */
    public function getTechniqueStatistics($userId = null)
    {
        $sql = 'SELECT technique, COUNT(*) as count, 
                       AVG(CASE WHEN regenerated_url IS NOT NULL THEN 1 ELSE 0 END) * 100 as success_rate
                FROM ' . $this->table;

        $params = [];

        if ($userId) {
            $sql .= ' WHERE created_by = ?';
            $params[] = $userId;
        }

        $sql .= ' GROUP BY technique ORDER BY count DESC';

        return $this->query($sql, $params);
    }

    /**
     * Get popular techniques
     *
     * @param int $limit Limit results
     * @return array Popular techniques
     */
    public function getPopularTechniques($limit = 10)
    {
        $sql = 'SELECT technique, COUNT(*) as usage_count
                FROM ' . $this->table . ' 
                WHERE technique IS NOT NULL
                GROUP BY technique 
                ORDER BY usage_count DESC 
                LIMIT ?';

        return $this->query($sql, [$limit]);
    }

    /**
     * Get recent links
     *
     * @param int $limit Limit results
     * @param int $userId User ID (optional)
     * @return array Recent links
     */
    public function getRecentLinks($limit = 10, $userId = null)
    {
        $sql = 'SELECT l.*, u.username as created_by_username 
                FROM ' . $this->table . ' l
                LEFT JOIN users u ON l.created_by = u.id';

        $params = [];

        if ($userId) {
            $sql .= ' WHERE l.created_by = ?';
            $params[] = $userId;
        }

        $sql .= ' ORDER BY l.created_at DESC LIMIT ?';
        $params[] = $limit;

        return $this->query($sql, $params);
    }

    /**
     * Check if URL exists
     *
     * @param string $originalUrl Original URL
     * @param int $userId User ID (optional)
     * @return bool
     */
    public function urlExists($originalUrl, $userId = null)
    {
        $sql = 'SELECT COUNT(*) as count FROM ' . $this->table . ' WHERE original_url = ?';
        $params = [$originalUrl];

        if ($userId) {
            $sql .= ' AND created_by = ?';
            $params[] = $userId;
        }

        $result = $this->query($sql, $params, ['fetch' => 'one']);
        return $result['count'] > 0;
    }

    /**
     * Get links by technique
     *
     * @param string $technique Technique name
     * @param int $limit Limit results
     * @return array Links
     */
    public function getLinksByTechnique($technique, $limit = 50)
    {
        $sql = 'SELECT l.*, u.username as created_by_username 
                FROM ' . $this->table . ' l
                LEFT JOIN users u ON l.created_by = u.id
                WHERE l.technique = ?
                ORDER BY l.created_at DESC
                LIMIT ?';

        return $this->query($sql, [$technique, $limit]);
    }

    /**
     * Get links by date range
     *
     * @param string $dateFrom Start date
     * @param string $dateTo End date
     * @param int $userId User ID (optional)
     * @return array Links
     */
    public function getLinksByDateRange($dateFrom, $dateTo, $userId = null)
    {
        $sql = 'SELECT l.*, u.username as created_by_username 
                FROM ' . $this->table . ' l
                LEFT JOIN users u ON l.created_by = u.id
                WHERE l.created_at BETWEEN ? AND ?';

        $params = [$dateFrom, $dateTo];

        if ($userId) {
            $sql .= ' AND l.created_by = ?';
            $params[] = $userId;
        }

        $sql .= ' ORDER BY l.created_at DESC';

        return $this->query($sql, $params);
    }

    /**
     * Count links by user
     *
     * @param int $userId User ID
     * @return int Link count
     */
    public function countLinksByUser($userId)
    {
        return $this->count('created_by = ?', [$userId]);
    }

    /**
     * Get total links count
     *
     * @param array $filters Filters
     * @return int Total count
     */
    public function getTotalLinksCount($filters = [])
    {
        $sql = 'SELECT COUNT(*) as count FROM ' . $this->table . ' WHERE 1=1';
        $params = [];

        // Apply filters
        if (!empty($filters['technique'])) {
            $sql .= ' AND technique = ?';
            $params[] = $filters['technique'];
        }

        if (!empty($filters['created_by'])) {
            $sql .= ' AND created_by = ?';
            $params[] = $filters['created_by'];
        }

        if (!empty($filters['date_from'])) {
            $sql .= ' AND created_at >= ?';
            $params[] = $filters['date_from'];
        }

        if (!empty($filters['date_to'])) {
            $sql .= ' AND created_at <= ?';
            $params[] = $filters['date_to'];
        }

        $result = $this->query($sql, $params, ['fetch' => 'one']);
        return $result['count'];
    }
}
