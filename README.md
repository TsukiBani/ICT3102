# POTATO@3102.com

## Website for ICT3102 Project

This website is for a module. The aim of the website is to attempt to decrease the workload of teachers within the given
field. The website would allow teachers to perform the following tasks:

<ol>
    <li>Upload Images</li>
    <li>Generate Captions</li>
    <li>Generate Questions and Answers</li>
    <li>Amend Generated QnA</li>
</ol>

## Directory Layout

### db
Folder contains the sql file used to set up the database.

### flask_app > Website > models.py

Contains all SQL-related stuff. Main handler is the ImageSQL class
<br>Tables are Listed Below

<ol>
    <li>Image</li>
    <li>QuestionAnswer</li>
</ol>

### flask_app > Website > views.py

Contains all the Flask routes

### imagedb

### JMeter_Test

Contains the JMeter testing related files and dependencies that may be requried to run the test plan.

### questGen

### questGen_Test

### VQA

## RabbitMQ Implementation

Queues Declared, No exchanges used

<ol>
    <li>CaptionGen</li>
    <li>QuestGen</li>
    <li>AnswerGen</li>
</ol>

## Requirements

All requirements can be found within the requirements.txt.
<br>
RabbitMQ's Docker Image might need to be added to the docker-compose.yml
