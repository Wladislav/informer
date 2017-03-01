from django import template
from wagtail.wagtailcore.models import Page

register = template.Library()

#@register.simple_tag(takes_context=True)
@register.inclusion_tag('blog/blog_page_widget.html')
def last_blog_news(value):
    some_pagr_qs = Page.objects.filter(live=1, content_type_id=32, expired=0).order_by('latest_revision_created_at')[:int(value)]
    context = {}
    context['blogpages'] = some_pagr_qs
    return context
    