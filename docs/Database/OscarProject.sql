-- Create database
CREATE DATABASE oscarProject;

-- Select the database
USE oscarProject;

-- movie table
CREATE TABLE movie (
    title VARCHAR(100) NOT NULL,
    release_date DATE NOT NULL,
    language VARCHAR(50),
    run_time INT,
    production_company VARCHAR(255),
    PRIMARY KEY (title, release_date)
);

-- person table
CREATE TABLE person (
    name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    country VARCHAR(100),
    dod DATE,
    PRIMARY KEY (name, dob)
);

-- user table
CREATE TABLE user (
    username VARCHAR(50) NOT NULL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    gender VARCHAR(10),
    birthdate DATE,
    country VARCHAR(100)
);

-- award table
CREATE TABLE award (
    category VARCHAR(100) NOT NULL,
    iteration INT NOT NULL,
    PRIMARY KEY (category, iteration)
);

-- nomination table
CREATE TABLE nomination (
    role_nomination_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_title VARCHAR(255),
    movie_release_date DATE,
    person_name VARCHAR(255),
    person_dob DATE,
    role VARCHAR(100),
    category VARCHAR(100),
    iteration INT,
    won BOOLEAN,
    FOREIGN KEY (movie_title, movie_release_date) 
        REFERENCES movie(title, release_date) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (person_name, person_dob) 
        REFERENCES person(name, dob) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (category, iteration) 
        REFERENCES award(category, iteration) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- user_nomination table
CREATE TABLE user_nomination (
    user_role_nomination INT AUTO_INCREMENT PRIMARY KEY, 
    username VARCHAR(50),
    movie_title VARCHAR(255),
    movie_release_date DATE,
    person_name VARCHAR(255),
    person_dob DATE,
    role VARCHAR(100),
    category VARCHAR(100),
    iteration INT,
    FOREIGN KEY (username) 
        REFERENCES user(username) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (movie_title, movie_release_date) 
        REFERENCES movie(title, release_date) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (person_name, person_dob) 
        REFERENCES person(name, dob) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (category, iteration) 
        REFERENCES award(category, iteration) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);
