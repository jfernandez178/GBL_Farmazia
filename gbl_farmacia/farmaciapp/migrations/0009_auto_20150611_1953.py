# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0008_auto_20150611_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pazienteensaio',
            name='ensaioa',
            field=models.ForeignKey(related_name=b'pazientea_ensaioan', to='farmaciapp.Ensaioa', null=True),
        ),
        migrations.AlterField(
            model_name='pazienteensaio',
            name='pazientea',
            field=models.ForeignKey(to='farmaciapp.Pazientea', null=True),
        ),
    ]
