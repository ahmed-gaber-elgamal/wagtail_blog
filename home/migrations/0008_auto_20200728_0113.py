# Generated by Django 3.0 on 2020-07-28 01:13

from django.db import migrations
import streams.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_blogabout_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogabout',
            name='content',
            field=wagtail.core.fields.StreamField([('title_and_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Add your title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Add your text', required=True))])), ('Full_richtext', streams.blocks.RichtextBlock())], blank=True, null=True),
        ),
    ]