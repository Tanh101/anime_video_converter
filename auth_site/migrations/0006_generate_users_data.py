from django.db import migrations
from auth_site.models import MyUser
import random
import datetime

def generate_random_users(apps, schema_editor):
    for _ in range(50):
        MyUser.objects.create(
            email=f'user_{random.randint(1, 10000)}@test.com',
            password='randompassword',
            role=random.choice(['user', 'admin']),
            status=random.choice(['active', 'banned']),
            created_at=datetime.datetime.now(),
            update_at=datetime.datetime.now()
        )

class Migration(migrations.Migration):

    dependencies = [
         ('auth_site', '0005_alter_myuser_role'),
    ]

    operations = [
        migrations.RunPython(generate_random_users)
    ]
