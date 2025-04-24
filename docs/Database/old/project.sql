CREATE DATABASE Project;

USE Project;


CREATE TABLE Movie (
    title VARCHAR(255) NOT NULL,
    releaseDate DATE,
    language VARCHAR(50),
    runtime INT,
    productionCompany VARCHAR(255),
    PRIMARY KEY (title, releaseDate)
);

CREATE TABLE Person (
    fullName VARCHAR(255) NOT NULL,
    DOB DATE NOT NULL,
    COB VARCHAR(100) NOT NULL,
    DOD DATE NULL,
    PRIMARY KEY (fullName, DOB)
);

CREATE TABLE User (
    email VARCHAR(225) NOT NULL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    gender ENUM('Male', 'Female') NUll,
    birthdate DATE NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE Award (
    category VARCHAR(255) NOT NULL,
    iteration INT NOT NULL,
    year INT NOT NULL,
    PRIMARY KEY (category, iteration)
);

CREATE TABLE MovieRole (
    title VARCHAR(255) NOT NULL,
    releaseDate DATE NOT NULL,
    fullName VARCHAR(255) NOT NULL,
    DOB DATE NOT NULL,
    role ENUM('Actor', 'Director', 'Producer') NOT NULL,
    PRIMARY KEY (title, releaseDate, fullName, DOB, role),
    FOREIGN KEY (title, releaseDate) REFERENCES Movie(title, releaseDate) ON DELETE CASCADE,
    FOREIGN KEY (fullName, DOB) REFERENCES Person(fullName, DOB) ON DELETE CASCADE
);

CREATE TABLE MovieNomination (
    title VARCHAR(255) NOT NULL,
    releaseDate DATE NOT NULL,
    category VARCHAR(255) NOT NULL,
    iteration INT NOT NULL,
    won BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (title, releaseDate, category, iteration),
    FOREIGN KEY (title, releaseDate) REFERENCES Movie(title, releaseDate) ON DELETE CASCADE,
    FOREIGN KEY (category, iteration) REFERENCES Award(category, iteration) ON DELETE CASCADE
);

CREATE TABLE RoleNomination (
	nominationID INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    releaseDate DATE NOT NULL,
    fullName VARCHAR(255) NOT NULL,
    DOB DATE NOT NULL,
    role ENUM('Actor', 'Director', 'Producer') NOT NULL,
    category VARCHAR(255) NOT NULL,
    iteration INT NOT NULL,
    won BOOLEAN NOT NULL,
    FOREIGN KEY (title, releaseDate) REFERENCES Movie(title, releaseDate) ON DELETE CASCADE,
    FOREIGN KEY (fullName, DOB) REFERENCES Person(fullName, DOB) ON DELETE CASCADE,
    FOREIGN KEY (title, releaseDate, fullName, DOB, role) REFERENCES MovieRole(title, releaseDate, fullName, DOB, role) ON DELETE CASCADE,
    FOREIGN KEY (category, iteration) REFERENCES Award(category, iteration) ON DELETE CASCADE
);

CREATE TABLE UserMovieNomination (
    email VARCHAR(225)  NOT NULL,
    title VARCHAR(255) NOT NULL,
    releaseDate DATE NOT NULL,
    category VARCHAR(255) NOT NULL,
    iteration INT NOT NULL,
    PRIMARY KEY (email, title, releaseDate, category, iteration),
    FOREIGN KEY (email) REFERENCES User(email) ON DELETE CASCADE,
    FOREIGN KEY (title, releaseDate) REFERENCES Movie(title, releaseDate) ON DELETE CASCADE,
    FOREIGN KEY (category, iteration) REFERENCES Award(category, iteration) ON DELETE CASCADE
);

CREATE TABLE UserRoleNomination (
	userNominationID INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(225) NOT NULL,
    title VARCHAR(255) NOT NULL,
    releaseDate DATE NOT NULL,
    fullName VARCHAR(255) NOT NULL,
    DOB DATE NOT NULL,
    role ENUM('Actor', 'Director', 'Producer') NOT NULL,
    category VARCHAR(255) NOT NULL,
    iteration INT NOT NULL,
    FOREIGN KEY (email) REFERENCES User(email) ON DELETE CASCADE,
    FOREIGN KEY (title, releaseDate) REFERENCES Movie(title, releaseDate) ON DELETE CASCADE,
    FOREIGN KEY (fullName, DOB) REFERENCES Person(fullName, DOB) ON DELETE CASCADE,
    FOREIGN KEY (title, releaseDate, fullName, DOB, role) REFERENCES MovieRole(title, releaseDate, fullName, DOB, role) ON DELETE CASCADE,
    FOREIGN KEY (category, iteration) REFERENCES Award(category, iteration) ON DELETE CASCADE
);
