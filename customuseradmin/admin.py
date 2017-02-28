# -*- coding:utf-8 -*-
from django.contrib import admin
from blog.models import BlogCategory
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin    
from django.utils.translation import ugettext_lazy as _

admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'id', 'first_name', 'last_name', 'email', 'is_staff','is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
        
admin.site.register(User, CustomUserAdmin)

@admin.register(BlogCategory)
class AdminCategory(admin.ModelAdmin):
    pass