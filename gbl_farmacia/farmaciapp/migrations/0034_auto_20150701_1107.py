# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0033_auto_20150701_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medikamentua',
            name='unitateak',
            field=models.IntegerField(default=1),
        ),
    ]
