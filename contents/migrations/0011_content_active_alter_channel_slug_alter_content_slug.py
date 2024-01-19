# Generated by Django 4.2.8 on 2024-01-19 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0010_alter_channel_slug_alter_content_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='active',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True, unique=True),
        ),
    ]
