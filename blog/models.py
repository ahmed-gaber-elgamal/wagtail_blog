from django.db import models
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField
from django_countries.fields import CountryField
from wagtail.contrib.routable_page.models import route, RoutablePageMixin
from django.shortcuts import render
from streams import blocks


class BlogIndexPage(RoutablePageMixin, Page):
    subpage_types = [
        'blog.BlogPage',
        'blog.VideoBlogPage',
    ]
    parent_page_types = ['home.HomePage']
    # ajax_template = "blog/blog_index_page_ajax.html"
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]
    def get_context(self, request):
        context = super().get_context(request)
        blogpages = BlogPage.objects.live().order_by('-first_published_at')
        paginator = Paginator(blogpages, 1)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['blogpages'] = blogpages
        context['categories'] = BlogCategory.objects.all()
        context['posts'] = posts
        return context

    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        context = self.get_context(request)
        category = BlogCategory.objects.get(slug=cat_slug)
        context['category'] = category
        context['posts'] = BlogPage.objects.filter(categories__in=[category])
        return render(request, "home/category.html", context)

    @route(r"^categories/$", name="categories_view")
    def categories_view(self, request):
        context = self.get_context(request)
        categories = BlogCategory.objects.all
        context['categories'] = categories
        # context['posts'] = BlogPage.objects.filter(categories__in=[category])
        return render(request, "home/categories.html", context)

    @route(r"^year/(\d+)/$", name="year_view")
    def year_view(self, request, year=None):
        context = self.get_context(request)
        context['year'] = year
        if year is not None:
            posts = BlogPage.objects.live().public().filter(release=year)
        else:
            posts = BlogPage.objects.live().public().filter(release=2020)
        print(year)
        context['posts'] = posts
        return render(request, "home/release.html", context)

    @route(r"^years/$", name="years_view")
    def years_view(self, request):
        context = self.get_context(request)
        # context['year'] = year
        posts = BlogPage.objects.live().public().all()
        # print(year)
        context['posts'] = posts
        return render(request, "home/releases.html", context)

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', on_delete=models.CASCADE, related_name='tagged_items')


class BlogPage(RoutablePageMixin, Page):
    subpage_types = []
    parent_page_types = ['blog.BlogIndexPage']
    date = models.DateField('Post date')
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)
    # country = CountryField(multiple=True, blank=True)
    country = CountryField(blank_label='(select country)', default='NZ')
    release = models.IntegerField(default=2000)

    sequel = StreamField([
        ('title_and_text', blocks.TitleAndTextBlock()),

    ],  null=True,
        blank=True
    )

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    content_panels = Page.content_panels+[
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('release'),
            FieldPanel('country'),
            FieldPanel('tags'),
            InlinePanel("post_author", label='Author', max_num=1),
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple),

        ], heading='Blog information'),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('gallery_images', label='Gallery Images'),
        StreamFieldPanel("sequel"),
    ]

    def get_absolute_url(self):
        return self.get_url()


class VideoBlogPage(BlogPage):
    youtube_video_id = models.CharField(max_length=300)
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('youtube_video_id'),
            FieldPanel('date'),
            FieldPanel('tags'),
            InlinePanel("post_author", label='Author', max_num=1),
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple),

        ], heading='Blog information'),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('gallery_images', label='Gallery Images'),
        StreamFieldPanel("sequel")
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

class BlogPageAuthor(Orderable):
    page = ParentalKey(BlogPage, related_name="post_author", null=True)
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
        null=True
    )
    panels = [
        SnippetChooserPanel("author")
    ]

class BlogTagIndexPage(Page):
    subpage_types = []
    parent_page_types = ['home.HomePage']
    def get_context(self, request):
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context['blogpages'] = blogpages
        # context['author'] = BlogPageAuthor.objects.all()
        return context

class BlogAuthor(models.Model):
    name = models.CharField(max_length=250)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name="+"
    )
    panels =  [
        MultiFieldPanel([
            FieldPanel('name'),
            ImageChooserPanel("image"),
        ], heading='Author information'),
        MultiFieldPanel([
            FieldPanel('website'),
            ], heading='Links'),

    ]
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Post Author"
        verbose_name = "Post Authors"
register_snippet(BlogAuthor)

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(
        verbose_name='slug',
        blank=True,
        allow_unicode=True,
        max_length=250,
        help_text='a slug to identify posts by this category'
    )
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "blog categories"

# @register_snippet
# class BlogLogo(models.Model):
#     name = models.CharField(max_length=250)
#     logo = models.ForeignKey(
#         'wagtailimages.Image',
#         on_delete=models.CASCADE,
#         related_name='+'
#     )
#     panels = [
#         FieldPanel('name', classname='full'),
#         ImageChooserPanel('logo')
#     ]
#     def __str__(self):
#         return self.name

