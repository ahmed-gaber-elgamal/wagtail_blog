# Generated by Django 3.0 on 2020-08-03 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_blogabout_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogabout',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]