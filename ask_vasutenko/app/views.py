from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get("page")
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def gen_sidebar():
    tags = Tag.objects.get_top()
    best_members = Profile.objects.get_top()
    sidebar = {'tags': tags, 'bestMembers': best_members}
    return sidebar


def index(request):
    questions = Question.objects.get_new()
    page = paginate(questions, request)
    sidebar = gen_sidebar()
    return render(request, 'index.html', context={'page': page, 'questions': questions, 'sidebar': sidebar})


def settings(request):
    sidebar = gen_sidebar()
    return render(request, 'settings.html', context={'sidebar': sidebar})


def hot(request):
    questions = Question.objects.get_top()
    page = paginate(questions, request)
    sidebar = gen_sidebar()
    return render(request, 'hot.html', context={'page': page, 'questions': questions, 'sidebar': sidebar})


def tag(request, id):
    tag = Tag.objects.get(id=id)
    questions = Question.objects.get_by_tag(id)
    page = paginate(questions, request)
    sidebar = gen_sidebar()
    return render(request, 'tag.html', context={'tag': tag, 'page': page, 'questions': questions, 'sidebar': sidebar})


def question(request, id):
    question = Question.objects.get_unique(id)
    answers = Answer.objects.get_top(question)
    page = paginate(answers, request)
    sidebar = gen_sidebar()
    return render(request, 'question.html', context={'question': question, 'page': page, 'sidebar': sidebar})


def login(request):
    sidebar = gen_sidebar()
    return render(request, 'login.html', context={'sidebar': sidebar})


def signup(request):
    sidebar = gen_sidebar()
    return render(request, 'registration.html', context={'sidebar': sidebar})


def ask(request):
    sidebar = gen_sidebar()
    return render(request, 'ask.html', context={'sidebar': sidebar})
