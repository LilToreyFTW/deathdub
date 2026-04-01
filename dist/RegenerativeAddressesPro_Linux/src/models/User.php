<?php

/**
 * User Model
 * PSR-2 compliant
 */

class User extends Model
{
    /**
     * Table name
     *
     * @var string
     */
    protected $table = 'users';

    /**
     * Find user by username
     *
     * @param string $username Username
     * @return array|bool User data or false on failure
     */
    public function findByUsername($username)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' WHERE username = ?';
        return $this->query($sql, [$username], ['fetch' => 'one']);
    }

    /**
     * Find user by email
     *
     * @param string $email Email address
     * @return array|bool User data or false on failure
     */
    public function findByEmail($email)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' WHERE email = ?';
        return $this->query($sql, [$email], ['fetch' => 'one']);
    }

    /**
     * Create new user
     *
     * @param array $userData User data
     * @return int|bool User ID or false on failure
     */
    public function createUser($userData)
    {
        // Hash password
        $userData['password'] = password_hash($userData['password'], PASSWORD_DEFAULT);
        $userData['created_at'] = date('Y-m-d H:i:s');
        $userData['updated_at'] = date('Y-m-d H:i:s');

        return $this->insert($userData);
    }

    /**
     * Update user
     *
     * @param int $userId User ID
     * @param array $userData User data
     * @return bool Success status
     */
    public function updateUser($userId, $userData)
    {
        // Hash password if provided
        if (isset($userData['password'])) {
            $userData['password'] = password_hash($userData['password'], PASSWORD_DEFAULT);
        }

        $userData['updated_at'] = date('Y-m-d H:i:s');

        return $this->update($userData, 'id = ?', [$userId]);
    }

    /**
     * Verify user credentials
     *
     * @param string $username Username
     * @param string $password Password
     * @return array|bool User data or false on failure
     */
    public function verifyCredentials($username, $password)
    {
        $user = $this->findByUsername($username);

        if ($user && password_verify($password, $user['password'])) {
            // Update last login
            $this->updateLastLogin($user['id']);
            return $user;
        }

        return false;
    }

    /**
     * Update last login time
     *
     * @param int $userId User ID
     * @return bool Success status
     */
    public function updateLastLogin($userId)
    {
        return $this->update(
            ['last_login' => date('Y-m-d H:i:s')],
            'id = ?',
            [$userId]
        );
    }

    /**
     * Get user by ID with additional data
     *
     * @param int $userId User ID
     * @return array|bool User data or false on failure
     */
    public function getUserWithDetails($userId)
    {
        $sql = 'SELECT u.*, 
                       COUNT(DISTINCT l.id) as login_count,
                       MAX(l.created_at) as last_login_session
                FROM ' . $this->table . ' u
                LEFT JOIN user_logins l ON u.id = l.user_id
                WHERE u.id = ?
                GROUP BY u.id';

        return $this->query($sql, [$userId], ['fetch' => 'one']);
    }

    /**
     * Get active users
     *
     * @param int $days Days threshold for activity
     * @return array Active users
     */
    public function getActiveUsers($days = 30)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' 
                WHERE last_login >= DATE_SUB(NOW(), INTERVAL ? DAY)
                ORDER BY last_login DESC';

        return $this->query($sql, [$days]);
    }

    /**
     * Get user statistics
     *
     * @return array User statistics
     */
    public function getUserStatistics()
    {
        $sql = 'SELECT 
                    COUNT(*) as total_users,
                    COUNT(CASE WHEN last_login >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as active_users,
                    COUNT(CASE WHEN last_login >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as weekly_active,
                    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as new_users,
                    COUNT(CASE WHEN status = "active" THEN 1 END) as active_status
                FROM ' . $this->table;

        return $this->query($sql, [], ['fetch' => 'one']);
    }

    /**
     * Search users
     *
     * @param string $query Search query
     * @param int $limit Limit results
     * @return array Search results
     */
    public function searchUsers($query, $limit = 50)
    {
        $sql = 'SELECT id, username, email, created_at, last_login, status 
                FROM ' . $this->table . ' 
                WHERE username LIKE ? OR email LIKE ?
                ORDER BY username
                LIMIT ?';

        $searchTerm = '%' . $query . '%';
        return $this->query($sql, [$searchTerm, $searchTerm, $limit]);
    }

    /**
     * Update user status
     *
     * @param int $userId User ID
     * @param string $status Status
     * @return bool Success status
     */
    public function updateStatus($userId, $status)
    {
        return $this->update(
            ['status' => $status, 'updated_at' => date('Y-m-d H:i:s')],
            'id = ?',
            [$userId]
        );
    }

    /**
     * Delete user
     *
     * @param int $userId User ID
     * @return bool Success status
     */
    public function deleteUser($userId)
    {
        // Soft delete - update status
        return $this->updateStatus($userId, 'deleted');
    }

    /**
     * Check if username exists
     *
     * @param string $username Username
     * @param int $excludeId Exclude user ID
     * @return bool
     */
    public function usernameExists($username, $excludeId = null)
    {
        $sql = 'SELECT COUNT(*) as count FROM ' . $this->table . ' WHERE username = ?';
        $params = [$username];

        if ($excludeId) {
            $sql .= ' AND id != ?';
            $params[] = $excludeId;
        }

        $result = $this->query($sql, $params, ['fetch' => 'one']);
        return $result['count'] > 0;
    }

    /**
     * Check if email exists
     *
     * @param string $email Email address
     * @param int $excludeId Exclude user ID
     * @return bool
     */
    public function emailExists($email, $excludeId = null)
    {
        $sql = 'SELECT COUNT(*) as count FROM ' . $this->table . ' WHERE email = ?';
        $params = [$email];

        if ($excludeId) {
            $sql .= ' AND id != ?';
            $params[] = $excludeId;
        }

        $result = $this->query($sql, $params, ['fetch' => 'one']);
        return $result['count'] > 0;
    }

    /**
     * Get user by API key
     *
     * @param string $apiKey API key
     * @return array|bool User data or false on failure
     */
    public function findByApiKey($apiKey)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' WHERE api_key = ? AND api_key IS NOT NULL';
        return $this->query($sql, [$apiKey], ['fetch' => 'one']);
    }

    /**
     * Generate and set API key for user
     *
     * @param int $userId User ID
     * @return string API key
     */
    public function generateApiKey($userId)
    {
        $apiKey = 'api_' . bin2hex(random_bytes(32));
        
        $this->update(
            ['api_key' => $apiKey, 'updated_at' => date('Y-m-d H:i:s')],
            'id = ?',
            [$userId]
        );

        return $apiKey;
    }

    /**
     * Revoke API key
     *
     * @param int $userId User ID
     * @return bool Success status
     */
    public function revokeApiKey($userId)
    {
        return $this->update(
            ['api_key' => null, 'updated_at' => date('Y-m-d H:i:s')],
            'id = ?',
            [$userId]
        );
    }

    /**
     * Update password
     *
     * @param int $userId User ID
     * @param string $newPassword New password
     * @return bool Success status
     */
    public function updatePassword($userId, $newPassword)
    {
        return $this->update(
            [
                'password' => password_hash($newPassword, PASSWORD_DEFAULT),
                'password_updated_at' => date('Y-m-d H:i:s'),
                'updated_at' => date('Y-m-d H:i:s')
            ],
            'id = ?',
            [$userId]
        );
    }

    /**
     * Get users by role
     *
     * @param string $role User role
     * @return array Users
     */
    public function getUsersByRole($role)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' WHERE role = ? ORDER BY username';
        return $this->query($sql, [$role]);
    }

    /**
     * Update user role
     *
     * @param int $userId User ID
     * @param string $role New role
     * @return bool Success status
     */
    public function updateRole($userId, $role)
    {
        return $this->update(
            ['role' => $role, 'updated_at' => date('Y-m-d H:i:s')],
            'id = ?',
            [$userId]
        );
    }
}
