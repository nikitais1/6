from mailing import forms
from mailing.forms import StyleFormMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Класс для формы регистрации пользователя"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class UserForm(StyleFormMixin, UserChangeForm):
    """Класс для формы профиля пользователя"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()