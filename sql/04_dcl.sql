-- 1. CREATE USERS
CREATE USER IF NOT EXISTS 'admin_user'@'localhost' IDENTIFIED BY 'admin123';
CREATE USER IF NOT EXISTS 'control_user'@'localhost' IDENTIFIED BY 'control123';
CREATE USER IF NOT EXISTS 'public_user'@'localhost' IDENTIFIED BY 'guest123';

-- 2. GRANT PRIVILEGES
-- admin_user: ALL privileges
GRANT ALL PRIVILEGES ON space_db.* TO 'admin_user'@'localhost';

-- control_user: SELECT everywhere, INSERT/UPDATE on Launches and Mission_Status_Log
GRANT SELECT ON space_db.* TO 'control_user'@'localhost';
GRANT INSERT, UPDATE ON space_db.Launches TO 'control_user'@'localhost';
GRANT INSERT, UPDATE ON space_db.Mission_Status_Log TO 'control_user'@'localhost';

-- public_user: SELECT only
GRANT SELECT ON space_db.* TO 'public_user'@'localhost';

-- 3. APPLY AND VERIFY
FLUSH PRIVILEGES;

-- Use this command to take the permission screenshot for your PPT:
SHOW GRANTS FOR 'control_user'@'localhost';