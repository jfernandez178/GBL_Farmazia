# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0004_auto_20150609_1802'),
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
            name='hasieraData',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='ikertzailea',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='monitorea',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='promotorea',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='titulua',
            field=models.CharField(unique=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='zerbitzua',
            field=models.CharField(max_length=128),
        ),
    ]
