from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, QuestionLike, Answer, AnswerLike


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




@receiver(post_save, sender=QuestionLike)
def update_likes_count_on_save(sender, instance, **kwargs):
    instance.question.update_likes_count()
    try:
        Profile.objects.get(user=instance.user).update_q_likes_count()
    except Profile.DoesNotExist:
        pass


@receiver(post_delete, sender=QuestionLike)
def update_likes_count_on_delete(sender, instance, **kwargs):
    instance.question.update_likes_count()
    try:
        Profile.objects.get(user=instance.user).update_q_likes_count()
    except Profile.DoesNotExist:
        pass


@receiver(post_save, sender=AnswerLike)
def update_likes_count_on_save(sender, instance, **kwargs):
    try:
        Profile.objects.get(user=instance.user).update_a_likes_count()
    except Profile.DoesNotExist:
        pass


@receiver(post_delete, sender=AnswerLike)
def update_likes_count_on_delete(sender, instance, **kwargs):
    try:
        Profile.objects.get(user=instance.user).update_a_likes_count()
    except Profile.DoesNotExist:
        pass


@receiver(post_save, sender=Answer)
def update_answers_count_on_save(sender, instance, **kwargs):
    instance.question.update_answers_count()


@receiver(post_delete, sender=Answer)
def update_answers_count_on_delete(sender, instance, **kwargs):
    instance.question.update_answers_count()
