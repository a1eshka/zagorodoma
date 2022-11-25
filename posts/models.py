import datetime
from msilib.schema import PublishComponent
from tabnanny import verbose
from tempfile import NamedTemporaryFile
from django.conf import settings
from django.core.files import File
from django.db import models
from django.urls import reverse
import requests
import uuid
from django.contrib.auth.models import User


class Post_sale(models.Model):
    class NewManager(models.Manager):
        def get_quertyser(self):
            return super().get_queryset().filter(published=True)

    type_object = models.ForeignKey('Type_object', on_delete=models.CASCADE, verbose_name='Тип объекта', blank=True, null=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name='Тип сделки', blank=False, default=1, related_name='status_st')
    adress = models.TextField(verbose_name='Адрес', max_length=1000)
    body = models.TextField(verbose_name='Описание', max_length=5000)
    square = models.IntegerField(blank=True, null=True, verbose_name='Площадь дома', max_length=4)
    floors = models.IntegerField(verbose_name='Этажей в доме', max_length=2, blank=True, null=True)
    land_area = models.IntegerField(verbose_name='Площадь участка', max_length=7)
    land_status = models.ForeignKey('Land_status', on_delete=models.CASCADE, verbose_name='Статус земли', blank=True, null=True)
    heating = models.ForeignKey('Heating', on_delete=models.CASCADE, verbose_name='Отопление', blank=True, null=True)
    year_of_construction = models.CharField(verbose_name='Год постройки', max_length=4, blank=True, null=True)
    house_material = models.ForeignKey('House_material', on_delete=models.CASCADE, verbose_name='Материал Дома', null=True, blank=True)
    ceiling_height = models.CharField(verbose_name='Высота потолков', max_length=5, blank=True, null=True)
    water = models.ForeignKey('Water', on_delete=models.CASCADE, verbose_name='Водоснабжение', null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена', max_length=30)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    created_at = models.DateTimeField (auto_now_add=True, verbose_name='Опубликовано')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='user_post')
    published = models.BooleanField(verbose_name='Опубликован', default=True)
    views = models.IntegerField(default=0)
    houseAdditional = models.ManyToManyField('HouseAdditional', verbose_name='Благоустройство', blank=True)
    rent_amenities = models.ManyToManyField('Rent_amenities', verbose_name='Аренда удобства', blank=True)
    rent_price = models.CharField(verbose_name='Арендная плата', max_length=30)
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    objects = models.Manager()
    newmanager = NewManager ()

   
    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"pk": self.pk})
    @property
    def todaytime(self):
        current_date = datetime.date.today()
        date = self.created_at.date()
        print(self.created_at.time())
        if current_date == date:
            return True
        else:
            return False
    
    @property 
    def pub(self):
        current_date = datetime.date.today()
        date = self.created_at.date()
        date2 = date + datetime.timedelta(days=30)
        if current_date > date2:
            self.published = False
            self.save(self.published)
            return True

        else:
            return False
    class Meta :
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

class Status(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Тип сделки', blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL сделки')
       
    def __str__(self):
        return self.title
    class Meta :
        verbose_name = 'Тип сделки'
        verbose_name_plural = 'Типы сделки'

class Land_status(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Статус земли', blank=True, null=True)
       
    def __str__(self):
        return self.title

    class Meta :
        verbose_name = 'Статус земли'
        verbose_name_plural = 'Статусы земли'

class Heating(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Отопление', blank=True, null=True)
       
    def __str__(self):
        return self.title

    class Meta :
        verbose_name = 'Отопление'
        verbose_name_plural = 'Отопление'

class House_material(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Материал Дома')
       
    def __str__(self):
        return self.title
    
    class Meta :
        verbose_name = 'Материал Дома'
        verbose_name_plural = 'Материалы Дома'

class Type_object(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Тип объекта')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL объекта')
       
    def __str__(self):
        return self.title
    
    class Meta :
        verbose_name = 'Тип объекта'
        verbose_name_plural = 'Типы объекта'

class Rent_amenities(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Аренда удобства')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL объекта')
       
    def __str__(self):
        return self.title
    
    class Meta :
        verbose_name = 'Аренда удобства'
        verbose_name_plural = 'Аренда удобства'


class HouseAdditional(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Благоустройство')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL объекта')
       
    def __str__(self):
        return self.title
    
    class Meta :
        verbose_name = 'Благоустройство'
        verbose_name_plural = 'Благоустройства'

class Water(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Водоснабжение')
       
    def __str__(self):
        return self.title
    
    class Meta :
        verbose_name = 'Водоснабжение'
        verbose_name_plural = 'Водоснабжение'



class PostImage(models.Model):
    def images_directory_path(instance, filename):
        return '/'.join(['images',str(instance.post.id), str(uuid.uuid4().hex + ".png")])
        
    image_data_link = models.ImageField(upload_to=images_directory_path)
    image_url = models.URLField(blank=True)
    post = models.ForeignKey(Post_sale, on_delete = models.CASCADE, related_name='all_images')

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def get_remote_url(self):
        if self.image_url and not self.image_data_link:
            image_temp = NamedTemporaryFile(delete=True)
            image_temp.write(requests.get(self.image_url).content)
            image_temp.flush()
            self.image_data_link.save(f'photo_{self.pk}.jpg', File(image_temp))
        self.save()

class Ip(models.Model): # наша таблица где будут айпи адреса
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


