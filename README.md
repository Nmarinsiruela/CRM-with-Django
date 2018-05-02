# REST API for a CRM Interface

## Installation

This API works with a Django Framework, PostgreSQL, and Google Cloud Storage, which will require the following dependencies.

In a virtual environment, type the following command, which will install all the necessary dependencies:
* pip install -r requirements.txt

## First use

Note: There is no superuser defined at the start, so it'll be necessary to create a new user by shell command the first time.

After installing Django, in the virtual environment:

* python manage.py makemigrations       - Takes the latest models defined for the DB.
* python manage.py migrate              - Creates the necessary tables and DB from the migrations.
* python manage.py shell < initadmin.py - It'll create a first user with Admin privileges. (User: admin/ Pass: admin)
* python manage.py check                - Verifies that everything it's correct.
* python manage.py runserver            - By defect, the server runs in localhost:8000.

### Tests
* python manage.py test

### Docker

Opening a console in the directory which has both Dockerfile and docker-compose.yml, it'll be possible to launch the whole project following Docker's commands:
* docker-compose up

### Shell
WARNING: Shell's DB is the same that has been launched by runserver command. Therefore any changes typed by Shell will be transmitted to the current server.

* python manage.py shell