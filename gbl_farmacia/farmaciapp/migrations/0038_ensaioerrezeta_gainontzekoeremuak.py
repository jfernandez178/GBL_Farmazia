# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0037_auto_20150702_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='ensaioerrezeta',
            name='gainontzekoEremuak',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
