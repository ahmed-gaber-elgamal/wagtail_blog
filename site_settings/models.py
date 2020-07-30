from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
# Create your models here.
@register_setting
class SocialMediaSettings(BaseSetting):
    facebook =models.URLField(blank=True, null=True, help_text="facebook url")
    gmail = models.URLField(blank=True, null=True, help_text="gmail url")
    linkedin = models.URLField(blank=True, null=True, help_text="linkedin url")
    github = models.URLField(blank=True, null=True, help_text="github url")
    panels = [
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("gmail"),
            FieldPanel("linkedin"),
            FieldPanel("github")
        ], heading="Social Media Settings")
    ]