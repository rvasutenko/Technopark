from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hot/", views.hot, name="hot"),
    path("tag/<int:id>/", views.tag, name="tag"),
    path("profile/edit/", views.settings, name="settings"),
    path("question/<int:id>/", views.question, name="question"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("ask/", views.ask, name="ask"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)