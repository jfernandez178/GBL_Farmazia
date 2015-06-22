# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0009_auto_20150611_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medikamentuensaio',
            name='medikamentua',
            field=models.ForeignKey(related_name=b'medikamentua_ensaioan', to='farmaciapp.Medikamentua'),
        ),
    ]
