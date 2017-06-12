# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-22 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informer_vcard', '0007_auto_20170522_0021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vcard',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='vcard',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='vcard',
            name='sound',
        ),
        migrations.AlterField(
            model_name='vcard_messengers',
            name='type',
            field=models.CharField(choices=[('other', 'Другой'), ('icq', 'ICQ'), ('skype', 'Skype'), ('viber', 'Viber'), ('whatsapp', 'WhatsApp'), ('telegram', 'Telegram'), ('jabber', 'Jabber'), ('agent', 'Mail.ru Agent'), ('yahoo', 'Yahoo'), ('allo', 'Allo'), ('snapchat', 'Snapchat ')], default='other', help_text='Название программы мессанджера', max_length=20, verbose_name='Вид мессанджера'),
        ),
        migrations.AlterField(
            model_name='vcard_social',
            name='description',
            field=models.TextField(blank=True, help_text='Краткое описание социальной сети', max_length=256, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='vcard_social',
            name='url',
            field=models.URLField(help_text='Ссылка в интернете', max_length=256, verbose_name='URL Социальной сети'),
        ),
    ]