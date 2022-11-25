from django.conf.urls import url
from . import views
from django.urls import path
 
from .views import ShowProfilePageView, SignUpView



urlpatterns = [
    
    url(r'^signup/$', views.register, name='signup'),
    url(r'^edit/$', views.edit, name='edit'),
    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
    path('user_profile/favourites/', views.favourite_list, name='favourite_list'),
    path('user_profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
]