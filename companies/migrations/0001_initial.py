# Generated by Django 3.0.14 on 2023-03-14 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, db_index=True, max_length=50, null=True, verbose_name='Услуги')),
                ('slug', models.SlugField(unique=True, verbose_name='URL услуги')),
            ],
            options={
                'verbose_name': 'Услуги',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='Constcomp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, db_index=True, max_length=200, null=True, unique=True, verbose_name='Название строительной компании')),
                ('slug', models.SlugField(unique=True, verbose_name='URL строительной компании')),
                ('youtube', models.TextField(blank=True, max_length=100, null=True, verbose_name='Канал на YouTube')),
                ('url', models.TextField(blank=True, max_length=100, null=True, verbose_name='Сайт строительной компании')),
                ('adress', models.TextField(blank=True, max_length=800, null=True, verbose_name='Адрес офиса')),
                ('body', models.TextField(blank=True, max_length=9000, null=True, verbose_name='Описание')),
                ('phone', models.TextField(blank=True, max_length=20, null=True, verbose_name='Контакты')),
                ('rate', models.IntegerField(default=0)),
                ('img', models.ImageField(blank=True, upload_to=posts.models.images_directory_path)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('services', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.Services', verbose_name='Услуги')),
            ],
            options={
                'verbose_name': 'Строительная компания',
                'verbose_name_plural': 'Строительные компании',
            },
        ),
    ]
