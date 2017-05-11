# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import vCard, vCard_phone, vCard_adress, vCard_email, vCard_names, vCard_category, vCard_impp, vCard_organization, vCard_related, vCard_expertise, vCard_hobby, vCard_interest


@admin.register(vCard)
class vCardAdmin(admin.ModelAdmin):
    readonly_fields = ('created','revision','version','system',)
    fields  = (
        'user',
        ('version',
        'system',
        'created',
        'revision'),
        ('start',
        'end'),
        'status',
        'objectname',
        'language',
        'tz',
        'photo',
        'label',
        'geo',
        'logo',
        'note',
        'sound',
        'url',
        'secure',
    )
    list_filter = ('user', 'revision', 'start', 'end')

@admin.register(vCard_phone)
class vCard_phoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'tel', 'type', 'function', 'prefer')
    list_filter = ('owner', 'prefer')


@admin.register(vCard_adress)
class vCard_adressAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'adr', 'type', 'prefer')
    list_filter = ('owner', 'prefer')


@admin.register(vCard_email)
class vCard_emailAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'email', 'type', 'prefer')
    list_filter = ('owner', 'prefer')


@admin.register(vCard_names)
class vCard_namesAdmin(admin.ModelAdmin):
    list_display = (
        #'id',
        'owner',
        'full_name',
        'first_name',
        'second_name',
        'middle_name',
        'bday',
        'prefix',
        'suffix',
        'nickname',
        'title',
        'role',
        'sort_as',
    )
    list_filter = ('owner',)


@admin.register(vCard_category)
class vCard_categoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'category')
    list_filter = ('owner',)


@admin.register(vCard_impp)
class vCard_imppAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'url', 'prefer')
    list_filter = ('owner', 'prefer')


@admin.register(vCard_organization)
class vCard_organizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'form', 'org', 'any', 'prefer')
    list_filter = ('owner', 'prefer')


@admin.register(vCard_related)
class vCard_relatedAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'relate', 'type', 'king')
    list_filter = ('owner', 'relate')


@admin.register(vCard_expertise)
class vCard_expertiseAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'expertise', 'type')
    list_filter = ('owner',)


@admin.register(vCard_hobby)
class vCard_hobbyAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'expertise', 'type')
    list_filter = ('owner',)


@admin.register(vCard_interest)
class vCard_interestAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'interest', 'type')
    list_filter = ('owner',)