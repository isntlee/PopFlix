# Generated by Django 4.2.8 on 2024-01-17 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0009_alter_channel_slug_alter_content_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
    ]
