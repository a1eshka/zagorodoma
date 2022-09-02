from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('post/new/', HomeCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/', HomeDetailView.as_view(), name='post_detail'),
    path('', HomePageView.as_view(), name='home'),
    path('doma', DomaListView.as_view(), name='doma'),
    path('ychastki', YchastkiListView.as_view(), name='ychastki'),
    path('sales', SalesListView.as_view(), name='sales'),
    path('my_posts', MyPostListView.as_view(), name='my_posts'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

