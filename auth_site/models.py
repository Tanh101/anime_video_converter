from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

class MyUser(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, default='user')
    status = models.CharField(max_length=25, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    use_in_migrations = True
