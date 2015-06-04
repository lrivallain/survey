# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import survey.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='date published')),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('token', models.CharField(primary_key=True, editable=False, serialize=False, max_length=20, default=survey.models._createToken)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('answer_date', models.DateTimeField(default=survey.models._defaultAnswerDelta, verbose_name='answer publication date')),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='survey.Question'),
            preserve_default=True,
        ),
    ]
