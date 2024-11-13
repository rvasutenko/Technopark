import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Tag, Question, Answer, QuestionLike, AnswerLike, Profile
from faker import Faker
from tqdm import tqdm

fake = Faker()


class Command(BaseCommand):
    help = 'Fill database with test data.'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for filling the database')

    def handle(self, *args, **options):
        ratio = options['ratio']

        users, profiles = [], []
        existing_users = set()
        for i in tqdm(range(ratio)):
            successfull = False
            while not successfull:
                username = fake.user_name()
                if username not in existing_users:
                    user = User(
                        username=username,
                        email=f'{username}@mail.ru',
                        password='admin'
                    )
                    profile = Profile(
                        user=user,
                        avatar=None
                    )
                    users.append(user)
                    profiles.append(profile)
                    existing_users.add(username)
                    successfull = True
        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)
        self.stdout.write(self.style.SUCCESS(f'Created {ratio} users and profiles.'))

        tags = []
        existing_tags = set()
        for i in tqdm(range(ratio)):
            successfull = False
            while not successfull:
                name = ' '.join(fake.words(2))
                if name not in existing_tags:
                    tag = Tag(
                        name=name
                    )
                    tags.append(tag)
                    existing_tags.add(name)
                    successfull = True
        Tag.objects.bulk_create(tags)
        self.stdout.write(self.style.SUCCESS(f'Created {ratio} tags.'))

        questions = []
        for i in tqdm(range(ratio * 10)):
            question = Question(
                title=fake.sentence(),
                description=fake.paragraph(),
                author=random.choice(users),
                status=random.choice(['s', 'ns'])
            )
            questions.append(question)
        questions = Question.objects.bulk_create(questions)
        for i in tqdm(range(len(questions))):
            questions[i].tags.set(random.sample(tags, k=min(3, len(tags))))
        self.stdout.write(self.style.SUCCESS(f'Created {ratio * 10} questions.'))

        answers = []
        for i in tqdm(range(ratio * 100)):
            answer = Answer(
                question=random.choice(questions),
                content=fake.paragraph(),
                author=random.choice(users)
            )
            answers.append(answer)
        Answer.objects.bulk_create(answers)
        self.stdout.write(self.style.SUCCESS(f'Created {ratio * 100} answers.'))

        question_likes = []
        existing_likes = set()
        for i in tqdm(range(min(ratio * ratio * 10, ratio * 200))):
            successfull = False
            while not successfull:
                question = random.choice(questions)
                user = random.choice(users)
                like_key = (question.id, user.id)
                if not like_key in existing_likes:
                    question_like = QuestionLike(
                        question=question,
                        user=user
                    )
                    question_likes.append(question_like)
                    existing_likes.add(like_key)
                    successfull = True
        QuestionLike.objects.bulk_create(question_likes)
        self.stdout.write(self.style.SUCCESS(f'Created {min(ratio * ratio * 10, ratio * 200)} question likes.'))

        answer_likes = []
        existing_likes = set()
        for i in tqdm(range(min(ratio * ratio * 100, ratio * 200))):
            successfull = False
            while not successfull:
                answer = random.choice(answers)
                user = random.choice(users)
                like_key = (answer.id, user.id)
                if not like_key in existing_likes:
                    answer_like = AnswerLike(
                        answer=answer,
                        user=user
                    )
                    answer_likes.append(answer_like)
                    existing_likes.add(like_key)
                    successfull = True
        AnswerLike.objects.bulk_create(answer_likes)
        self.stdout.write(self.style.SUCCESS(f'Created {min(ratio * ratio * 100, ratio * 200)} answer likes.'))
