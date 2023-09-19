from django.core.management.base import BaseCommand
from django_seed import Seed
from home.models import Video, MyUser  # Replace with your actual models
import datetime
import random

class Command(BaseCommand):
    help = 'Seed the database with fake video data'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()
        users = MyUser.objects.all()

        # Define the seed data for Video model
        seeder.add_entity(Video, 100, {
            'id': lambda x: seeder.faker.random_number(digits=4),
            'name': lambda x: seeder.faker.name(),
            'user_id': lambda x: random.choice(users).id,
            'original_video_path': lambda x: f'path/to/original_video_{seeder.faker.random_int(min=1, max=10000)}.mp4',
            'converted_video_path': lambda x: f'path/to/converted_video_{seeder.faker.random_int(min=1, max=10000)}.mp4',
            'status': lambda x: seeder.faker.random_element(['completed', 'pending', 'failed']),
            'created_at': lambda x: self.generate_created_at(),
            'update_at': lambda x: self.generate_updated_at(),
        })

        seeder.execute()
        text_art = """
        ───────────▄▄▄▄▄▄▄▄▄───────────
        ────────▄█████████████▄────────
        █████──█████████████████──█████ 
        ▐████▌─▀███▄───────▄███▀─▐████▌
        ─█████▄──▀███▄───▄███▀──▄█████─
        ─▐██▀███▄──▀███▄███▀──▄███▀██▌─
        ──███▄▀███▄──▀███▀──▄███▀▄███──
        ──▐█▄▀█▄▀███─▄─▀─▄─███▀▄█▀▄█▌──
        ───███▄▀█▄██─██▄██─██▄█▀▄███───
        ────▀███▄▀██─█████─██▀▄███▀────
        ───█▄─▀█████─█████─█████▀─▄█───
        ───███────────███────────███───
        ───███▄────▄█─███─█▄────▄███───
        ───█████─▄███─███─███▄─█████───
        ───█████─████─███─████─█████───
        ───█████─████─███─████─█████───
        ───█████─████─███─████─█████───
        ───█████─████▄▄▄▄▄████─█████───
        ────▀███─█████████████─███▀────
        ──────▀█─███─▄▄▄▄▄─███─█▀──────
        ─────────▀█▌▐█████▌▐█▀─────────
        ────────────███████────────────

        """
        self.stdout.write(self.style.SUCCESS(text_art))
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with random video data 👌'))

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
