# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0007_auto_20150610_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pazienteensaio',
            name='pazientea',
            field=models.ForeignKey(related_name=b'pazientea_ensaioan', to='farmaciapp.Pazientea', null=True),
        ),
    ]
