# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0050_auto_20150822_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pazientea',
            name='idensaioan',
        ),
        migrations.AddField(
            model_name='pazienteensaio',
            name='idensaioan',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
    ]
