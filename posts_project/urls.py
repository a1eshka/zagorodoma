from django.contrib import admin
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from posts.sitemaps import PostSitemap
from companies.sitemaps import CompanySitemap
from news.sitemaps import NewsSitemap

sitemaps = {
    'posts': PostSitemap,
    'company': CompanySitemap,
    'News': NewsSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('companies/', include('companies.urls')),
    path('news/', include('news.urls')),
    path('', include('posts.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]  

