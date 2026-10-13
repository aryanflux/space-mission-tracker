USE space_db;

-- 1. Users (Roles for Streamlit Login)
INSERT INTO Users (user_id, username, password, role) VALUES
(1, 'admin_arya', 'admin123', 'admin_user'),
(2, 'mission_control', 'control123', 'control_user'),
(3, 'guest_user', 'guest123', 'public_user');

-- 2. Agencies
INSERT INTO Agencies (agency_id, agency_name, country, founded_year) VALUES
(1, 'ISRO', 'India', 1969),
(2, 'NASA', 'USA', 1958),
(3, 'ESA', 'Europe', 1975),
(4, 'SpaceX', 'USA', 2002),
(5, 'JAXA', 'Japan', 2003);

-- 3. Celestial_Bodies
INSERT INTO Celestial_Bodies (body_id, body_name, body_type, distance_million_km) VALUES
(1, 'Earth', 'Planet', 0.00),
(2, 'Moon', 'Moon', 0.38),
(3, 'Mars', 'Planet', 225.00),
(4, 'Sun', 'Star', 149.60),
(5, 'Jupiter', 'Planet', 778.50);

-- 4. Launch_Sites
INSERT INTO Launch_Sites (site_id, site_name, country, agency_id) VALUES
(1, 'Satish Dhawan Space Centre', 'India', 1),
(2, 'Kennedy Space Center', 'USA', 2),
(3, 'Guiana Space Centre', 'French Guiana', 3),
(4, 'Starbase', 'USA', 4),
(5, 'Tanegashima Space Center', 'Japan', 5);

-- 5. Rockets
INSERT INTO Rockets (rocket_id, rocket_name, agency_id, payload_capacity_kg, cost_million) VALUES
(1, 'LVM3', 1, 10000.00, 46.00),
(2, 'PSLV', 1, 3800.00, 25.00),
(3, 'Space Launch System (SLS)', 2, 95000.00, 2000.00),
(4, 'Ariane 5', 3, 20000.00, 150.00),
(5, 'Falcon 9', 4, 22800.00, 67.00);

-- 6. Missions
INSERT INTO Missions (mission_id, mission_name, agency_id, body_id, mission_type, status, budget_million) VALUES
(1, 'Chandrayaan-3', 1, 2, 'Lunar Lander/Rover', 'Success', 74.00),
(2, 'Aditya-L1', 1, 4, 'Solar Observatory', 'Active', 48.00),
(3, 'Artemis I', 2, 2, 'Lunar Flight Test', 'Success', 4000.00),
(4, 'JUICE', 3, 5, 'Orbiter', 'Active', 1700.00),
(5, 'Mars Perseverance', 2, 3, 'Rover', 'Active', 2700.00);

-- 7. Launches
INSERT INTO Launches (launch_id, mission_id, rocket_id, site_id, launch_date, outcome) VALUES
(1, 1, 1, 1, '2023-07-14', 'Success'),
(2, 2, 2, 1, '2023-09-02', 'Success'),
(3, 3, 3, 2, '2022-11-16', 'Success'),
(4, 4, 4, 3, '2023-04-14', 'Success'),
(5, 5, 5, 2, '2020-07-30', 'Success');

-- 8. Satellites
INSERT INTO Satellites (satellite_id, satellite_name, mission_id, orbit_type, weight_kg) VALUES
(1, 'Pragyan Rover (Chandrayaan-3)', 1, 'Lunar Surface', 26.00),
(2, 'Aditya-L1 Observatory', 2, 'Halo Orbit (L1)', 1475.00),
(3, 'JUICE Spacecraft', 4, 'Jovian Orbit', 4800.00);

-- 9. Payloads
INSERT INTO Payloads (payload_id, launch_id, payload_name, payload_type, weight_kg) VALUES
(1, 1, 'Vikram Lander', 'Lander', 1752.00),
(2, 2, 'VELC Instrument', 'Spectrograph', 190.00),
(3, 3, 'Orion Spacecraft', 'Crew Module (Uncrewed)', 26520.00);

-- 10. Astronauts
INSERT INTO Astronauts (astronaut_id, name, nationality, dob, agency_id) VALUES
(1, 'Rakesh Sharma', 'Indian', '1949-01-13', 1),
(2, 'Neil Armstrong', 'American', '1930-08-05', 2),
(3, 'Thomas Pesquet', 'French', '1978-02-27', 3),
(4, 'Gaganyaan Crew Candidate 1', 'Indian', '1985-01-01', 1);

-- 11. Crew_Assignments
-- Artemis II dummy assignment for context
INSERT INTO Crew_Assignments (assignment_id, mission_id, astronaut_id, crew_role) VALUES
(1, 3, 2, 'Honorary Commander');

-- 12. Mission_Costs
INSERT INTO Mission_Costs (cost_id, mission_id, cost_category, amount_million) VALUES
(1, 1, 'Launch Vehicle', 26.00),
(2, 1, 'Spacecraft & Rover', 48.00),
(3, 3, 'SLS Development', 2000.00);

-- 13. Mission_Status_Log
INSERT INTO Mission_Status_Log (log_id, mission_id, status, log_date, remarks) VALUES
(1, 1, 'Launched', '2023-07-14', 'Successfully inserted into Earth orbit'),
(2, 1, 'Landed', '2023-08-23', 'Historic landing near Lunar South Pole'),
(3, 2, 'Orbit Insertion', '2024-01-06', 'Successfully placed in Halo Orbit around L1'),
(4, 5, 'Landed', '2021-02-18', 'Perseverance rover landed in Jezero Crater');