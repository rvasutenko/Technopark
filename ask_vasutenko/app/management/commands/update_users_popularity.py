from django.core.management.base import BaseCommand
from app.models import Profile
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Update users popularity.'

    def handle(self, *args, **options):
        for profile in tqdm(Profile.objects.all()):
            profile.update_weekly_popularity()