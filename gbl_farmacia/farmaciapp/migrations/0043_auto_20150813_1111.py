# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0042_auto_20150813_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ensaioa',
            name='ikertzailea',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='protokoloZenbakia',
            field=models.CharField(unique=True, max_length=128),
        ),
    ]
