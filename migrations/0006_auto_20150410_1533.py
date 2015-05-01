# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import survey.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20150410_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(null=True, editable=False, to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_date',
            field=models.DateTimeField(verbose_name='answer publication date', default=datetime.datetime(2015, 4, 12, 15, 33, 57, 747017)),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='token',
            field=models.CharField(max_length=20, serialize=False, editable=False, default=survey.models._createToken, primary_key=True),
        ),
    ]
