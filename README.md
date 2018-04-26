Testing Method: Currently the only way to test the Server files is to run the Runner.py file. In order to do that, there are some examples ahead, depending on where was installed
the Google Cloud SDK files:

Call in UNIX: python runner.py ~/google/google-cloud-sdk/platform/google_appengine

Call in Bash: ~/AppData/Local/Google/Cloud\ SDK/google-cloud-sdk/platform/google_appengine/runner.py .

Call in Windows (the file runner.py has to be in said path): "%HOME%\AppData\Local\Google\Cloud SDK\google-cloud-sdk\platform\google_appengine\runner.py" .

Google Cloud SDK must be installed

Origin of Runner.py : https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/localtesting/runner.py
