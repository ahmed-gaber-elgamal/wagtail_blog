# Generated by Django 3.0.9 on 2020-08-04 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_blogpage_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='release',
            field=models.IntegerField(default=2000),
        ),
    ]
