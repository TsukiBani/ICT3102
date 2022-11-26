# Test Data and Scripts
This directory contains the datasets and items used for the testing of the QuestGen docker container

# Important Notice
The files used to simulate the DockerSwarm scenario are found within the **questGen** folder.
<br>Kindly refer to the _README.md_ within the **questGen** folder for more information. 

## Question Generation Testing Guide

### Prerequisites:

1) Ensure all containers are running
2) Import **amazon_cells_labelled.csv** into the database, '_db_'
    1) Import according to names: Eg. caption csv into caption column
3) Run **common_testing_script.py** and use the '_QuestGen_' queue

### Limitations:

- **QUEUE ITEMS COUNT** Must be 1000 or lesser

## Getting Results
1) Enter the '_questgen_'container and execute the **collation.py**
   1) Command Example:
      1) python collation.py

## How to Interpret results
It will return the following:
- Total Number of Captions Evaluated
- Total Number of Questions Generated
- Average Number of Questions Generated based on Characters of Caption