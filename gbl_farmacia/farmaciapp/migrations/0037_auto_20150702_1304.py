# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0036_pazientedispentsazio_identbi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pazientedispentsazio',
            name='ident',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='pazientedispentsazio',
            name='identBi',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
