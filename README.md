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
<br>Tables initialised are as follows:

<ol>
    <li>Image</li>
    <li>QuestionAnswer</li>
</ol>

### flask_app

Contains code related to the development of the website.

### imagedb

Storage folder for the user's uploaded image files.

### JMeter_Test

Contains the JMeter testing related files and dependencies that may be requried to run the test plan.

### questGen

Contains all the files required for implementing questGen and dockerising.

Additionally contains the files used for DockerSwarm simulation.

### questGen_Test

Contains the files required for the load testing of RabbitMQ using questGen.

### VQA

Contains all the files required for implementing caption and answer generation.

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
