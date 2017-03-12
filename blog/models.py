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
from django.template.defaultfilters import truncatechars_html
from meta.models import ModelMeta
import re

class BlogListPage(Page):
    intro = RichTextField(blank=True)
    class Meta:
        verbose_name = _('Список записей')
        verbose_name_plural = _('Список записей')
    def get_context(self, request):
        context = super(BlogListPage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        paginator = Paginator(blogpages, settings.BLOG_PAGINATOR_PER_PAGE)
        page = request.GET.get('page')
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)        
        for page_res in resources:
            # Obrezaem do 130 simvolov
            truncated_text = truncatechars_html(page_res.specific.body.strip('\r'),150)
            # Udalaem html tegi + <p>chistiy tekst</p>
            page_res.specific.body = '<p>'+re.sub(r'\<[^>]*\>', ' ', truncated_text)+'</p>'

        context['blogpages'] = resources
        return context
    
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')
    
class BlogPage(TranslationMixin, ModelMeta, Page):
    
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

    def main_image_url(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image.get_rendition('fill-750x400').url
        else:
            return ''        

    def get_absolute_url(self):
        abs_url = Page.get_site(self).root_url
        return abs_url+self.url
    
    def get_context(self, request):
            context = super(BlogPage, self).get_context(request)
            context['meta'] = self.as_meta(request)
            return context    

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
    
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    
    _metadata = {
        'title': 'title',
        'use_title_tag': 'title',
        'description': 'intro',
        'image': 'main_image_url',
        'url': 'url',
        'site_name': 'wisemarker.com',
        'published_time': 'first_published_at',
        'modified_time': 'latest_revision_created_at',
        'use_og': 'True',
        'use_twitter':'True',
        'use_facebook':'True',
        'use_googleplus':'True',
    }    

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
    
class BlogTagsListPage(Page):
    class Meta:
        verbose_name = _('Список тегов')
        verbose_name_plural = _('Список тегов')
    def get_context(self, request):
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        paginator = Paginator(blogpages, settings.TAGS_PAGINATOR_PER_PAGE)
        page = request.GET.get('page')
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)         

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
    
