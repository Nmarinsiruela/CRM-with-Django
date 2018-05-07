#!/usr/bin/env python
from django.contrib.auth.models import User

if len(User.objects.all()) <1:
	user=User.objects.create_user('admin', password='admin')
	user.is_staff=True
	user.save()