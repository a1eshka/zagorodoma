from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),

        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'phone', 'photo')
        widgets = {
            'date_of_birth': forms.NumberInput(attrs={'type':'date', 'class': 'form-control'}),
            'phone':forms.TextInput(attrs={'class': 'form-control'}),
            

        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
    
    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Такой email уже используется в системе')
        return email

class UserForgotPasswordForm(PasswordResetForm):
    """
    Запрос на восстановление пароля
    """
    class Meta:
        help_texts = {
            'new_password1': None,
            'new_password2': None,
        }

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserSetNewPasswordForm(SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения
    """
    class Meta:
        help_texts = {
            'new_password1': None,
            'new_password2': None,
        }
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })    
class UserPasswordChangeForm(SetPasswordForm):
    """
    Форма изменения пароля
    """
    class Meta:
        help_texts = {
            'new_password1': None,
            'new_password2': None,
        }
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })            