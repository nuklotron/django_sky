import random

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, LoginForm
from users.models import User


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject="Hello",
            message="Welcome to hell!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def gen_new_password(request):
    new_pass = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject="Сброс пароля!",
        message=f"Ваш новый пароль - {new_pass}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_pass)
    request.user.save()
    return redirect(reverse('main:index'))
