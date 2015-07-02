# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0029_auto_20150629_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medikamentua',
            name='ident',
            field=models.CharField(max_length=128),
        ),
    ]
