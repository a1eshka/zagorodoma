# Generated by Django 3.0.14 on 2023-03-20 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_cottvill_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='cottvill',
            name='urgent_sales',
            field=models.BooleanField(default=False, verbose_name='Срочная продажа'),
        ),
    ]
