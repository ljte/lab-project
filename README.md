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
-  Flask 1.1.2
-  Flask-SQLAlchemy 2.4.4
-  Flask-Migrate 2.5.3
-  Postgresql 12.4


## Installation
install virtualenv
```
pip install virtualenv
```
create virtual environment
```
virtualenv venv
```
activate venv
on Linux or Mac:
```
source venv/bin/activate
```
on Windows:
```
venv/Scripts/activate.bat
```
install requirements
```
pip install -r requirements.txt
```
or
```
python setup.py install
```
to create database you need to run the following commands
```
python manage.py db migrate
python manage.py db upgrade
```
this will create two tables Department and Employee in your database
and the commands above are used to make migrations and also you can use
```
python manage.py db downgrade
``` 
to cancel the upgrade

## Additional info
After installing the app you can run a gunicorn or development server
```
gunicorn "run:run()" or python run.py
```
then open your browser and go to the localhost url to see the app,
you can play around with it, add, change, delete some stuff.

You can find working version on *https://mylabproject.herokuapp.com/*