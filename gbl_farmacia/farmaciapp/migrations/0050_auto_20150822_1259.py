# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0049_auto_20150821_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medikamentua',
            name='bidalketaData',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='bidalketaZenbakia',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='kit',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='lote',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
