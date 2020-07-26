from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full')
    ]
    def get_context(self, request):
        context = super().get_context(request)
        blog_indexes = self.get_children().live().order_by('-first_published_at')
        context['blog_indexes'] = blog_indexes
        return context