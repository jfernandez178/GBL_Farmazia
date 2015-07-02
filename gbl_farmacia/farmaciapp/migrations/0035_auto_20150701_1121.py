# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0034_auto_20150701_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pazientedispentsazio',
            name='dosia',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
