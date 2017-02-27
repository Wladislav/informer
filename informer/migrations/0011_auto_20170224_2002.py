# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-24 17:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('informer', '0010_auto_20170218_0227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Профиль пользователя', 'verbose_name_plural': 'Профили пользователей'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, default='', verbose_name='О себе'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='img_height',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Высота (px)'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='img_width',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Ширина (px)'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.CharField(choices=[('ru', 'Russin'), ('en', 'English')], default='ru', max_length=5, verbose_name='Язык'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_update',
            field=models.DateField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, height_field='img_height', upload_to='avatars/', verbose_name='Фотография', width_field='img_width'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='website',
            field=models.URLField(blank=True, default='', verbose_name='Вебсайт'),
        ),
    ]
