# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0023_auto_20150624_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ensaioerrezeta',
            name='hurrengoPreskripzioData',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ensaioerrezeta',
            name='pazientea',
            field=models.ForeignKey(to='farmaciapp.Pazientea', null=True),
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='bidalketaData',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='bidalketaZenbakia',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='kaduzitatea',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='kit',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='lote',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='pazientea',
            name='idensaioan',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='pazientea',
            name='pisua',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='pazientea',
            name='unitateKlinikoa',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]
