from django.contrib import admin
from .models import *


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'author', 'tags', 'status', 'rating')
    list_display = ('title', 'author', 'status')
    filter_horizontal = ('tags',)
    list_filter = ('status',)
    search_fields = ('title', 'author')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    fields = ('question', 'content', 'author', 'rating')
    list_display = ('question', 'author')
    search_fields = ('author', 'question')
    raw_id_fields = ('question',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'avatar')
    list_display = ('user', 'avatar')
    search_fields = ('user',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(QuestionRate)
class QuestionAdmin(admin.ModelAdmin):
    fields = ('user', 'question')
    list_display = ('user', 'question')
    raw_id_fields = ('question',)


@admin.register(AnswerRate)
class AnswerAdmin(admin.ModelAdmin):
    fields = ('user', 'answer')
    list_display = ('user', 'answer')
    raw_id_fields = ('answer',)
