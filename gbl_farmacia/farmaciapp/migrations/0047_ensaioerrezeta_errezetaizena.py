# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0046_medikamentua_identkodetua'),
    ]

    operations = [
        migrations.AddField(
            model_name='ensaioerrezeta',
            name='errezetaIzena',
            field=models.CharField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
    ]
