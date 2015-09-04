# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0051_auto_20150822_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='pazientea',
            name='idensaioan',
            field=models.CharField(default='', max_length=128, blank=True),
            preserve_default=False,
        ),
    ]
