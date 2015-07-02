# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0025_auto_20150625_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='medikamentua',
            name='bidalketaOrdua',
            field=models.TimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='medikamentua',
            name='unitateak',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
