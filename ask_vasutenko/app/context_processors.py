import jwt
import time
from django.conf import settings
from .models import *
from django.core.cache import cache
from django.db.models import Sum
from app.models import Profile, Question, Answer
from django.contrib.auth.models import User

from django.utils.timezone import now
from datetime import timedelta


def get_centrifugo_info(user_id):
    secret = settings.CENTRIFUGO_SECRET_KEY
    claims = {
        'sub': str(user_id),
        'exp': int(time.time()) + 5 * 60
    }
    token = jwt.encode(claims, secret, algorithm='HS256')
    return {
        'token': token,
        'ws_url': settings.CENTRIFUGO_WS_URL
    }


def get_and_cache_best_members():
    one_week_ago = now() - timedelta(days=7)
    question_ratings = (
        Question.objects.filter(created_at__gte=one_week_ago).values('author').annotate(rating_sum=Sum('rating'))
    )
    answer_ratings = (
        Answer.objects.filter(created_at__gte=one_week_ago).values('author').annotate(rating_sum=Sum('rating'))
    )

    total_ratings = {}
    for q_score in question_ratings:
        total_ratings[q_score['author']] = total_ratings.get(q_score['author'], 0) + q_score['rating_sum']
    for a_score in answer_ratings:
        total_ratings[a_score['author']] = total_ratings.get(a_score['author'], 0) + a_score['rating_sum']

    best_users = sorted(total_ratings.items(), key=lambda x: x[1], reverse=True)[:10]
    best_users_data = [{'id': user_id, 'total_rating': total_rating} for user_id, total_rating in best_users]
    for user in best_users_data:
        user['username'] = User.objects.get(id=user['id']).username
    cache.set("best_users", best_users_data, timeout=61)

    return best_users_data


def get_and_cache_best_tags():
    best_tags = Tag.objects.get_top()
    cache.set("best_tags", best_tags, timeout=61)
    return best_tags


def get_sidebar():
    best_tags = cache.get('best_tags')
    if not best_tags:
        best_tags = get_and_cache_best_tags()

    best_members = cache.get('best_users')
    if not best_members:
        best_members = get_and_cache_best_members()

    sidebar = {
        'tags': best_tags,
        'bestMembers': best_members
    }

    return sidebar


def global_settings(request):
    sidebar = get_sidebar()

    return {
        'sidebar': sidebar,
        **get_centrifugo_info(request.user.id),
    }
