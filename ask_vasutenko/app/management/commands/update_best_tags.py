from django.core.management.base import BaseCommand
from app.context_processors import get_and_cache_best_members, get_and_cache_best_tags


class Command(BaseCommand):
    help = 'Update best_tags cache.'

    def handle(self, *args, **kwargs):
        get_and_cache_best_tags()
        self.stdout.write(self.style.SUCCESS("Best Tags cache is renewed"))