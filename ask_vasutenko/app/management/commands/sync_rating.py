from django.core.management.base import BaseCommand
from app.models import Tag, Question, Answer, QuestionRate, AnswerRate, Profile
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Synchronise Question.rating and Question.rating.'

    def handle(self, *args, **options):
        questions = Question.objects.all()
        answers = Answer.objects.all()
        for i in tqdm(range(len(questions))):
            questions[i].rating = QuestionRate.objects.filter(question=questions[i], is_dislike=True).count() - QuestionRate.objects.filter(question=questions[i], is_dislike=False).count()
        Question.objects.bulk_update(questions, ['rating'])

        for i in tqdm(range(len(answers))):
            answers[i].rating = AnswerRate.objects.filter(answer=answers[i], is_dislike=True).count() - AnswerRate.objects.filter(answer=answers[i], is_dislike=False).count()
        Answer.objects.bulk_update(answers, ['rating',])

        self.stdout.write(self.style.SUCCESS(f'All data is synchronised.'))

    # def handle(self, *args, **options):
    #     questions = Question.objects.all()
    #     likes = QuestionRate.objects.all()
    #     answers = Answer.objects.all()
    #     for i in tqdm(range(len(questions))):
    #         questions[i].likes_count = likes.filter(question=questions[i]).count()
    #         questions[i].answers_count = answers.filter(question=questions[i]).count()
    #     Question.objects.bulk_update(questions, ['likes_count', 'answers_count'])
    #     self.stdout.write(self.style.SUCCESS(f'All data is synchronised.'))