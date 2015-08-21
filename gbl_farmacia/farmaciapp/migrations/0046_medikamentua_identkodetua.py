# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0045_auto_20150813_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='medikamentua',
            name='identKodetua',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
