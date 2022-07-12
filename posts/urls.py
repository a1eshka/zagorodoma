from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('post/new/', HomeCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/', HomeDetailView.as_view(), name='post_detail'),
    path('', HomePageView.as_view(), name='home'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

