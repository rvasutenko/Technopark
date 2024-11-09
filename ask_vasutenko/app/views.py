import random

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate(objectsList, request, perPage=10):
    paginator = Paginator(objectsList, perPage)
    pageNumber = request.GET.get("page")

    try:
        page = paginator.page(pageNumber)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


def genSidebar():
    tags = ['perl', 'python', 'javascript', 'MySQL', 'django', 'mail.ru', 'firefox', 'techno-park']
    bestMembers = ['Mr. Freeman', 'Dr. House', 'Bender', 'Queen Victoria', 'V. Pupkin']
    sidebar = {'tags': tags, 'bestMembers': bestMembers}
    return sidebar


def getQuestions(num):
    questions = []
    for i in range(num):
        questions.append({
            'title': 'title ' + str(i),
            'id': i,
            'text': 'text' + str(i),
            'tags': ['tag1', 'tag2', 'tag3', 'tag4'],
        })
    return questions


def getQuestion(id):
    question = {
        'title': 'title ' + str(id),
        'id': id,
        'text': 'text' + str(id),
        'tags': ['tag1', 'tag2', 'tag3', 'tag4'],
    }
    return question


def getAnswers(num):
    answers = []
    for i in range(num):
        answers.append({
            'id': i,
            'text': 'text' + str(i),
            'likes': random.randint(1, 100),
        })
    return answers


def index(request):
    questions = getQuestions(90)
    page = paginate(questions, request)
    sidebar = genSidebar()
    return render(request, 'index.html', context={'page': page, 'questions': questions, 'sidebar': sidebar})


def settings(request):
    sidebar = genSidebar()
    return render(request, 'settings.html', context={'sidebar': sidebar})


def hot(request):
    questions = getQuestions(13)
    page = paginate(questions, request)
    sidebar = genSidebar()
    return render(request, 'hot.html', context={'page': page, 'questions': questions, 'sidebar': sidebar})


def tag(request, tag):
    questions = getQuestions(15)
    page = paginate(questions, request)
    sidebar = genSidebar()
    return render(request, 'tag.html', context={'tag': tag, 'page': page, 'questions': questions, 'sidebar': sidebar})


def question(request, id):
    question = getQuestion(id)
    answers = getAnswers(50)
    page = paginate(answers, request)
    sidebar = genSidebar()
    return render(request, 'question.html', context={'question': question, 'page': page, 'sidebar': sidebar})


def login(request):
    sidebar = genSidebar()
    return render(request, 'login.html', context={'sidebar': sidebar})


def signup(request):
    sidebar = genSidebar()
    return render(request, 'registration.html', context={'sidebar': sidebar})


def ask(request):
    sidebar = genSidebar()
    return render(request, 'ask.html', context={'sidebar': sidebar})
