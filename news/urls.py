from . import views
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from .views import *
from .models import *



urlpatterns = [
    path('', NewsListView.as_view(), name='news'),
    path('add-news', NewsCreateView.as_view(), name='add_news'),
    path('detail-news/<slug:news_slug>/', NewsDetailView.as_view(), name='detail_news'),
]