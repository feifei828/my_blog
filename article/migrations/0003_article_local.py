# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_article_is_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='local',
            field=models.CharField(max_length=20, verbose_name='\u4f4d\u7f6e', blank=True),
        ),
    ]
