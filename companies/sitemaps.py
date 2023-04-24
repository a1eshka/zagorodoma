from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Constcomp


class CompanySitemap(Sitemap):
    """
    Карта-сайта для компаний
    """

    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Constcomp.objects.all()
    