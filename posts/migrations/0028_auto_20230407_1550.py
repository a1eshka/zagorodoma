# Generated by Django 3.0.14 on 2023-04-07 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0027_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribers',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
