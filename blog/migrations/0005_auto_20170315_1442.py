# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 11:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20170314_0106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faqpageimage',
            name='faqpage',
        ),
        migrations.RemoveField(
            model_name='faqpageimage',
            name='image',
        ),
        migrations.DeleteModel(
            name='FaqPageImage',
        ),
    ]
