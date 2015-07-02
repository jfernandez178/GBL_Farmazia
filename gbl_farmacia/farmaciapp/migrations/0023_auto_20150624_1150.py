# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0022_auto_20150624_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ensaioa',
            name='egoera',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='estudioMota',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='protokoloZenbakia',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='zerbitzua',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='erabiltzaileprofila',
            name='zerbitzua',
            field=models.CharField(max_length=128),
        ),
    ]
