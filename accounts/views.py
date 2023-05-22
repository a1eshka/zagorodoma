import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from multiprocessing import context
import smtplib
import ssl
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from requests import request
from .forms import UserForgotPasswordForm, UserPasswordChangeForm, UserRegistrationForm, UserSetNewPasswordForm
from .models import Profile
from .forms import UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic import View, TemplateView
from django.contrib import messages
from posts.models import Post_sale
from .forms import UserRegistrationForm
from django.contrib.auth import login, authenticate
from .mixins import UserIsNotAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from posts_project.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from django.contrib.auth.views import PasswordChangeView
from .services.tasks import send_activate_email_message_task

@ login_required
def favourite_list(request):
    new = Post_sale.newmanager.filter(favourites=request.user)
    return render(request,
                  'profile/favourites.html',
                  {'new': new})


@ login_required
def favourite_add(request, id):
    post = get_object_or_404(Post_sale, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@ login_required
def pub(request, id):
    post = get_object_or_404(Post_sale, id=id)
    post.published = True
    post.created_at = datetime.datetime.now()
    post.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class SignUpView( generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    context_object_name = 'all_posts_list'
    
def register(request, *args, **kwargs):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.is_active = False
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            password = user_form.cleaned_data.get('password')
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Поздравляем! Ваш аккаунт: {username} успешно зарегистрирован! Теперь его необходимо подтвердить. Письмо отправлено Вам на почту.')
            send_activate_email_message_task.delay(new_user.id)
            return redirect('/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'signup.html', {'user_form': user_form})    

class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')
class EmailConfirmationSentView(TemplateView):
    template_name = 'registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context

class EmailConfirmedView(TemplateView):
    template_name = 'registration/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context

class EmailConfirmationFailedView(TemplateView):
    template_name = 'registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context   
        
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Данные профиля успешно изменены.')
        else:
            messages.error(request, 'Ошибка при изменении данных.')
        return redirect ('edit')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
        return render(request,
                      'profile/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'profile/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context
        
User = get_user_model()

class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')
        

class EmailConfirmationSentView(TemplateView):
    template_name = 'registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context

class EmailConfirmedView(TemplateView):
    template_name = 'registration/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context

class EmailConfirmationFailedView(TemplateView):
    template_name = 'registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context

class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'registration/user_password_reset.html'
    success_url = reverse_lazy('home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    email_template_name = 'registration/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'registration/user_password_set_new.html'
    success_url = reverse_lazy('home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'
               
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context    

class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """
    Изменение пароля пользователя
    """
    form_class = UserPasswordChangeForm
    template_name = 'registration/user_password_change.html'
    success_message = 'Ваш пароль был успешно изменён!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля на сайте'
        return context

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.request.user.profile.pk})    