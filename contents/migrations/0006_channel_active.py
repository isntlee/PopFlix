# Generated by Django 4.2.8 on 2024-01-14 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0005_alter_channel_parent_alter_content_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
