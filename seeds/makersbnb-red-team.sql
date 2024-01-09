-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

-- First, we must delete (drop) all our tables
DROP TABLE IF EXISTS account CASCADE;
DROP SEQUENCE IF EXISTS account_id_seq CASCADE;

DROP TABLE IF EXISTS listing CASCADE;
DROP SEQUENCE IF EXISTS listing_id_seq CASCADE;

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

CREATE SEQUENCE IF NOT EXISTS listing_id_seq;
CREATE TABLE listing (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    description VARCHAR(255),
    price int,
    account_id int,
    constraint fk_account foreign key(account_id) references account(id) on delete cascade
);

-- Finally, we add any records that are needed for the tests to run
INSERT INTO account (username, first_name, last_name, email, password, phone_number)
VALUES
    ('JohnD', 'John', 'Doe', 'johndoe@example.com', 'password123', '07973661188');
INSERT INTO account (username, first_name, last_name, email, password, phone_number)
VALUES
    ('RubyS', 'Ruby', 'Seresin', 'ruby@example.com', 'password1234', '07973661100');
INSERT INTO account (username, first_name, last_name, email, password, phone_number)
VALUES
    ('DanG', 'Dan', 'Gullis', 'dan@example.com', 'password1235', '07973661122');
INSERT INTO account (username, first_name, last_name, email, password, phone_number)
VALUES
    ('KatB', 'Kat', 'Biel', 'kat@example.com', 'password1236', '07973661133');
INSERT INTO account (username, first_name, last_name, email, password, phone_number)
VALUES
    ('AmparoG', 'Amparo', 'Guevara', 'amparo@example.com', 'password1237', '07973661144');



INSERT INTO listing (name, address, description, price, account_id)
VALUES
    ('JohnD house', '145 JohnD lane, London', 'Two bedroom flat, next to the sea', 100, 1);
INSERT INTO listing (name, address, description, price, account_id)
VALUES
    ('RubyS house', '12 Fairytale lane, London', 'Ten bedroom mansion', 300, 2);
INSERT INTO listing (name, address, description, price, account_id)
VALUES
    ('RubyS cottage', '34 Cottage lane, Village', 'Beautiful cottage in the woods', 150, 2);
INSERT INTO listing (name, address, description, price, account_id)
VALUES
    ('DanG', '22 High Street, London', 'Modern loft', 350, 3);
INSERT INTO listing (name, address, description, price, account_id)
VALUES
    ('KatB', '12 Nowhere lane, Middletown', 'Quiet house in the wilderness', 350, 3);