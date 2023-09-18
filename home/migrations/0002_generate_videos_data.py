from django.conf import settings
from django.db import migrations, models
import datetime
import random
from home.models import Video
from auth_site.models import MyUser

def generate_random_videos(apps, schema_editor):
    users = MyUser.objects.all()
    for _ in range(100):
        user = random.choice(users)
        Video.objects.create(
            user_id=user,
            original_video_path=f'/path/to/original_video_{random.randint(1, 10000)}.mp4',
            status=random.choice(['completed', 'pending', 'failed']),
            created_at=datetime.datetime.now(),
            update_at=datetime.datetime.now()
        )
        
class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_random_videos)
    ]
    
    