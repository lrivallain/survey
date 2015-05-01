# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import survey.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('token', models.CharField(primary_key=True, serialize=False, default=survey.models._createToken, max_length=20)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('answer_date', models.DateTimeField(verbose_name='answer publication date')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
