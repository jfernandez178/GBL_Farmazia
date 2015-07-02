# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0032_auto_20150629_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medikamentua',
            name='unitateak',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
