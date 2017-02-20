from django.contrib import admin
from django.contrib.auth.models import User
from . models import UserProfile
from django.utils.translation import ugettext_lazy as _

class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Фотография и ее размер', {'fields': ['photo',('img_width', 'img_height')]}),        
        (None, {'fields': ('website', 'bio', 'phone', ('country', 'city'), 'language', 'last_update')}),
    )
    readonly_fields = ['last_update']
    list_display = ('upper_case_user', 'photo', 'last_update', 'phone', 'country', 'city', 'website', 'language')

    def upper_case_user(self, obj):
        return ("%s %s (%s)" % (obj.user.first_name, obj.user.last_name, obj.user))
    upper_case_user.short_description = 'Пользователи'
    
admin.site.register(UserProfile, UserProfileAdmin)

