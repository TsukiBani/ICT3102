CREATE
database 02db;
USE
02db;

CREATE TABLE Image
(
    ID        INTEGER AUTO_INCREMENT,
    name      VARCHAR(255),
    image_url VARCHAR(255),
    caption   VARCHAR(255),
    PRIMARY KEY (ID)
);

CREATE TABLE QuestionAnswer
(
    ID         INTEGER,
    questionID INTEGER AUTO_INCREMENT,
    question   VARCHAR(255),
    answer     VARCHAR(255),
    PRIMARY KEY (ID, questionID),
    FOREIGN KEY (ID) REFERENCES Image (ID)
);