USE space_db;

-- 1. SELECT with WHERE, LIKE, ORDER BY, and LIMIT
SELECT mission_name, status, budget_million 
FROM Missions 
WHERE mission_name LIKE '%yaan%' 
ORDER BY budget_million DESC 
LIMIT 5;

-- 2. SELECT with BETWEEN
SELECT rocket_name, payload_capacity_kg, cost_million 
FROM Rockets 
WHERE cost_million BETWEEN 20.00 AND 100.00;

-- 3. Aggregation (COUNT, SUM, AVG, MAX, MIN)
SELECT 
    COUNT(mission_id) AS total_missions, 
    SUM(budget_million) AS total_budget, 
    AVG(budget_million) AS avg_budget, 
    MAX(budget_million) AS highest_budget, 
    MIN(budget_million) AS lowest_budget 
FROM Missions;

-- 4. GROUP BY and HAVING
SELECT a.agency_name, COUNT(m.mission_id) AS mission_count 
FROM Missions m
INNER JOIN Agencies a ON m.agency_id = a.agency_id
GROUP BY a.agency_name 
HAVING mission_count >= 1;

-- 5. INNER JOIN (Missions and Agencies)
SELECT m.mission_name, a.agency_name, m.mission_type, m.status 
FROM Missions m 
INNER JOIN Agencies a ON m.agency_id = a.agency_id;

-- 6. LEFT JOIN (Rockets and Launches to see unused rockets)
SELECT r.rocket_name, l.launch_date, l.outcome 
FROM Rockets r 
LEFT JOIN Launches l ON r.rocket_id = l.rocket_id;