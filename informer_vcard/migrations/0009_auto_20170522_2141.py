# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-22 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informer_vcard', '0008_auto_20170522_2134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vcard_organization',
            old_name='any',
            new_name='description',
        ),
        migrations.AddField(
            model_name='vcard_expertise',
            name='description',
            field=models.TextField(blank=True, help_text='Дополнительная информация', max_length=256, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='vcard_hobby',
            name='description',
            field=models.TextField(blank=True, help_text='Дополнительная информация', max_length=256, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='vcard_interest',
            name='description',
            field=models.TextField(blank=True, help_text='Дополнительная информация', max_length=256, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='vcard_related',
            name='description',
            field=models.TextField(blank=True, help_text='Дополнительная информация', max_length=256, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='vcard_social',
            name='description',
            field=models.TextField(blank=True, help_text='Дополнительная информация', max_length=256, verbose_name='Описание'),
        ),
    ]