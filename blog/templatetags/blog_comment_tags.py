from django.conf import settings
from django import template

register = template.Library()

@register.simple_tag
def unregistered_user_can_comment():
    return settings.UNREGISTERED_USER_CAN_COMMENT

