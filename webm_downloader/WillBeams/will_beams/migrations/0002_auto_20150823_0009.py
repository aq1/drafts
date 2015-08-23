# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('will_beams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webm',
            name='thumbnail',
            field=models.ImageField(default='', upload_to='thumbnail/%Y/%m/%d'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='webm',
            name='video',
            field=models.FileField(upload_to='webm/%Y/%m/%d', blank=True),
        ),
    ]
