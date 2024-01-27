# Generated by Django 4.2.8 on 2024-01-24 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0012_remove_channel_parent_channel_superchannel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=True, null=True)),
                ('picture_url', models.URLField(blank=True, max_length=250, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='groups',
            field=models.ManyToManyField(blank=True, to='contents.group'),
        ),
    ]
