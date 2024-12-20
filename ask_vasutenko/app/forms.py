from django import forms
from django.contrib.auth.models import User
from .models import Profile, Question, Tag, Answer
from django.core.exceptions import ValidationError
import re


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if len(content) > 5000:
            raise forms.ValidationError('Answer must not be more than 5000 characters')
        return content

    def save(self, commit=True):
        answer = super().save(commit=False)
        answer.author_id = self.user.id
        answer.question = self.question
        answer.save()
        return answer


class QuestionForm(forms.ModelForm):
    tags = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) > 100:
            raise forms.ValidationError('Title must not be more than 100 characters')
        return title

    def clean_description(self):
        description = self.cleaned_data['description'].strip()
        if len(description) > 5000:
            raise forms.ValidationError('Description must not be more than 5000 characters')
        return description

    def save(self, commit=True):
        tags_data = self.cleaned_data.pop('tags', '')
        question = super().save(commit=False)
        question.author_id = self.user.id
        question.save()
        tag_names = [tag.strip() for tag in tags_data.split(',') if tag.strip()]
        tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
        question.tags.set(tags)
        return question


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        return self.cleaned_data['username'].strip()


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    username = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('email', 'first_name')

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if re.search(r'[^a-zA-Z0-9]', username):
            raise forms.ValidationError('Username can contain latin letters and numbers')
        if len(username) > 25:
            raise forms.ValidationError('Username must not be more than 25 characters')
        if username != self.user.username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].strip()
        return first_name

    def save(self, commit=True):
        user = User.objects.filter(id=self.user.id)
        user.update(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name']
        )
        if self.files:
            profile = Profile.objects.get(user_id=self.user.id)
            profile.avatar = self.files['avatar']
            profile.save(update_fields=['avatar'])
        return user


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name')

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if re.search(r'[^a-zA-Z0-9]', username):
            raise forms.ValidationError('Username can contain latin letters and numbers')
        if len(username) > 25:
            raise forms.ValidationError('Username must not be more than 25 characters')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username already exists')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('Password must contain at least 8 characters')
        if len(password) > 32:
            raise forms.ValidationError('Password must contain no more than 32 characters')
        if password.isdigit() or password.isalpha() or ' ' in password:
            raise forms.ValidationError('Password must contain letters and numbers')
        return password

    def clean_password_confirmation(self):
        if self.is_valid():
            password = self.cleaned_data['password']
            password_confirmation = self.cleaned_data['password_confirmation']
            if password != password_confirmation:
                raise ValidationError('Passwords do not match')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        if self.files:
            user.profile.avatar = self.files['avatar']
        user.save()
        return user