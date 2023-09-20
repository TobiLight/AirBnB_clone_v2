-- Script that prepares a MySQL server for the project
-- Create a DEV Database for the project with name: hbnb_dev_db
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Create a new user with the username: 'hbnb_dev' and password: 'hbnb_dev_pwd' 
-- on the database hbnb_dev_db
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grant the user all privileges
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- Grant User 'hbnb_dev' SELECT privilege on the database 'performance_schema'
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;