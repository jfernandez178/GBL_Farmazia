# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0013_auto_20150613_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pazientedispentsazio',
            name='id',
        ),
        migrations.AddField(
            model_name='pazientedispentsazio',
            name='ident',
            field=models.AutoField(default='1', serialize=False, primary_key=True),
            preserve_default=False,
        ),
    ]
