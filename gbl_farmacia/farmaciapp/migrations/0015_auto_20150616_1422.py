# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0014_auto_20150616_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pazientedispentsazio',
            name='dispentsazioa',
            field=models.ForeignKey(to='farmaciapp.Dispentsazioa', null=True),
        ),
        migrations.AlterField(
            model_name='pazientedispentsazio',
            name='medikamentua',
            field=models.ForeignKey(to='farmaciapp.Medikamentua', null=True),
        ),
        migrations.AlterField(
            model_name='pazientedispentsazio',
            name='paziente',
            field=models.ForeignKey(to='farmaciapp.Pazientea', null=True),
        ),
    ]
