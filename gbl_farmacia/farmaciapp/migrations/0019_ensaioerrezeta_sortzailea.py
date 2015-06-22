# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0018_auto_20150620_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='ensaioerrezeta',
            name='sortzailea',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
