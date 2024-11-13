from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hot/", views.hot, name="hot"),
    path("tag/<int:id>/", views.tag, name="tag"),
    path("settings/", views.settings, name="settings"),
    path("question/<int:id>/", views.question, name="question"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("ask/", views.ask, name="ask"),
]
