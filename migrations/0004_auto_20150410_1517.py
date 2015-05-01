# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_auto_20150410_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 15, 17, 23, 52568), verbose_name='answer publication date'),
        ),
    ]
