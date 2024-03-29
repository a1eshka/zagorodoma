from django.urls import path
from posts import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('filter/', views.FilterPostsView.as_view(), name="filter"),
    path("json-filter/", views.json_filter, name='json_filter'),
    path("load-more-data", views.load_more_data, name='load_more_data'),
    path("load-more-data-sales", views.load_more_data_sales, name='load_more_data_sales'),
    path("load-more-data-rent", views.load_more_data_rent, name='load_more_data_rent'),
    path("load-more-data-doma", views.load_more_data_doma, name='load_more_data_doma'),
    path("load-more-data-ychastki", views.load_more_data_ychastki, name='load_more_data_ychastki'),
    path("load-more-data-village", views.load_more_data_village, name='load_more_data_village'),
    path('post/new/', HomeCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/', HomeDetailView.as_view(), name='post_detail'),
    path('doma', DomaListView.as_view(), name='doma'),
    path('ychastki', YchastkiListView.as_view(), name='ychastki'),
    path('sales', SalesListView.as_view(), name='sales'),
    path('rent', RentListView.as_view(), name='rent'),
    path('my_posts', MyPostListView.as_view(), name='my_posts'),
    path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),
    path('post_delete/<int:pk>/', views.delete_post, name='post_delete'),
    path('village', VillageListView.as_view(), name='village'),
    path('village/new/', VillageCreateView.as_view(), name='village_new'),
    path('village/<slug:village_slug>/', VillageDetailView.as_view(), name='village_detail'),
    path('village/search', views.VillageSearch.as_view(), name='village_search'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('json_main', views.json_main, name='json_main'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

