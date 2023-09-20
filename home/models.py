from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from auth_site.models import MyUser

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_video', null=True)
    name = models.CharField(max_length=100)
    original_video_path = models.CharField(max_length=50, blank=True, null=True)
    converted_video_path = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    use_in_migrations = True
