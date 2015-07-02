# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0024_auto_20150625_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pazientea',
            name='pisua',
            field=models.FloatField(),
        ),
    ]
