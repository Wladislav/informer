from django import template
from wagtail.wagtailcore.models import Page
from django.template.defaultfilters import truncatechars_html
import re

register = template.Library()

@register.inclusion_tag('blog/blog_page_widget.html')
def last_blog_news(value):
    some_pagr_qs = Page.objects.filter(live=1, content_type_id=37, expired=0).order_by('latest_revision_created_at')[:int(value)]
    for page_res in some_pagr_qs:
        # Obrezaem do 130 simvolov
        truncated_text = truncatechars_html(page_res.specific.body.strip('\r'),150)
        # Udalaem html tegi + <p>chistiy tekst</p>
        page_res.specific.body = '<p>'+re.sub(r'\<[^>]*\>', ' ', truncated_text)+'</p>'    
    context = {}
    context['blogpages'] = some_pagr_qs
    return context
    
