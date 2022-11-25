# Generated by Django 3.0.14 on 2022-09-20 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='Телефон')),
                ('photo', models.ImageField(blank=True, upload_to='users/profile/', verbose_name='Фотография')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
