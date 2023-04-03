from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from slugify import slugify

def images_directory_path3(instance, filename):
    return '/'.join(['news',str(instance.slug), str(uuid.uuid4().hex + ".webp")])

class News(models.Model):
        
    title = models.TextField(max_length=200, unique=True, db_index=True, verbose_name='Название новости', blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL новости')
    body = models.TextField(max_length=95000 , verbose_name='Текст новости', blank=True, null=True)
    created_at = models.DateTimeField (auto_now_add=True, verbose_name='Опубликовано')
    published = models.BooleanField(verbose_name='Опубликован', default=False)
    views = models.IntegerField(default=0)
    img = models.ImageField(upload_to=images_directory_path3, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='editor')

    def __str__(self):
        return self.title

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.title)
        return super(News, self).save(*args, **kwargs)

    class Meta :
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
    
    def get_absolute_url(self):
        return reverse('detail_news', kwargs={'news_slug': self.slug})
