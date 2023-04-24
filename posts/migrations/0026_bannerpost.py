# Generated by Django 3.0.14 on 2023-04-05 14:10

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0025_auto_20230331_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(blank=True, upload_to=posts.models.BannerPost.banner_directory_path)),
                ('alt', models.TextField(db_index=True, max_length=50, verbose_name='Баннер')),
            ],
            options={
                'verbose_name': 'Рекламный баннер',
                'verbose_name_plural': 'Рекламные баннеры',
            },
        ),
    ]