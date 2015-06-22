# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0005_auto_20150609_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pazienteensaio',
            name='ensaioa',
            field=models.ForeignKey(to='farmaciapp.Ensaioa', null=True),
        ),
    ]
