# Generated by Django 5.0.3 on 2024-06-24 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20240614_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_published_at',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
    ]
