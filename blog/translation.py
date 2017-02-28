from .models import BlogPage
from wagtail_modeltranslation.translation import TranslationOptions
from wagtail_modeltranslation.decorators import register


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    fields = (
        'intro',
        'body',
    )