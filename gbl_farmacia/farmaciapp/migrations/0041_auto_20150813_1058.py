# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0040_auto_20150813_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='ensaioa',
            name='monitoreaEmail',
            field=models.CharField(default='', max_length=240),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ensaioa',
            name='monitoreaFax',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ensaioa',
            name='monitoreaMugikor',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ensaioa',
            name='monitoreaTel',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='ikertzailea',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='titulua',
            field=models.CharField(max_length=600, unique=True, serialize=False, primary_key=True),
        ),
    ]
