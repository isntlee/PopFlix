# Generated by Django 4.2.8 on 2024-01-24 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0013_group_channel_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='groups',
            field=models.ManyToManyField(blank=True, to='contents.group'),
        ),
    ]
