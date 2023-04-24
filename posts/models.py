import datetime
from tabnanny import verbose
from tempfile import NamedTemporaryFile
from django.conf import settings
from django.core.files import File
from django.db import models
from django.shortcuts import render
from django.urls import reverse
import requests
import uuid
from django.contrib.auth.models import User
from slugify import slugify
from PIL import Image



class Post_sale(models.Model):
    class NewManager(models.Manager):
        def get_quertyser(self):
            return super().get_queryset().filter(published=True)

    type_object = models.ForeignKey('Type_object', on_delete=models.CASCADE, verbose_name='Тип объекта', default=0, blank=False, related_name='type_object_st')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name='Тип сделки', blank=False, default=0, related_name='status_st')
    adress = models.TextField(verbose_name='Адрес', max_length=1000, blank=True)
    body = models.TextField(verbose_name='Описание', max_length=5000)
    square = models.IntegerField(blank=True, null=True, verbose_name='Площадь дома')
    floors = models.IntegerField(verbose_name='Этажей в доме', blank=True, null=True)
    land_area = models.IntegerField(verbose_name='Площадь участка')
    land_status = models.ForeignKey('Land_status', on_delete=models.CASCADE, verbose_name='Статус земли', blank=True, null=True)
    heating = models.ForeignKey('Heating', on_delete=models.CASCADE, verbose_name='Отопление', blank=True, null=True)
    year_of_construction = models.CharField(verbose_name='Год постройки', max_length=4, blank=True, null=True)
    house_material = models.ForeignKey('House_material', on_delete=models.CASCADE, verbose_name='Материал Дома', null=True, blank=True)
    ceiling_height = models.CharField(verbose_name='Высота потолков', max_length=5, blank=True, null=True)
    water = models.ForeignKey('Water', on_delete=models.CASCADE, verbose_name='Водоснабжение', null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    created_at = models.DateTimeField (auto_now_add=True, verbose_name='Опубликовано')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='user_post')
    published = models.BooleanField(verbose_name='Опубликован', default=True)
    views = models.IntegerField(default=0)
    houseAdditional = models.ManyToManyField('HouseAdditional', verbose_name='Благоустройство', blank=True)
    rent_amenities = models.ManyToManyField('Rent_amenities', verbose_name='Аренда удобства', blank=True)
    rent_price = models.CharField(verbose_name='Арендная плата', max_length=30, blank=True)
    rent_period = models.ForeignKey('RentPeriod', on_delete=models.CASCADE, verbose_name='Время аренды', blank=True, null=True, related_name='rent_period')
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    urgent_sales = models.BooleanField(verbose_name='Срочная продажа', default=False)
    district = models.ForeignKey('District', on_delete=models.CASCADE, verbose_name='Район', blank=True, null=True)
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
        
def images_directory_path(instance, filename):
    return '/'.join(['villages',str(instance.slug), str(uuid.uuid4().hex + ".png")])

class Cottvill(models.Model):
    title = models.TextField(max_length=200, unique=True, db_index=True, verbose_name='Название поселка', blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL поселка')
    developer = models.TextField(max_length=100, verbose_name='Застройщик', blank=True, null=True)
    url = models.TextField(max_length=100 , verbose_name='Сайт поселка', blank=True, null=True)
    adress = models.TextField(max_length=800 , verbose_name='Адрес поселка', blank=True, null=True)
    status_land = models.ForeignKey('Land_status', on_delete=models.CASCADE, verbose_name='Статус земли', blank=True, null=True)
    col_area = models.IntegerField(verbose_name='Количество участков', blank=True, null=True)
    min_area = models.IntegerField(verbose_name='Минимальная площадь участка', blank=True, null=True)
    max_area = models.IntegerField(verbose_name='Максимальная площадь участка', blank=True, null=True)
    price_area = models.IntegerField(verbose_name='Цена участка', blank=True, null=True)
    сommunications = models.TextField(max_length=15 , verbose_name='Коммуникации', blank=True, null=True)
    body = models.TextField(max_length=9000 , verbose_name='Описание', blank=True, null=True)
    house_price_min = models.TextField(max_length=20 , verbose_name='Минимальная цена дома', blank=True, null=True)
    house_price_max = models.TextField(max_length=20 , verbose_name='Максимальная цена дома', blank=True, null=True)
    col_house = models.TextField(max_length=4 , verbose_name='Количество домов', blank=True, null=True)
    payment = models.TextField(max_length=20 , verbose_name='Ежемесячные взносы', blank=True, null=True)
    published = models.BooleanField(verbose_name='Опубликован', default=False)
    main_slider = models.BooleanField(verbose_name='На главном слайдере', default=False)
    img = models.ImageField(upload_to=images_directory_path, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='user')


    def __str__(self):
        return self.title

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Cottvill, self).save(*args, **kwargs)

    class Meta :
        verbose_name = 'Поселок'
        verbose_name_plural = 'Поселки'
    
    def get_absolute_url(self):
        return reverse('village_detail', kwargs={'village_slug': self.slug})
    
class Status(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Тип сделки', blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL сделки')
       
    def __str__(self):
        return self.title
    class Meta :
        verbose_name = 'Тип сделки'
        verbose_name_plural = 'Типы сделки'

class RentPeriod (models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Время аренды', blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL время аренды')
       
    def __str__(self):
        return self.title
    class Meta :
        verbose_name = 'Время аренды'
        verbose_name_plural = 'Время аренды'        

class District(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Район объекта', blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL района')
       
    def __str__(self):
        return self.title
    class Meta :
        verbose_name = 'Район объекта'
        verbose_name_plural = 'Районы объекта'

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
    title = models.TextField(max_length=50, db_index=True , verbose_name='Тип объекта', blank=True, null=True)
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

class Subscribers(models.Model):
    email = models.EmailField('',max_length=255, unique=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')
       
    def __str__(self):
        return self.email
    
    class Meta :
        verbose_name = 'Подписка на новости'
        verbose_name_plural = 'Подписки на новости'

class Water(models.Model):
    title = models.TextField(max_length=50, db_index=True , verbose_name='Водоснабжение')
       
    def __str__(self):
        return self.title
    
    class Meta :
        verbose_name = 'Водоснабжение'
        verbose_name_plural = 'Водоснабжение'



class PostImage(models.Model):
    def images_directory_path(instance, filename):
        return '/'.join(['images',str(instance.post.id), str(uuid.uuid4().hex + ".webp")])
        
    image_data_link = models.ImageField(upload_to=images_directory_path)
    image_url = models.URLField(blank=True)
    post = models.ForeignKey(Post_sale, on_delete = models.CASCADE, related_name='all_images')

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def get_remote_url(self):
        cleaned_data = super().clean()
        all_images = cleaned_data.get("all_images")
        if self.image_url and not self.image_data_link:
            image_temp = NamedTemporaryFile(delete=True)
            image_temp.write(requests.get(self.image_url).content)
            image_temp.flush()
            with Image.open(all_images) as img:
                self.image_data_link.save(f'photo_{self.pk}.jpg', File(image_temp))
        self.save()


class BannerPost(models.Model):
    def banner_directory_path(instance, filename):
        return '/'.join(['banners',str(instance.alt), str(uuid.uuid4().hex + ".webp")])
    banner = models.ImageField(upload_to=banner_directory_path, blank=True)
    alt = models.TextField(max_length=50, db_index=True , verbose_name='Баннер')
       
    def __str__(self):
        return self.alt
    
    class Meta :
        verbose_name = 'Рекламный баннер'
        verbose_name_plural = 'Рекламные баннеры'