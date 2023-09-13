from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos', null=True)
    original_video_path = models.CharField(max_length=50, blank=True, null=True) 
    status = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    use_in_migrations = True

class History(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='histories')
    converted_video_path = models.CharField(max_length=50, blank=True, null=True)
    action = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    use_in_migrations = True
