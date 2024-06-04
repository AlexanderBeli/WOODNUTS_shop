# Generated by Django 5.0.3 on 2024-06-04 20:04

import django.db.models.deletion
import imagekit.models.fields
import products.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_number', models.IntegerField(auto_created=True, unique=True, verbose_name='category number')),
                ('category_name_ru', models.CharField(max_length=50, verbose_name='category name in Russian')),
                ('category_name_en', models.CharField(max_length=50, verbose_name='category name in English')),
                ('category_name_zh_hans', models.CharField(max_length=50, verbose_name='category name in Chinese')),
                ('author_id', models.ForeignKey(auto_created=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['category_number'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(auto_created=True, unique=True, verbose_name='item number')),
                ('item_name_en', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='item name in English')),
                ('item_name_ru', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='item name in Russian')),
                ('item_name_zh_hans', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='item name in Chinese')),
                ('item_picture', imagekit.models.fields.ProcessedImageField(upload_to=products.models.generate_path_and_image, verbose_name='picture')),
                ('item_description_en', models.TextField(blank=True, verbose_name='item description in English')),
                ('item_description_ru', models.TextField(blank=True, verbose_name='item description in Russian')),
                ('item_description_zh_hans', models.TextField(blank=True, verbose_name='item description in Chinese')),
                ('item_extra_tag', models.CharField(choices=[(None, 'Unknown'), ('Fancy Product', 'Fancy Product'), ('Sale', 'Sale'), ('Special Item', 'Special Item'), ('Bestseller', 'Bestseller')], default='Unknown', verbose_name='item extra tag')),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='item price')),
                ('item_price_extra_new', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='extra new item price')),
                ('item_price_currency', models.CharField(choices=[('RUB', 'RUB ₽')], default='RUB', max_length=3, verbose_name='item price currency')),
                ('item_published_at', models.DateField(auto_now_add=True)),
                ('item_author_id', models.ForeignKey(auto_created=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('item_category_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
                'ordering': ['-item_published_at'],
            },
        ),
    ]
