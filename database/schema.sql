DROP TABLE IF EXISTS Agents;

CREATE TABLE Agents (agent_id INT NOT NULL, username VARCHAR, password VARCHAR, PRIMARY KEY (agent_id, username));

DROP TABLE IF EXISTS Hospitals;

CREATE TABLE Hospitals (hospital_id INT NOT NULL, username VARCHAR, password VARCHAR, status INT, PRIMARY KEY (hospital_id, username));

DROP TABLE IF EXISTS Visitors;

CREATE TABLE Visitors (citizen_id INT NOT NULL, username VARCHAR, password VARCHAR, visitor_name VARCHAR, address VARCHAR, contact_type VARCHAR, phone_number VARCHAR, email VARCHAR, device_id VARCHAR, infected BOOL, PRIMARY KEY (citizen_id, username));

DROP TABLE IF EXISTS Places;

CREATE TABLE Places (place_id INT NOT NULL, username VARCHAR, password VARCHAR, place_name VARCHAR, address VARCHAR, qrcode VARCHAR, PRIMARY KEY (place_id, username));

DROP TABLE IF EXISTS VisitorsToPlace;

CREATE TABLE VisitorsToPlace (vtp_id INT NOT NULL, qrcode VARCHAR, device_id VARCHAR, entry_time DATETIME, exit_time DATETIME, PRIMARY KEY (vtp_id, device_id), FOREIGN KEY (qrcode) REFERENCES Places(qrcode), FOREIGN KEY (device_id) REFERENCES Visitors(device_id));