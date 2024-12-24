import json

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, JsonResponse, HttpResponse
from .models import *

from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserForm, SettingsForm, QuestionForm, AnswerForm
from django.urls import reverse
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect

from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST
from django.conf import settings as _settings


def bad_request(message):
    response = HttpResponse(json.dumps({'message': message}), content_type='application/json')
    response.status_code = 400
    return response

def handle_file_saving(request, name):
    if request.FILES:
        file = request.FILES[name]
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        return filename


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


def annotate_with_user_rate(request, obj_list):
    if request.user.is_authenticated and obj_list:
        if isinstance(obj_list[0], Question):
            for obj in obj_list:
                obj.user_rate = QuestionRate.objects.filter(question=obj.id, user=request.user).first()
        elif isinstance(obj_list[0], Answer):
            for obj in obj_list:
                obj.user_rate = AnswerRate.objects.filter(answer=obj.id, user=request.user).first()
    return obj_list


def handle_like(request, obj, body):
    if isinstance(obj, Question):
        obj_like, created = QuestionRate.objects.get_or_create(user=request.user, question=obj)
    elif isinstance(obj, Answer):
        obj_like, created = AnswerRate.objects.get_or_create(user=request.user, answer=obj)

    if body.get('type') == 'like':
        if not created and obj_like.is_dislike:
            obj_like.delete()
        else:
            obj_like.save()
    elif body.get('type') == 'dislike':
        if not created and not obj_like.is_dislike:
            obj_like.delete()
        else:
            obj_like.is_dislike = True
            obj_like.save()


def index(request):
    questions = Question.objects.get_new()
    page = paginate(questions, request)
    annotate_with_user_rate(request, page.object_list)
    sidebar = gen_sidebar()
    return render(request, 'index.html', context={'page': page, 'questions': questions, 'sidebar': sidebar})

@login_required(redirect_field_name=_settings.REDIRECT_FIELD_NAME)
def settings(request):
    sidebar = gen_sidebar()
    form = SettingsForm
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
    return render(request, 'settings.html', context={'sidebar': sidebar, 'form': form})


def hot(request):
    questions = Question.objects.get_top()
    page = paginate(questions, request)
    annotate_with_user_rate(request, page.object_list)
    sidebar = gen_sidebar()
    return render(request, 'hot.html', context={'page': page, 'questions': questions, 'sidebar': sidebar})


def tag(request, id):
    try:
        tag = Tag.objects.get(id=id)
    except Tag.DoesNotExist:
        raise Http404("No Tag matches the given query.")
    questions = Question.objects.get_by_tag(id)
    page = paginate(questions, request)
    annotate_with_user_rate(request, page.object_list)
    sidebar = gen_sidebar()
    return render(request, 'tag.html', context={'tag': tag, 'page': page, 'questions': questions, 'sidebar': sidebar})


def question(request, id):
    sidebar = gen_sidebar()

    question = get_object_or_404(Question, id=id)
    annotate_with_user_rate(request, [question])

    answers = Answer.objects.get_top(question)
    page = paginate(answers, request)
    annotate_with_user_rate(request, page.object_list)

    form = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST, user=request.user, question=question)
        if form.is_valid():
            answer = form.save()
            page_number = answers.count() // 10 + 1
            return redirect(reverse('question', kwargs={'id': form.instance.question_id}) + f'?page={page_number}#answer-{answer.id}')
    return render(request, 'question.html', context={'question': question, 'page': page, 'sidebar': sidebar, 'form': form})


@login_required(redirect_field_name=_settings.REDIRECT_FIELD_NAME)
@require_POST
@csrf_protect
def question_like(request, id):
    body = json.loads(request.body)
    question = get_object_or_404(Question, id=id)

    handle_like(request, question, body)
    question.update_rating()

    return JsonResponse({
        'rating': question.rating,
    })


@login_required(redirect_field_name=_settings.REDIRECT_FIELD_NAME)
@require_POST
@csrf_protect
def answer_like(request, id):
    body = json.loads(request.body)
    answer = get_object_or_404(Answer, id=id)

    handle_like(request, answer, body)
    answer.update_rating()

    return JsonResponse({
        'rating': answer.rating,
    })


@login_required(redirect_field_name=_settings.REDIRECT_FIELD_NAME)
@require_POST
@csrf_protect
def answer_correct(request, id):
    body = json.loads(request.body)
    answer = get_object_or_404(Answer, id=id)
    question_id = body.get('question_id')
    question = get_object_or_404(Question, id=question_id)
    if request.user == question.author:
        message = ''
        answer.is_correct = not answer.is_correct
        answer.save(update_fields=['is_correct'])
    else:
        message = 'You do not have enough permission'
    return JsonResponse({
        'is_correct': answer.is_correct,
        'message': message,
    })


def login(request):
    sidebar = gen_sidebar()
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                continue_url = request.GET.get('continue', '/')
                return redirect(continue_url)
            form.add_error('password', 'Wrong username or password')
    return render(request, 'login.html', {'sidebar': sidebar, 'form': form})


def logout(request):
    continue_url = request.GET.get('continue', '/')
    auth.logout(request)
    return redirect(continue_url)


def signup(request):
    sidebar = gen_sidebar()
    form = UserForm
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
            return redirect(reverse('index'))
    return render(request, 'registration.html', context={'sidebar': sidebar, 'form': form})


@login_required(redirect_field_name=_settings.REDIRECT_FIELD_NAME)
def ask(request):
    sidebar = gen_sidebar()
    if request.method == 'POST':
        form = QuestionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('question', kwargs={'id': form.instance.id}))
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {'sidebar': sidebar, 'form': form})
