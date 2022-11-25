from django.urls import path
from posts import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
 
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('filter/', views.FilterPostsView.as_view(), name="filter"),
    path("json-filter/", views.json_filter, name='json_filter'),
    path("load-more-data", views.load_more_data, name='load_more_data'),
    path('post/new/', HomeCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/', HomeDetailView.as_view(), name='post_detail'),
    path('doma', DomaListView.as_view(), name='doma'),
    path('ychastki', YchastkiListView.as_view(), name='ychastki'),
    path('sales', SalesListView.as_view(), name='sales'),
    path('my_posts', MyPostListView.as_view(), name='my_posts'),
    path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

