# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0017_auto_20150619_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pazientedispentsazio',
            name='ident',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
