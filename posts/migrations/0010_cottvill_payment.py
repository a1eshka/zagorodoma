# Generated by Django 3.0.14 on 2023-02-15 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20230213_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='cottvill',
            name='payment',
            field=models.TextField(blank=True, max_length=20, null=True, verbose_name='Ежемесячные взносы'),
        ),
    ]
