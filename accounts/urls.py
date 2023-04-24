from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth.views import *
from .views import *



urlpatterns = [
    
    url(r'^signup/$', views.register, name='signup'),
    url(r'^edit/$', views.edit, name='edit'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
    path('user_profile/favourites/', views.favourite_list, name='favourite_list'),
    path('pub/<int:id>/', views.pub, name='pub'),
    path('user_profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
]