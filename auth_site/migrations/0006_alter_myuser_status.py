# Generated by Django 3.2.6 on 2023-09-18 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_site', '0005_alter_myuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='status',
            field=models.CharField(default='active', max_length=25),
        ),
    ]
