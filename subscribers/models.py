from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

# Create your models here.
class Subscriber(models.Model):
    full_name = models.CharField(max_length=250, blank=False, null=False, help_text="full name")
    email = models.CharField(max_length=250, blank=False, null=False, help_text="email")
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name="+"
    )
    panels = [
        MultiFieldPanel([
            FieldPanel('full_name'),
            FieldPanel("email"),
            ImageChooserPanel("image"),
        ], heading='Subscriber information'),

    ]
    def __str__(self):
        return self.full_name