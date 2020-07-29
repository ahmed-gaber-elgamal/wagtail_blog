# Generated by Django 3.0 on 2020-07-28 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('subscribers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.Image'),
        ),
    ]