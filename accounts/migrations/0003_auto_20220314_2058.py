# Generated by Django 3.0.14 on 2022-03-14 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220303_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='users/profile/', verbose_name='Фотография'),
        ),
    ]
