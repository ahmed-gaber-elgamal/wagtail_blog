# Generated by Django 3.0 on 2020-08-03 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogabout',
            name='location',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
