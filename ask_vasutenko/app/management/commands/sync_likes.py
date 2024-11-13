from django.core.management.base import BaseCommand
from app.models import Tag, Question, Answer, QuestionLike, AnswerLike, Profile
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Synchronise Question.likes_count and Question.answers_count after filling DB.'

    def handle(self, *args, **options):
        questions = Question.objects.all()
        likes = QuestionLike.objects.all()
        answers = Answer.objects.all()
        for i in tqdm(range(len(questions))):
            questions[i].likes_count = likes.filter(question=questions[i]).count()
            questions[i].answers_count = answers.filter(question=questions[i]).count()
        Question.objects.bulk_update(questions, ['likes_count', 'answers_count'])
        self.stdout.write(self.style.SUCCESS(f'All data is synchronised.'))