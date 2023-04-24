from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post_sale


class PostSitemap(Sitemap):
    """
    Карта-сайта для статей
    """

    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Post_sale.objects.all()

    def lastmod(self, obj):
        return obj.created_at
    