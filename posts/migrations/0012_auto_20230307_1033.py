# Generated by Django 3.0.14 on 2023-03-07 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_cottvill_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post_sale',
            name='floors',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=2, null=True, verbose_name='Этажей в доме'),
        ),
        migrations.AlterField(
            model_name='post_sale',
            name='land_area',
            field=models.DecimalField(decimal_places=1, max_digits=6, verbose_name='Площадь участка'),
        ),
        migrations.AlterField(
            model_name='post_sale',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=20, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='post_sale',
            name='square',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True, verbose_name='Площадь дома'),
        ),
    ]
