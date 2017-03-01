from django.db import models
from django import forms
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet
from wagtail_modeltranslation.models import TranslationMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    class Meta:
        verbose_name = _('Список записей')
        verbose_name_plural = _('Список записей')
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(BlogIndexPage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        paginator = Paginator(blogpages, settings.BLOG_PAGINATOR_PER_PAGE)
        page = request.GET.get('page')
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            resources = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            resources = paginator.page(paginator.num_pages)        
        
        context['blogpages'] = resources
        return context
    
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')
    
class BlogPage(TranslationMixin, Page):
    class Meta:
        verbose_name = _('Запись в блоге')
        verbose_name_plural = _('Записи в блоге')
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

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

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

class BlogPageGalleryImage(TranslationMixin, Orderable):
    page = ParentalKey(BlogPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
    
class BlogTagIndexPage(Page):
    class Meta:
        verbose_name = _('Список тегов')
        verbose_name_plural = _('Список тегов')
    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        paginator = Paginator(blogpages, settings.TAGS_PAGINATOR_PER_PAGE)
        page = request.GET.get('page')
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            resources = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            resources = paginator.page(paginator.num_pages)         
        # Update template context
        context = super(BlogTagIndexPage, self).get_context(request)
        context['blogpages'] = resources
        return context
    
@register_snippet
class BlogCategory(TranslationMixin, models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
    def __str__(self):
        return self.name 
    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]