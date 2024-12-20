from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from .models import *

from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserForm, SettingsForm, QuestionForm, AnswerForm
from django.urls import reverse
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect

from django.core.files.storage import FileSystemStorage


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


def index(request):
    questions = Question.objects.get_new()
    page = paginate(questions, request)
    sidebar = gen_sidebar()
    return render(request, 'index.html', context={'page': page, 'questions': questions, 'sidebar': sidebar})

@login_required(redirect_field_name="continue")
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
    sidebar = gen_sidebar()
    return render(request, 'hot.html', context={'page': page, 'questions': questions, 'sidebar': sidebar})


def tag(request, id):
    try:
        tag = Tag.objects.get(id=id)
    except Tag.DoesNotExist:
        raise Http404("No Tag matches the given query.")
    questions = Question.objects.get_by_tag(id)
    page = paginate(questions, request)
    sidebar = gen_sidebar()
    return render(request, 'tag.html', context={'tag': tag, 'page': page, 'questions': questions, 'sidebar': sidebar})


def question(request, id):
    sidebar = gen_sidebar()
    question = get_object_or_404(Question, id=id)
    answers = Answer.objects.get_top(question)
    page = paginate(answers, request)
    form = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST, user=request.user, question=question)
        if form.is_valid():
            answer = form.save()
            page_number = answers.count() // 10 + 1
            return redirect(reverse('question', kwargs={'id': form.instance.question_id}) + f'?page={page_number}#answer-{answer.id}')
    return render(request, 'question.html', context={'question': question, 'page': page, 'sidebar': sidebar, 'form': form})


    # if request.method == 'POST':
    #     form = QuestionForm(request.POST, user=request.user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(reverse('question', kwargs={'id': form.instance.id}))
    # else:
    #     form = QuestionForm()


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
        # return render(request, 'login.html', {'sidebar': sidebar, 'form': form})
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


# @login_required
# def ask(request):
#     sidebar = gen_sidebar()
#     return render(request, 'ask.html', context={'sidebar': sidebar})


@login_required(redirect_field_name="continue")
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
