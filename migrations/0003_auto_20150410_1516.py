# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_date',
            field=models.DateTimeField(verbose_name='answer publication date', default=datetime.datetime(2015, 4, 12, 15, 16, 26, 69879)),
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.ForeignKey(null=True, blank=True, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published', editable=False),
        ),
    ]
