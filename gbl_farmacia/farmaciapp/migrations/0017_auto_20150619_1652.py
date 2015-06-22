# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0016_auto_20150617_1140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispentsazioa',
            name='dosia',
        ),
        migrations.RemoveField(
            model_name='dispentsazioa',
            name='id',
        ),
        migrations.AddField(
            model_name='pazientedispentsazio',
            name='dosia',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dispentsazioa',
            name='ident',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
