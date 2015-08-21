# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0048_erabiltzaileprofila_azpizerbitzua'),
    ]

    operations = [
        migrations.AddField(
            model_name='medikamentua',
            name='unitateak_historikoa',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pazientedispentsazio',
            name='dispentsazioa',
            field=models.ForeignKey(related_name=b'dispentsazioa_pazientearekiko', to='farmaciapp.Dispentsazioa', null=True),
        ),
        migrations.AlterField(
            model_name='pazientedispentsazio',
            name='paziente',
            field=models.ForeignKey(related_name=b'pazientea_dispentsazioan', to='farmaciapp.Pazientea', null=True),
        ),
    ]
