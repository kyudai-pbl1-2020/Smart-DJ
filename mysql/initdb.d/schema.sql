CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    month INT NOT NULL,
    day INT NOT NULL,
    temperature FLOAT NOT NULL,
    pressure FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    PRIMARY KEY (id)
);