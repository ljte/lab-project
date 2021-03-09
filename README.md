[![Build Status](https://travis-ci.com/ljte/lab-project.svg?branch=master)](https://travis-ci.com/ljte/lab-project) [![Coverage Status](https://coveralls.io/repos/github/ljte/lab-project/badge.svg?branch=master)](https://coveralls.io/github/ljte/lab-project?branch=master)

## Table of Contents
* [General Info](#general-info)
* [Application](#application)
* [Technologies](#technologies)
* [Installation](#installation)

## General info
This project is going to use modern web technologies to work with Department and Employee databases.

## Application
The user of the app will be able to:
-  See the list of departments;
-  See the list of employees;
-  Add, remove and edit departments;
-  Add, remove and edit employees;

## Technologies
-  Python 3.8
-  Django 3.1.7
-  Docker 20.10.5   
-  Postgresql latest docker image

 ## Installation
 if you have docker and docker-compose installed just run
 > docker-compose ud -d or make run
 
 migrations
 > docker-compose run --rm app python manage.py makemigrations
 >
 > docker-compose run --rm app python manage.py migrate
 > 
 or simply `make migrate` does the same thing
 
 ### TODO
 * add filters
 * configure nginx
 * add more tests
 * split api and backend into services
 * add container healthchecks
 * deploy to heroku
 * Optinal(think about adding redis)
