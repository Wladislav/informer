# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informer_vcard', '0003_auto_20170519_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vcard',
            name='geo',
        ),
        migrations.AlterField(
            model_name='vcard_adress',
            name='prefer',
            field=models.BooleanField(default=False, help_text='Рекомендуется как основной', verbose_name='Предпочтительный'),
        ),
        migrations.AlterField(
            model_name='vcard_adress',
            name='type',
            field=models.CharField(choices=[('dom', 'Местный'), ('intl', 'Международный'), ('postal', 'Для писем'), ('parcel', 'Для посылок'), ('home', 'Место проживания'), ('work', 'Место работы')], default='home', help_text='Тип Адреса', max_length=20, verbose_name='Тип адреса'),
        ),
        migrations.AlterField(
            model_name='vcard_email',
            name='prefer',
            field=models.BooleanField(default=False, help_text='Рекомендуется как основной', verbose_name='Предпочтительный'),
        ),
        migrations.AlterField(
            model_name='vcard_impp',
            name='prefer',
            field=models.BooleanField(default=False, help_text='Рекомендуется как основной', verbose_name='Предпочтительный'),
        ),
        migrations.AlterField(
            model_name='vcard_organization',
            name='prefer',
            field=models.BooleanField(default=False, help_text='Рекомендуется как основной', verbose_name='Предпочтительный'),
        ),
    ]
