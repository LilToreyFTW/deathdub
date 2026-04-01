<?php

/**
 * Model Class for Regenerative Addresses Tool
 * Follows PSR-2 coding standards
 */

class Model
{
    /**
     * Database connection
     *
     * @var PDO|null
     */
    protected $db = null;

    /**
     * Table name
     *
     * @var string
     */
    protected $table = '';

    /**
     * Constructor
     *
     * @param array $config Database configuration
     */
    public function __construct($config = null)
    {
        if ($config !== null) {
            $this->connect($config);
        }
    }

    /**
     * Connect to database
     *
     * @param array $config Database configuration
     * @return bool
     */
    public function connect($config)
    {
        try {
            $dsn = 'mysql:host=' . $config['host'] .
                   ';dbname=' . $config['dbname'] .
                   ';charset=utf8mb4';

            $options = [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
            ];

            $this->db = new PDO($dsn, $config['username'], $config['password'], $options);

            return true;
        } catch (PDOException $e) {
            error_log('Database connection failed: ' . $e->getMessage());
            return false;
        }
    }

    /**
     * Execute query
     *
     * @param string $sql SQL query
     * @param array $params Query parameters
     * @param array $options Query options
     * @return mixed
     */
    public function query($sql, $params = [], $options = [])
    {
        try {
            if ($this->db === null) {
                throw new Exception('Database not connected');
            }

            $stmt = $this->db->prepare($sql);

            // Bind parameters if provided
            if (!empty($params)) {
                foreach ($params as $key => $value) {
                    $param_type = PDO::PARAM_STR;
                    
                    if (is_int($value)) {
                        $param_type = PDO::PARAM_INT;
                    } elseif (is_bool($value)) {
                        $param_type = PDO::PARAM_BOOL;
                    } elseif (is_null($value)) {
                        $param_type = PDO::PARAM_NULL;
                    }

                    if (is_string($key) && $key[0] === ':') {
                        $stmt->bindValue($key, $value, $param_type);
                    } else {
                        $stmt->bindValue(is_int($key) ? $key + 1 : $key, $value, $param_type);
                    }
                }
            }

            $stmt->execute();

            // Handle different fetch modes
            $fetch_mode = $options['fetch'] ?? 'all';
            
            switch ($fetch_mode) {
                case 'all':
                    return $stmt->fetchAll();
                case 'one':
                    return $stmt->fetch();
                case 'column':
                    return $stmt->fetchColumn();
                case 'count':
                    return $stmt->rowCount();
                case 'true':
                    return true;
                default:
                    return $stmt->fetchAll();
            }

        } catch (PDOException $e) {
            error_log('Query failed: ' . $e->getMessage());
            return false;
        }
    }

    /**
     * Insert record
     *
     * @param array $data Data to insert
     * @return int|bool Last insert ID or false on failure
     */
    public function insert($data)
    {
        try {
            if ($this->db === null) {
                throw new Exception('Database not connected');
            }

            if (empty($this->table)) {
                throw new Exception('Table name not set');
            }

            $columns = array_keys($data);
            $placeholders = array_fill(0, count($columns), '?');
            
            $sql = 'INSERT INTO ' . $this->table .
                   ' (' . implode(', ', $columns) . ') ' .
                   'VALUES (' . implode(', ', $placeholders) . ')';

            $stmt = $this->db->prepare($sql);
            $stmt->execute(array_values($data));

            return $this->db->lastInsertId();

        } catch (PDOException $e) {
            error_log('Insert failed: ' . $e->getMessage());
            return false;
        }
    }

    /**
     * Update record
     *
     * @param array $data Data to update
     * @param string $where WHERE clause
     * @param array $where_params WHERE parameters
     * @return bool Success status
     */
    public function update($data, $where, $where_params = [])
    {
        try {
            if ($this->db === null) {
                throw new Exception('Database not connected');
            }

            if (empty($this->table)) {
                throw new Exception('Table name not set');
            }

            $set_clauses = [];
            $params = [];

            foreach ($data as $column => $value) {
                $set_clauses[] = $column . ' = ?';
                $params[] = $value;
            }

            $sql = 'UPDATE ' . $this->table .
                   ' SET ' . implode(', ', $set_clauses) .
                   ' WHERE ' . $where;

            $params = array_merge($params, $where_params);

            $stmt = $this->db->prepare($sql);
            return $stmt->execute($params);

        } catch (PDOException $e) {
            error_log('Update failed: ' . $e->getMessage());
            return false;
        }
    }

    /**
     * Delete record
     *
     * @param string $where WHERE clause
     * @param array $params WHERE parameters
     * @return bool Success status
     */
    public function delete($where, $params = [])
    {
        try {
            if ($this->db === null) {
                throw new Exception('Database not connected');
            }

            if (empty($this->table)) {
                throw new Exception('Table name not set');
            }

            $sql = 'DELETE FROM ' . $this->table . ' WHERE ' . $where;

            $stmt = $this->db->prepare($sql);
            return $stmt->execute($params);

        } catch (PDOException $e) {
            error_log('Delete failed: ' . $e->getMessage());
            return false;
        }
    }

    /**
     * Find record by ID
     *
     * @param int $id Record ID
     * @return array|bool Record data or false on failure
     */
    public function findById($id)
    {
        $sql = 'SELECT * FROM ' . $this->table . ' WHERE id = ?';
        return $this->query($sql, [$id], ['fetch' => 'one']);
    }

    /**
     * Find all records
     *
     * @param string $order ORDER BY clause
     * @param int $limit LIMIT clause
     * @return array|bool Records or false on failure
     */
    public function findAll($order = '', $limit = 0)
    {
        $sql = 'SELECT * FROM ' . $this->table;

        if (!empty($order)) {
            $sql .= ' ORDER BY ' . $order;
        }

        if ($limit > 0) {
            $sql .= ' LIMIT ' . $limit;
        }

        return $this->query($sql);
    }

    /**
     * Count records
     *
     * @param string $where WHERE clause
     * @param array $params WHERE parameters
     * @return int Record count
     */
    public function count($where = '', $params = [])
    {
        $sql = 'SELECT COUNT(*) FROM ' . $this->table;

        if (!empty($where)) {
            $sql .= ' WHERE ' . $where;
        }

        $result = $this->query($sql, $params, ['fetch' => 'column']);
        return (int) $result;
    }

    /**
     * Begin transaction
     *
     * @return bool Success status
     */
    public function beginTransaction()
    {
        if ($this->db === null) {
            return false;
        }

        return $this->db->beginTransaction();
    }

    /**
     * Commit transaction
     *
     * @return bool Success status
     */
    public function commit()
    {
        if ($this->db === null) {
            return false;
        }

        return $this->db->commit();
    }

    /**
     * Rollback transaction
     *
     * @return bool Success status
     */
    public function rollback()
    {
        if ($this->db === null) {
            return false;
        }

        return $this->db->rollBack();
    }

    /**
     * Get last error
     *
     * @return string Last error message
     */
    public function getLastError()
    {
        if ($this->db === null) {
            return 'Database not connected';
        }

        $error_info = $this->db->errorInfo();
        return $error_info[2] ?? 'Unknown error';
    }

    /**
     * Escape string for safe SQL usage
     *
     * @param string $string String to escape
     * @return string Escaped string
     */
    public function escape($string)
    {
        if ($this->db === null) {
            return addslashes($string);
        }

        return $this->db->quote($string);
    }

    /**
     * Close database connection
     */
    public function close()
    {
        $this->db = null;
    }

    /**
     * Destructor
     */
    public function __destruct()
    {
        $this->close();
    }
}
