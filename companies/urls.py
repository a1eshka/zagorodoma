from . import views
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from .views import *
from .models import *



urlpatterns = [
    path('catalog', ConstcompListView.as_view(), name='catalog'),
    path('detail_company/<slug:constcomp_slug>/', ConstcompDetailView.as_view(), name='detail_company'),
    path('new/', ConstcompCreateView.as_view(), name='companies_new'),
    path('rate_constcomp', rate_constcomp, name='rate_constcomp'),
]