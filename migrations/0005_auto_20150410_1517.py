# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20150410_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 15, 17, 43, 49688), verbose_name='answer publication date'),
        ),
    ]
