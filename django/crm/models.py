from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=30, help_text="Enter name")
    surname = models.CharField(max_length=40, help_text="Enter surname")
    photo = models.ImageField(help_text="Enter an optional image", blank=True, upload_to = 'img_folder/', default = 'img_folder/default.png')
    referenced_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name