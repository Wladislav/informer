# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 21:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_comments_xtd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentPost',
            fields=[
                ('xtdcomment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_comments_xtd.XtdComment')),
                ('title', models.CharField(max_length=250)),
                ('enable_comments', models.BooleanField()),
            ],
            options={
                'abstract': False,
                'verbose_name': 'comment',
                'permissions': [('can_moderate', 'Can moderate comments')],
                'verbose_name_plural': 'comments',
                'ordering': ('submit_date',),
            },
            bases=('django_comments_xtd.xtdcomment',),
        ),
    ]
