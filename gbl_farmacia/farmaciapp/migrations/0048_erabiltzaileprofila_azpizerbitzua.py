# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0047_ensaioerrezeta_errezetaizena'),
    ]

    operations = [
        migrations.AddField(
            model_name='erabiltzaileprofila',
            name='azpizerbitzua',
            field=models.CharField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
    ]
