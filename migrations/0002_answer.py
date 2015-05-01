# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(to='survey.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
