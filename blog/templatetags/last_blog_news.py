from django import template
from wagtail.wagtailcore.models import Page
from blog.models import BlogPage
from django.template.defaultfilters import truncatechars_html
from django.contrib.contenttypes.models import ContentType
import re

register = template.Library()

@register.inclusion_tag('blog/blog_page_widget.html')
def last_blog_news(value):
    context = {}
    try:
        content_type_id =  ContentType.objects.get_for_model(BlogPage).pk #37
    except:
        return context
    some_pagr_qs = Page.objects.filter(live=1, content_type_id=content_type_id, expired=0).order_by('latest_revision_created_at')[:int(value)]
    for page_res in some_pagr_qs:
        # Obrezaem do 130 simvolov
        truncated_text = truncatechars_html(page_res.specific.body.strip('\r'),150)
        # Udalaem html tegi + <p>chistiy tekst</p>
        page_res.specific.body = '<p>'+re.sub(r'\<[^>]*\>', ' ', truncated_text)+'</p>'    
    context['blogpages'] = some_pagr_qs
    return context
    
