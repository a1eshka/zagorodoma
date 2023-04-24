from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import News


class NewsSitemap(Sitemap):
    """
    Карта-сайта для новостей
    """

    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return News.objects.all()

    def lastmod(self, obj):
        return obj.created_at
    