# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0053_remove_pazientea_idensaioan'),
    ]

    operations = [
        migrations.AddField(
            model_name='pazientea',
            name='idensaioan',
            field=models.CharField(default='1', max_length=128, blank=True),
            preserve_default=False,
        ),
    ]
