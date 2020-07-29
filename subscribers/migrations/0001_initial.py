# Generated by Django 3.0 on 2020-07-28 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='full name', max_length=250)),
                ('email', models.CharField(help_text='email', max_length=250)),
            ],
        ),
    ]