# Generated by Django 4.2.5 on 2023-09-13 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('role', models.CharField(default='user', max_length=10)),
                ('status', models.CharField(default='active', max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
