from .models import BlogPage, FaqPage, BlogPageGalleryImage#, BlogCategory
from wagtail_modeltranslation.translation import TranslationOptions
from wagtail_modeltranslation.decorators import register


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    fields = (
        'title',
        'intro',
        'body',
    )
    
@register(FaqPage)
class FaqPageTR(TranslationOptions):
    fields = (
        'title',
        'body',
    )    
    
# @register(BlogPageGalleryImage)
# class BlogPageGalleryImageTR(TranslationOptions):
#     fields = (
#         'caption',
#     )
#     
# @register(BlogCategory)
# class BlogCategoryTR(TranslationOptions):
#     fields = (
#         'name',
#     )