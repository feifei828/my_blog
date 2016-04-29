# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='\u535a\u5ba2\u6807\u9898')),
                ('tag', models.CharField(max_length=50, verbose_name='\u535a\u5ba2\u6807\u7b7e', blank=True)),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='\u535a\u5ba2\u65e5\u671f')),
                ('content', models.TextField(null=True, verbose_name='\u535a\u5ba2\u6b63\u6587', blank=True)),
            ],
            options={
                'verbose_name': '\u535a\u5ba2\u6587\u7ae0',
            },
        ),
    ]
