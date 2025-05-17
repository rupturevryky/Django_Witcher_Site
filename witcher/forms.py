from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SchoolUser

class UserRegistrationForm(UserCreationForm):
    school = forms.ChoiceField(choices=SchoolUser.SCHOOL_CHOICES, label="Школа")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'school')

class SchoolLoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    school = forms.ChoiceField(choices=SchoolUser.SCHOOL_CHOICES, label="Школа") 