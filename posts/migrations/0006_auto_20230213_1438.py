# Generated by Django 3.0.14 on 2023-02-13 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_cottvill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cottvill',
            name='status_land',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Land_status', verbose_name='Статус земли'),
        ),
    ]