# -*- coding:utf-8 -*-
from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UsernameSearch(object):
    """The User object may not be auth.User, so we need to provide
    a mechanism for issuing the equivalent of a .filter(user__username=...)
    search in CommentAdmin.
    """

    def __str__(self):
        return 'user__%s' % get_user_model().USERNAME_FIELD
    
class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {'fields': ('user', )}
        ),
        (
            _('Content'),
            {'fields': ('photo', 'img_height', 'img_width', 'website', 'bio', 'phone', 'city', 'country', 'language', 'timezone',)}
        ),
        (
            _('Metadata'),
            {'fields': ( )}
        ),
    )
    list_display = ('user', 'phone', 'city', 'country', 'language', 'last_update', )
    raw_id_fields = ('user',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    
admin.site.register(UserProfile, UserProfileAdmin)