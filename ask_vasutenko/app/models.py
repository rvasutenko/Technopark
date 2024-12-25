from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count, Q, F
from django.core.validators import MaxLengthValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-created_at')[:100].prefetch_related('tags')

    def get_top(self):
        return self.order_by('-rating')[:20].prefetch_related('tags')

    def get_by_tag(self, tag_id):
        return self.filter(tags__id=tag_id).order_by('-rating').prefetch_related('tags')


class AnswerManager(models.Manager):
    def get_top(self, question):
        return self.filter(question=question).order_by('-is_correct', '-rating')


class TagManager(models.Manager):
    def get_top(self):
        three_months_ago = now() - timedelta(days=90)
        return self.annotate(
            questions_count=Count('questions', filter=Q(questions__created_at__gte=three_months_ago))
        ).order_by('-questions_count')[:10]


class ProfileManager(models.Manager):
    # def get_top(self):
    #     one_week_ago = now() - timedelta(days=7)
    #     return self.annotate(
    #         q_likes_last_week=Count(
    #             'user__questions__likes',
    #             filter=Q(user__questions__likes__created_at__gte=one_week_ago, user__questions__likes__is_dislike=False)
    #         ),
    #         a_likes_last_week=Count(
    #             'user__answers__likes',
    #             filter=Q(user__answers__likes__created_at__gte=one_week_ago, user__answers__likes__is_dislike=False)
    #         ),
    #         total_popularity=F('q_likes_last_week') + F('a_likes_last_week')
    #     ).order_by('-total_popularity')[:10]
    def get_top(self):
        return self.order_by('-total_popularity')[:10]


class Tag(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50, unique=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Изменён', auto_now=True)

    objects = TagManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class QuestionRate(models.Model):
    is_dislike = models.BooleanField(verbose_name='Дизлайк', default=False, db_index=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='Вопрос', related_name='likes', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='question_likes', db_index=True)
    created_at = models.DateTimeField('Поставлен', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'Like by {self.user} on {self.question}'

    class Meta:
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'
        unique_together = ('question', 'user')


class Question(models.Model):
    STATUS_CHOICES = [
        ('s', 'Solved'),
        ('ns', 'Not Solved'),
    ]
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    description = models.TextField('Описание', validators=[MaxLengthValidator(5000)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='questions', db_index=True)
    tags = models.ManyToManyField('Tag', verbose_name='Теги', blank=False, related_name='questions', db_index=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('Изменён', auto_now=True)
    status = models.CharField(verbose_name='Статус', max_length=16, choices=STATUS_CHOICES, default='ns')
    rating = models.IntegerField(default=0,  db_index=True)
    answers_count = models.PositiveIntegerField(default=0)
    # likes_count = models.IntegerField(default=0, db_index=True)

    objects = QuestionManager()

    def update_status(self):
        if self.answers.filter(is_correct=True).count() > 0:
            self.status = 's'
        else:
            self.status = 'ns'
        self.save(update_fields=['status'])

    @receiver(post_save, sender=QuestionRate)
    @receiver(post_delete, sender=QuestionRate)
    def update_rating(self):
        self.rating = self.likes.filter(is_dislike=False).count() - self.likes.filter(is_dislike=True).count()
        self.save(update_fields=['rating'])

    def update_answers_count(self):
        self.answers_count = self.answers.count()
        self.save(update_fields=['answers_count'])

    def get_absolute_url(self):
        return reverse('question', kwargs={'id': self.pk})

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerRate(models.Model):
    is_dislike = models.BooleanField(verbose_name='Дизлайк', default=False, db_index=True)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name='Ответ', related_name='likes', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='answer_likes', db_index=True)
    created_at = models.DateTimeField('Поставлен', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'Like by {self.user} on {self.answer}'

    class Meta:
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'
        unique_together = ('answer', 'user')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', db_index=True)
    content = models.TextField(verbose_name='Содержание', validators=[MaxLengthValidator(5000)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='answers', db_index=True)
    rating = models.IntegerField(default=0, db_index=True)
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Изменён', auto_now=True)
    # likes_count = models.IntegerField(default=0, db_index=True)

    objects = AnswerManager()

    @receiver(post_save, sender=AnswerRate)
    @receiver(post_delete, sender=AnswerRate)
    def update_rating(self):
        self.rating = self.likes.filter(is_dislike=False).count() - self.likes.filter(is_dislike=True).count()
        self.save(update_fields=['rating'])

    def __str__(self):
        return f'{self.author} to {self.question}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='profile', db_index=True)
    avatar = models.ImageField('Аватар', upload_to='profiles/avatars/', blank=True, null=True)
    # q_likes_count = models.PositiveIntegerField(default=0)
    # a_likes_count = models.PositiveIntegerField(default=0)
    q_likes_last_week = models.PositiveIntegerField(default=0, db_index=True)
    a_likes_last_week = models.PositiveIntegerField(default=0, db_index=True)
    total_popularity = models.PositiveIntegerField(default=0, db_index=True)

    objects = ProfileManager()

    def update_weekly_popularity(self):
        one_week_ago = now() - timedelta(days=7)
        self.q_likes_last_week = self.user.questions.filter(
            likes__created_at__gte=one_week_ago, likes__is_dislike=False
        ).count()
        self.a_likes_last_week = self.user.answers.filter(
            likes__created_at__gte=one_week_ago, likes__is_dislike=False
        ).count()
        self.total_popularity = self.q_likes_last_week + self.a_likes_last_week
        self.save()

    def update_q_likes_count(self):
        self.q_likes_count = self.user.question_likes.count()
        self.save(update_fields=['q_likes_count'])

    def update_a_likes_count(self):
        self.a_likes_count = self.user.answer_likes.count()
        self.save(update_fields=['a_likes_count'])

    def image_tag(self):
        return mark_safe('<img src="%s" style="max-width: 400px; max-width: 400px;" />' % self.avatar.url)
    image_tag.short_description = 'Image'

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
