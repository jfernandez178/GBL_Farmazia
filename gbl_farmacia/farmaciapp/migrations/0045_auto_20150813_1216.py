# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0044_auto_20150813_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medikamentua',
            name='lote',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]
