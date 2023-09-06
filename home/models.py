from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

class Video(models.Model):
    Id = models.AutoField(primary_key=True)
    User_Id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos', null=True)
    Original_video_path = models.CharField(max_length=50, blank=True, null=True)
    Converted_video_path = models.CharField(max_length=50, blank=True, null=True)
    Status = models.CharField(max_length=25)
    Created_at = models.DateTimeField(auto_now_add=True)
    Update_at = models.DateTimeField(auto_now=True)
    use_in_migrations = True

class History(models.Model):
    Id = models.AutoField(primary_key=True)
    User_Id = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='histories')
    Action = models.CharField(max_length=25)
    Created_at = models.DateTimeField(auto_now_add=True)
    Update_at = models.DateTimeField(auto_now=True)
    use_in_migrations = True