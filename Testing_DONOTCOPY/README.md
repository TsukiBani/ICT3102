# POTATO@3102.com

## Test Data and Scripts

This directory contains the datasets and items used for the testing of the docker container

### Caption Generation Testing Guide

X) Run **common_testing_script.py** and use the '_CaptionGen_' queue

### Question Generation Testing Guide

#### Prerequisites:

1) Ensure all containers are running
2) Import **amazon_cells_labelled.csv** into the database, '_db_'
    1) Import according to names: Eg. caption csv into caption column
3) Run **common_testing_script.py** and use the '_QuestGen_' queue

#### Limitations:

- **RANGE FOR RANDOMISATION** Must be 1000 or lesser

### Answer Generation Testing Guide

X) Run **common_testing_script.py** and use the '_AnswerGen_' queue