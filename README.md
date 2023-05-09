# 016_anomaly_detection_project
This is a repo for CodeUp DS Anomaly Detection project.

# Anomaly Detection Project

#### by Corey Baughman

##### May 8th, 2023

### Goal: To answer questions for boss

### Overview:

This repository contains a main notebook 'explore.ipynb' that contains the exploration of data necessary to answer the questions about a network log file for curriculum pages for CodeUp, llc for my boss. Start with that notebook to follow the process. Supporting functions are contained in wrangle.py, and explore.py.  You will need an env file with credentials to query the company MySQL server. See 'How to Recreate this Repo' below for more details.

### Instructions to Reproduce Work

download project repo here:
https://github.com/corey-baughman/016_anomaly_detection_project/

create a file called env.py in the directory where you put the files.
The env.py file should contain this entry:

host = 'data.codeup.com'
user = 'your_username'
password = 'your_password'

replace 'your_username' and 'your_password' with your credentials to access the CodeUp mySQL server.
