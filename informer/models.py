from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
import django.core.exceptions
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name = _('Пользователь'), related_name='user', primary_key=True, on_delete=models.CASCADE)
    img_height = models.PositiveIntegerField(verbose_name = _('Высота (px)'), null=True, blank=True)
    img_width = models.PositiveIntegerField(verbose_name = _('Ширина (px)'), null=True, blank=True)    
    photo = models.ImageField(verbose_name = _('Фотография'), upload_to='avatars/', height_field='img_height', width_field='img_width', blank=True)
    website = models.URLField(verbose_name = _('Вебсайт'), default='', blank=True)
    bio = models.TextField(verbose_name = _('О себе'), default='', blank=True)
    phone = models.CharField(verbose_name = _('Телефон'), max_length=20, blank=True, default='')
    city = models.CharField(verbose_name = _('Город'), max_length=100, default='', blank=True)
    country = models.CharField(verbose_name = _('Страна'), max_length=100, default='', blank=True)
    language = models.CharField(choices=settings.LANGUAGES, verbose_name = _('Язык'), max_length=5, blank=False, default=settings.LANGUAGE_CODE)
    last_update = models.DateField(verbose_name = _('Дата обновления'), auto_now=True)
    read_only_fields = ['last_update']
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    class Meta:
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')
    def __str__(self):
        return "Профиль пользователя: %s" % self.user    
    panels = [
        FieldPanel('user'),
        FieldPanel('website'),
        FieldPanel('bio'),
        FieldPanel('phone'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('language'),
        FieldPanel('country'),
        FieldPanel('last_update'),
        ImageChooserPanel('photo'),        
        FieldPanel('img_height'),
        FieldPanel('img_width'),
    ]

def create_profile(sender, **kwargs):
     user = kwargs["instance"]
     if kwargs["created"]:
         user_profile = UserProfile(user=user)
         user_profile.save()
         
post_save.connect(create_profile, sender=User)