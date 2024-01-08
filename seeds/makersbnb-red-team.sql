-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

-- First, we must delete (drop) all our tables
DROP TABLE IF EXISTS account;
DROP SEQUENCE IF EXISTS account_id_seq;


-- Then, we recreate them
CREATE SEQUENCE IF NOT EXISTS account_id_seq;
CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    phone_number VARCHAR(255)
);

-- Finally, we add any records that are needed for the tests to run
INSERT INTO account (username, first_name, last_name, email, password, phone_number)
VALUES
    ('JohnD', 'John', 'Doe', 'johndoe@example.com', 'password123', '07973661188');
