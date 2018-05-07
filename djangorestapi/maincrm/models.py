from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    photo = models.ImageField(help_text="Optional", upload_to = 'img_folder/', default = 'img_folder/default.png')
    last_modified_by_user = models.CharField(max_length=150, editable=False)
    created_by_user = models.CharField(max_length=150, editable=False)
    

    def __str__(self):
        return self.name