# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 17:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('informer_vcard', '0009_auto_20170410_2025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vcard',
            name='model_version',
        ),
    ]