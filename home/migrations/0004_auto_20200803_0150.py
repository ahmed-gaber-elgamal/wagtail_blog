# Generated by Django 3.0 on 2020-08-03 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_blogabout_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogabout',
            name='formatted_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='blogabout',
            name='latlng_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
