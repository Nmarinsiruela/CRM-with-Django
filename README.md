# REST API for a CRM Interface
This API works with [Django Framework](https://docs.djangoproject.com/en/2.0/) as a client, PostgreSQL as the database, and Google Cloud Storage for image-related storing.

In order to change from Developing to Production, just set the DEBUG variable from True to False, in the file settings.py.

## Installation (Developing)
In a virtual environment, type the following command, which will install all the necessary dependencies:
* pip install -r requirements.txt

## First use (Developing)
Note: There is no superuser defined at the start, so it'll be necessary to create a new user by shell command the first time.

After installing Django, in the virtual environment:

* python manage.py makemigrations       - Takes the latest models defined for the DB.
* python manage.py migrate              - Creates the necessary tables and DB from the migrations.
* python manage.py shell < initadmin.py - Creates a first user with Admin privileges. (User: admin/ Pass: admin)
* python manage.py check                - Verifies that everything it's correct.
* python manage.py runserver            - By defect, the server runs in localhost:8000.

## Installation by Docker (Developing / Production)
Opening a console in the directory which has both Dockerfile and docker-compose.yml files, it'll be possible to launch the whole project by simply following Docker's command:
* docker-compose up

### Tests
* python manage.py test

### Shell
WARNING: Shell's DB is the same that has been launched by runserver command. Therefore any changes typed by Shell will be transmitted to the current server.

* python manage.py shell