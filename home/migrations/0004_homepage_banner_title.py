# Generated by Django 3.0 on 2020-07-27 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='banner_title',
            field=models.CharField(max_length=250, null=True),
        ),
    ]