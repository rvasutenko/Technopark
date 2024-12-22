from django.core.management.base import BaseCommand
from app.models import Answer, AnswerRate
from tqdm import tqdm
from django.db import transaction
from django.db.models import Count, Q
from django.db.models.signals import pre_save, post_save


class Command(BaseCommand):
    help = 'Synchronise Question.likes_count and Question.answers_count after filling DB.'

    def handle(self, *args, **options):
        pre_save.disconnect(sender=Answer)
        post_save.disconnect(sender=Answer)

        answers = Answer.objects.annotate(
            likes_count=Count('likes', filter=Q(likes__is_dislike=False)),
            dislikes_count=Count('likes', filter=Q(likes__is_dislike=True))
        )

        with transaction.atomic():
            for answer in tqdm(answers):
                answer.rating = answer.likes_count - answer.dislikes_count
                answer.save(update_fields=['rating'])

        self.stdout.write(self.style.SUCCESS('All data is synchronized.'))