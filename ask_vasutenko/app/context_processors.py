import jwt
import time
from django.conf import settings
from .models import *
from django.core.cache import cache


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


def gen_and_cache_sidebar():
    tags = Tag.objects.get_top()
    best_members = Profile.objects.get_top()
    sidebar = {
        'tags': tags,
        'bestMembers': best_members
    }
    cache.set('sidebar', sidebar, timeout=61)
    return sidebar


def global_settings(request):
    sidebar = cache.get('sidebar')
    if not sidebar:
        sidebar = gen_and_cache_sidebar()

    return {
        'sidebar': sidebar,
        **get_centrifugo_info(request.user.id),
    }
