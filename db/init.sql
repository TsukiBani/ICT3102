CREATE  database 02db;
USE     02db;

CREATE TABLE Image
(
    ID        INTEGER AUTO_INCREMENT,
    image_url VARCHAR(255),
    caption   VARCHAR(255),
    PRIMARY KEY (ID)
);

CREATE TABLE QuestionAnswer
(
    ID       INTEGER,
    question VARCHAR(255),
    answer   VARCHAR(255),
    PRIMARY KEY (ID, question),
    FOREIGN KEY (ID) REFERENCES Image (ID)
);