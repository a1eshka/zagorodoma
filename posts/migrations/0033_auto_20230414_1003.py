# Generated by Django 3.0.14 on 2023-04-14 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0032_auto_20230414_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, db_index=True, max_length=50, null=True, verbose_name='Время аренды')),
                ('slug', models.SlugField(unique=True, verbose_name='URL время аренды')),
            ],
            options={
                'verbose_name': 'Время аренды',
                'verbose_name_plural': 'Время аренды',
            },
        ),
        migrations.AddField(
            model_name='post_sale',
            name='rent_period',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rent_period', to='posts.RentPeriod', verbose_name='Время аренды'),
        ),
    ]
