CREATE  database 02db;
USE     02db;

CREATE TABLE Image
(
    ID        INTEGER AUTO_INCREMENT,
    image_url VARCHAR(255),
    Caption   VARCHAR(255),
    PRIMARY KEY (ID)
);

CREATE TABLE QuestionAnswer
(
    ID       INTEGER,
    Question VARCHAR(255),
    Answer   VARCHAR(255),
    PRIMARY KEY (ID, Question),
    FOREIGN KEY (ID) REFERENCES Image (ID)
);