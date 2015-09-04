# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0054_pazientea_idensaioan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pazienteensaio',
            name='idensaioan',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
