REST API for a CRM Interface

# Installation

This API works with a Django Framework, which will require Python3, Pip, Pillow and django-admin.

In a virtual environment, type the following commands:
pip install python
pip install django --> Basic Django
pip install django-admin --> Admin control
pip install Pillow --> Image processing

# Use

python manage.py runserver

# Tests

python manage.py tests

# Shell
WARNING: In development, Shell's database is the one that is launched with runserver command. Therefore any changes typed by Shell will be transmitted to the testing server.

python manage.py shell