# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=31)),
            ],
        ),
        migrations.CreateModel(
            name='Webm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('video', models.FileField(upload_to='webm/%Y/%m/%d')),
                ('rating', models.IntegerField(default=0)),
                ('nsfw', models.BooleanField(default=False)),
                ('md5', models.CharField(unique=True, max_length=16, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='WebmTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('tag', models.ForeignKey(to='will_beams.Tag')),
                ('webm', models.ForeignKey(to='will_beams.Webm')),
            ],
        ),
    ]
