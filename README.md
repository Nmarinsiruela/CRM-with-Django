# REST API for a CRM Interface

## Installation

This API works with a Django Framework, MySQL, and Google Cloud Storage, which will require the following dependencies.

In a virtual environment, type the following commands:
* pip install python
* pip install django
* pip install django-admin
* pip install Pillow            - For Python Image processing
* pip install mysqlclient       - MySQL dependency
* pip install django-storages   - Storage
* pip install boto              - Storage

## First use

After installing Django, in the virtual environment:

* python manage.py makemigrations   - Take the latest models defined for the DB.
* python manage.py migrate          - Create the necessary tables and DB from the migrations.
* python manage.py check            - Verify that everything it's connected.
* python manage.py runserver        - Run the server. By defect, it runs in localhost:8000.

### Tests
* python manage.py tests

### Shell
WARNING: In development, Shell's database is the one that is launched with runserver command. Therefore any changes typed by Shell will be transmitted to the testing server.

* python manage.py shell