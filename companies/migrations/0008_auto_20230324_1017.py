# Generated by Django 3.0.14 on 2023-03-24 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0007_likedislike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='author',
        ),
        migrations.RemoveField(
            model_name='review',
            name='company',
        ),
        migrations.DeleteModel(
            name='LikeDislike',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
