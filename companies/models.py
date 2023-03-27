import datetime
from msilib.schema import PublishComponent
from tabnanny import verbose
from tempfile import NamedTemporaryFile
from django.conf import settings
from django.core.files import File
from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from slugify import slugify

def images_directory_path2(instance, filename):
    return '/'.join(['companies',str(instance.slug), str(uuid.uuid4().hex + ".png")])

class Constcomp(models.Model):
    class ConstcompManager(models.Manager):
        
        def all(self):
            return self.get_queryset().prefetch_related('ratings').filter(status='published')

        
    title = models.TextField(max_length=200, unique=True, db_index=True, verbose_name='Название строительной компании', blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL строительной компании')
    youtube = models.TextField(max_length=100, verbose_name='Канал на YouTube', blank=True, null=True)
    url = models.TextField(max_length=100 , verbose_name='Сайт строительной компании', blank=True, null=True)
    adress = models.TextField(max_length=800 , verbose_name='Адрес офиса', blank=True, null=True)
    services = models.ManyToManyField('Services', verbose_name='Услуги', blank=True)
    body = models.TextField(max_length=9000 , verbose_name='Описание', blank=True, null=True)
    phone = models.TextField(max_length=20 , verbose_name='Контакты', blank=True, null=True)
    published = models.BooleanField(verbose_name='Опубликован', default=False)
    img = models.ImageField(upload_to=images_directory_path2, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='author')

    def __str__(self):
        return self.title

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Constcomp, self).save(*args, **kwargs)

    class Meta :
        verbose_name = 'Строительная компания'
        verbose_name_plural = 'Строительные компании'
    
    def get_absolute_url(self):
        return reverse('detail_company', kwargs={'constcomp_slug': self.slug})
    
    def get_sum_rating(self):
        return sum([rating.value for rating in self.ratings.all()])

class Services(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Услуги', blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL услуги')
       
    def __str__(self):
        return self.title
    class Meta :
        verbose_name = 'Услуги'
        verbose_name_plural = 'Услуги'
