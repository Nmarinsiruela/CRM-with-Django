This folder has to store the following files:

# secret_keys.txt
Which comprises:
* "Django Secret Key"                   - Secret of the whole project, created by Django.
* "Google Cloud Storage Access Key"     - GSC User identifier, created by Interoperability Setting.
* "Google Cloud Storage Secret"         - GSC Secret, created by Interoperability Setting.
* "Google Cloud Storage Bucket name"    - Name of the GSC bucket.

# database.json
With the configuration of your database, following [Django Structure](https://docs.djangoproject.com/en/2.0/ref/settings/#databases):

{
    "default": {
        "ENGINE": "DJANGO_ENGINE",
		"NAME": "DATABASE_NAME",
        "USER": "USER_NAME",
        "PASSWORD": "PASSWORD_NAME",
        "HOST": "HOST",
        "PORT": "PORT"
    }
}