# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0010_auto_20150612_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medikamentua',
            name='bidalketaZenbakia',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='kit',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='lote',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='medikamentuensaio',
            name='ensaioa',
            field=models.ForeignKey(to='farmaciapp.Ensaioa', null=True),
        ),
        migrations.AlterField(
            model_name='medikamentuensaio',
            name='medikamentua',
            field=models.ForeignKey(related_name=b'medikamentua_ensaioan', to='farmaciapp.Medikamentua', null=True),
        ),
    ]
