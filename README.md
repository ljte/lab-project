[![Build Status](https://travis-ci.com/ljte/lab-project.svg?branch=master)](https://travis-ci.com/ljte/lab-project) [![Coverage Status](https://coveralls.io/repos/github/ljte/lab-project/badge.svg?branch=master)]

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
-  Poetry

 ## Installation
 if you have docker docker-compose and make installed just run
 ```
 docker-compose ud -d or make run
 ```
 
 migrations
```
docker-compose run --rm app python manage.py makemigrations

docker-compose run --rm app python manage.py migrate
```
or simply `make migrate` does the same thing don't forget to collectstatic
 
 ### TODO
 * deploy to heroku
