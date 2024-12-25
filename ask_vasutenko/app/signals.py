from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, QuestionRate, Answer, AnswerRate, Question
from django.contrib.postgres.search import SearchVectorField, SearchVector


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




@receiver(post_save, sender=QuestionRate)
def update_likes_count_on_save(sender, instance, **kwargs):
    instance.question.update_rating()
    # try:
    #     Profile.objects.get(user=instance.user).update_q_likes_count()
    # except Profile.DoesNotExist:
    #     pass


@receiver(post_delete, sender=QuestionRate)
def update_likes_count_on_delete(sender, instance, **kwargs):
    print('handle')
    instance.question.update_rating()
    # try:
    #     Profile.objects.get(user=instance.user).update_q_likes_count()
    # except Profile.DoesNotExist:
    #     pass


@receiver(post_save, sender=AnswerRate)
def update_likes_count_on_save(sender, instance, **kwargs):
    instance.answer.update_rating()
    # try:
    #     Profile.objects.get(user=instance.user).update_a_likes_count()
    # except Profile.DoesNotExist:
    #     pass


@receiver(post_delete, sender=AnswerRate)
def update_likes_count_on_delete(sender, instance, **kwargs):
    instance.answer.update_rating()
    # try:
    #     Profile.objects.get(user=instance.user).update_a_likes_count()
    # except Profile.DoesNotExist:
    #     pass




@receiver(post_save, sender=Answer)
def update_answers_count_on_save(sender, instance, **kwargs):
    instance.question.update_answers_count()
    instance.question.update_status()


@receiver(post_delete, sender=Answer)
def update_answers_count_on_delete(sender, instance, **kwargs):
    instance.question.update_answers_count()
    instance.question.update_status()




@receiver(post_save, sender=Question)
def update_search_vector(sender, instance, **kwargs):
    if kwargs.get('update_fields') is None or 'search_vector' in kwargs.get('update_fields', []):
        return

    post_save.disconnect(update_search_vector, sender=Question)

    try:
        instance.search_vector = SearchVector('title', 'description')
        instance.save(update_fields=['search_vector'])
    finally:
        post_save.connect(update_search_vector, sender=Question)