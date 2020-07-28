from django.db import models

from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from streams import blocks
class HomePage(Page):
    max_count = 1
    banner_title = models.CharField(max_length=250, blank=False, null=True)
    banner_subtitle = RichTextField(features=['bold', 'italic'])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('banner_title'),
        FieldPanel('banner_subtitle'),
        ImageChooserPanel('banner_image'),
        PageChooserPanel('banner_cta'),
        FieldPanel('body', classname='full'),
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=5, min_num=1)
        ], heading='carousel images')

    ]
    def get_context(self, request):
        context = super().get_context(request)
        blog_indexes = self.get_children().live().order_by('-first_published_at')
        context['blog_indexes'] = blog_indexes
        return context


class BlogAbout(Page):
    max_count = 1
    content = StreamField([
        ("title_and_text", blocks.TitleAndTextBlock()),
        ("Full_richtext", blocks.RichtextBlock()),
        ("card_block", blocks.CardBlock()),
    ], null=True,
       blank=True
    )
    subtitle = models.CharField(max_length=250, blank=True, null=True)
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        StreamFieldPanel("content")
    ]
class HomePageCarouselImages(Orderable):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='carousel_images')
    carousel_image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+', null=True, blank=False)
    caption = models.CharField(blank=True, max_length=250)
    panels = [
        ImageChooserPanel('carousel_image'),

    ]