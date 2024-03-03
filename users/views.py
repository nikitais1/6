from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView

from config import settings

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from users.forms import UserRegisterForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    """
    Класс для авторизации пользователя
    """
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    """
    Класс для регистрации нового пользователя
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Функция генерации ссылки для верификации пользователя по адресу электронной почты"""
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()
        token = default_token_generator.make_token(new_user)
        new_user.email_verification_token = token
        new_user.save()
        uid = urlsafe_base64_encode(force_str(new_user.pk).encode())
        verification_url = reverse('users:activate', kwargs={'uidb64': uid, 'token': token})
        verification_url = self.request.build_absolute_uri(verification_url)
        send_mail(
            subject='Поздравляем с регистрацией',
            message=render_to_string('users/verify_email.html', {'verification_url': verification_url}),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
            fail_silently=False
        )
        print(verification_url)
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для изменения данных пользователя"""
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Функция для получения текущего пользователя (чтобы не использовать pk)"""
        return self.request.user


def activate(request, uidb64, token):
    """Функция активации пользователя в случае успешной верификации по адресу электронной почты"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserDoesNotExist):
        user = None
    if user and user.email_verification_token == token:
        user.is_active = True
        user.save()
        return redirect('users:login')
    else:
        return redirect('users:verification_failed')


class UserListView(PermissionRequiredMixin, ListView):
    """Класс для просмотра списка пользователей"""
    permission_required = 'users.view_all_users'
    model = User

    def get_queryset(self):
        """Метод для вывода пользователей исключая себя"""
        return super().get_queryset().exclude(pk=self.request.user.pk).exclude(is_superuser=True)


class VerificationFailedView(TemplateView):
    """Класс для неуспешной регистрации пользователя"""
    template_name = 'users/verification_failed.html'


@permission_required('users.set_user_deactivate')
def toggle_active(request, pk):
    """Пермиссия: функция для активации/деактивации пользователя"""
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse('users:users'))