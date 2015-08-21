# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0039_dispentsazioa_ensaioerrezeta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erabiltzaileprofila',
            name='zerbitzua',
            field=models.CharField(default=1, max_length=128, choices=[(b'Farmazia', b'Farmazia'), (b'Medicina', b'Medicina')]),
        ),
    ]
