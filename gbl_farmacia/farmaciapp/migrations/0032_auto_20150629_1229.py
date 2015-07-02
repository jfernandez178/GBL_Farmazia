# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0031_auto_20150629_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medikamentua',
            name='superident',
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='ident',
            field=models.CharField(max_length=128, serialize=False, primary_key=True),
        ),
    ]
