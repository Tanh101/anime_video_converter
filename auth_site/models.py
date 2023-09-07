<<<<<<< HEAD
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

class User(models.Model):
    Id = models.AutoField(primary_key=True)
    Email = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Role = models.BooleanField()
    Status = models.CharField(max_length=25)
    Created_at = models.DateTimeField(auto_now_add=True)
    Update_at = models.DateTimeField(auto_now=True)
    use_in_migrations = True
    
=======
from django.db import models

# Create your models here.
>>>>>>> c72794d (Dashboard basic)
