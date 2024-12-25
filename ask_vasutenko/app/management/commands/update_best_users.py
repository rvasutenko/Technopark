from django.core.management.base import BaseCommand
from app.context_processors import get_and_cache_best_members


class Command(BaseCommand):
    help = 'Update best_users cache.'

    def handle(self, *args, **kwargs):
        get_and_cache_best_members()
        self.stdout.write(self.style.SUCCESS("Best Users cache is renewed"))