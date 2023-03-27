# Generated by Django 3.0.14 on 2023-03-07 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_auto_20230307_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post_sale',
            name='floors',
            field=models.IntegerField(blank=True, max_length=2, null=True, verbose_name='Этажей в доме'),
        ),
        migrations.AlterField(
            model_name='post_sale',
            name='land_area',
            field=models.IntegerField(max_length=7, verbose_name='Площадь участка'),
        ),
        migrations.AlterField(
            model_name='post_sale',
            name='price',
            field=models.IntegerField(max_length=30, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='post_sale',
            name='square',
            field=models.IntegerField(blank=True, max_length=4, null=True, verbose_name='Площадь дома'),
        ),
    ]