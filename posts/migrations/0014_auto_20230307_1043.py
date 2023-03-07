# Generated by Django 3.0.14 on 2023-03-07 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20230307_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post_sale',
            name='floors',
            field=models.IntegerField(blank=True, null=True, verbose_name='Этажей в доме'),
        ),
        migrations.AlterField(
            model_name='post_sale',
            name='land_area',
            field=models.IntegerField(verbose_name='Площадь участка'),
        ),
        migrations.AlterField(
            model_name='post_sale',
            name='price',
            field=models.IntegerField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='post_sale',
            name='square',
            field=models.IntegerField(blank=True, null=True, verbose_name='Площадь дома'),
        ),
    ]
