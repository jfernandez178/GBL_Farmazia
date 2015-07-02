# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0020_auto_20150622_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erabiltzaileprofila',
            name='zerbitzua',
            field=models.CharField(default=1, max_length=128, choices=[(1, b'Farmazia'), (2, b'Medicina')]),
        ),
    ]
