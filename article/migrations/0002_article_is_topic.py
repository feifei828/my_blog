# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_topic',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u663e\u793a\u5728\u9996\u9875'),
        ),
    ]
