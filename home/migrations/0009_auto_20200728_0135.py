# Generated by Django 3.0 on 2020-07-28 01:35

from django.db import migrations
import streams.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20200728_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogabout',
            name='content',
            field=wagtail.core.fields.StreamField([('title_and_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Add your title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Add your text', required=True))])), ('Full_richtext', streams.blocks.RichtextBlock()), ('card_block', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Add your title', required=True)), ('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.core.blocks.CharBlock(max_length=50, required=True)), ('text', wagtail.core.blocks.TextBlock(max_length=250, required=True)), ('button_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('button_url', wagtail.core.blocks.URLBlock(help_text='if the button page above is selected, that will be used first', required=False))])))]))], blank=True, null=True),
        ),
    ]
