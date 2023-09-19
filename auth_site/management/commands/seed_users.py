from django.core.management.base import BaseCommand
from django_seed import Seed
from auth_site.models import MyUser  
from django.contrib.auth.hashers import make_password
import datetime
import random

class Command(BaseCommand):
    help = 'Seed the database with fake data'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()
        seeder.add_entity(MyUser, 50, {
            'id': lambda x: seeder.faker.random_number(digits=4),
            'email': lambda x: seeder.faker.email(),
            'password': make_password('123456'),
            'role': lambda x: seeder.faker.random_element(['user', 'admin']),
            'status': lambda x: seeder.faker.random_element(['active', 'banned']),
            'created_at': lambda x: self.generate_created_at(),
            'update_at': lambda x: self.generate_updated_at(),
        })
        seeder.execute()
        text_art = """
     ───────▄▀▀▀▀▀▀▀▀▀▀▄▄
     ────▄▀▀░░░░░░░░░░░░░▀▄
     ──▄▀░░░░░░░░░░░░░░░░░░▀▄
     ──█░░░░░░░░░░░░░░░░░░░░░▀▄
     ─▐▌░░░░░░░░▄▄▄▄▄▄▄░░░░░░░▐▌
     ─█░░░░░░░░░░░▄▄▄▄░░▀▀▀▀▀░░█
     ▐▌░░░░░░░▀▀▀▀░░░░░▀▀▀▀▀░░░▐▌
     █░░░░░░░░░▄▄▀▀▀▀▀░░░░▀▀▀▀▄░█
     █░░░░░░░░░░░░░░░░▀░░░▐░░░░░▐▌
     ▐▌░░░░░░░░░▐▀▀██▄░░░░░░▄▄▄░▐▌
     ─█░░░░░░░░░░░▀▀▀░░░░░░▀▀██░░█
     ─▐▌░░░░▄░░░░░░░░░░░░░▌░░░░░░█
     ──▐▌░░▐░░░░░░░░░░░░░░▀▄░░░░░█
     ───█░░░▌░░░░░░░░▐▀░░░░▄▀░░░▐▌
     ───▐▌░░▀▄░░░░░░░░▀░▀░▀▀░░░▄▀
     ───▐▌░░▐▀▄░░░░░░░░░░░░░░░░█
     ───▐▌░░░▌░▀▄░░░░▀▀▀▀▀▀░░░█
     ───█░░░▀░░░░▀▄░░░░░░░░░░▄▀
     ──▐▌░░░░░░░░░░▀▄░░░░░░▄▀
     ─▄▀░░░▄▀░░░░░░░░▀▀▀▀█▀
     ▀░░░▄▀░░░░░░░░░░▀░░░▀▀▀▀▄▄▄▄▄"""
        self.stdout.write(self.style.SUCCESS(text_art))
        self.stdout.write(self.style.SUCCESS('Successfully  the database with random user data 👌'))
    def generate_created_at(self):
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=3652)
        return self.random_datetime_between(start_date, end_date)

    def generate_updated_at(self):
        created_at = self.generate_created_at()
        end_date = datetime.datetime.now()
        return self.random_datetime_between(created_at, end_date)

    def random_datetime_between(self, start_date, end_date):
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        random_seconds = random.randint(0, delta.seconds)
        return start_date + datetime.timedelta(days=random_days, seconds=random_seconds)