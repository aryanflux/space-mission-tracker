-- Create and use the database
CREATE DATABASE IF NOT EXISTS space_db;
USE space_db;

-- 1. Users (Parent)
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- 2. Agencies (Parent)
CREATE TABLE Agencies (
    agency_id INT AUTO_INCREMENT PRIMARY KEY,
    agency_name VARCHAR(100) UNIQUE NOT NULL,
    country VARCHAR(100) NOT NULL,
    founded_year INT
);

-- 3. Celestial_Bodies (Parent)
CREATE TABLE Celestial_Bodies (
    body_id INT AUTO_INCREMENT PRIMARY KEY,
    body_name VARCHAR(100) NOT NULL,
    body_type VARCHAR(50),
    distance_million_km DECIMAL(10,2)
);

-- 4. Launch_Sites (Child of Agencies)
CREATE TABLE Launch_Sites (
    site_id INT AUTO_INCREMENT PRIMARY KEY,
    site_name VARCHAR(150) NOT NULL,
    country VARCHAR(100),
    agency_id INT,
    FOREIGN KEY (agency_id) REFERENCES Agencies(agency_id) ON DELETE SET NULL
);

-- 5. Rockets (Child of Agencies)
CREATE TABLE Rockets (
    rocket_id INT AUTO_INCREMENT PRIMARY KEY,
    rocket_name VARCHAR(100) NOT NULL,
    agency_id INT,
    payload_capacity_kg DECIMAL(10,2),
    cost_million DECIMAL(10,2),
    FOREIGN KEY (agency_id) REFERENCES Agencies(agency_id) ON DELETE SET NULL
);

-- 6. Missions (Child of Agencies, Celestial_Bodies)
CREATE TABLE Missions (
    mission_id INT AUTO_INCREMENT PRIMARY KEY,
    mission_name VARCHAR(150) NOT NULL,
    agency_id INT,
    body_id INT,
    mission_type VARCHAR(100),
    status VARCHAR(50),
    budget_million DECIMAL(10,2),
    FOREIGN KEY (agency_id) REFERENCES Agencies(agency_id) ON DELETE SET NULL,
    FOREIGN KEY (body_id) REFERENCES Celestial_Bodies(body_id) ON DELETE SET NULL
);

-- 7. Launches (Child of Missions, Rockets, Launch_Sites)
CREATE TABLE Launches (
    launch_id INT AUTO_INCREMENT PRIMARY KEY,
    mission_id INT,
    rocket_id INT,
    site_id INT,
    launch_date DATE,
    outcome VARCHAR(50),
    FOREIGN KEY (mission_id) REFERENCES Missions(mission_id) ON DELETE CASCADE,
    FOREIGN KEY (rocket_id) REFERENCES Rockets(rocket_id) ON DELETE SET NULL,
    FOREIGN KEY (site_id) REFERENCES Launch_Sites(site_id) ON DELETE SET NULL
);

-- 8. Satellites (Child of Missions)
CREATE TABLE Satellites (
    satellite_id INT AUTO_INCREMENT PRIMARY KEY,
    satellite_name VARCHAR(150) NOT NULL,
    mission_id INT,
    orbit_type VARCHAR(50),
    weight_kg DECIMAL(10,2),
    FOREIGN KEY (mission_id) REFERENCES Missions(mission_id) ON DELETE CASCADE
);

-- 9. Payloads (Child of Launches)
CREATE TABLE Payloads (
    payload_id INT AUTO_INCREMENT PRIMARY KEY,
    launch_id INT,
    payload_name VARCHAR(150) NOT NULL,
    payload_type VARCHAR(100),
    weight_kg DECIMAL(10,2),
    FOREIGN KEY (launch_id) REFERENCES Launches(launch_id) ON DELETE CASCADE
);

-- 10. Astronauts (Child of Agencies)
CREATE TABLE Astronauts (
    astronaut_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    nationality VARCHAR(100),
    dob DATE,
    agency_id INT,
    FOREIGN KEY (agency_id) REFERENCES Agencies(agency_id) ON DELETE SET NULL
);

-- 11. Crew_Assignments (Resolves M:N for Astronauts and Missions)
CREATE TABLE Crew_Assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    mission_id INT,
    astronaut_id INT,
    crew_role VARCHAR(100),
    FOREIGN KEY (mission_id) REFERENCES Missions(mission_id) ON DELETE CASCADE,
    FOREIGN KEY (astronaut_id) REFERENCES Astronauts(astronaut_id) ON DELETE CASCADE
);

-- 12. Mission_Costs (Child of Missions)
CREATE TABLE Mission_Costs (
    cost_id INT AUTO_INCREMENT PRIMARY KEY,
    mission_id INT,
    cost_category VARCHAR(100),
    amount_million DECIMAL(10,2),
    FOREIGN KEY (mission_id) REFERENCES Missions(mission_id) ON DELETE CASCADE
);

-- 13. Mission_Status_Log (Child of Missions)
CREATE TABLE Mission_Status_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    mission_id INT,
    status VARCHAR(50),
    log_date DATE,
    remarks TEXT,
    FOREIGN KEY (mission_id) REFERENCES Missions(mission_id) ON DELETE CASCADE
);