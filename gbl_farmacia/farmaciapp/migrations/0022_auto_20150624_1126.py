# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0021_auto_20150624_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ensaioa',
            name='egoera',
            field=models.CharField(default=1, max_length=128, choices=[(1, b'Irekita'), (2, b'Itxita')]),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='estudioMota',
            field=models.CharField(default=1, max_length=128, choices=[(1, b'mota 1'), (2, b'mota 2')]),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='protokoloZenbakia',
            field=models.IntegerField(default=1, blank=True, choices=[(1, b'I'), (2, b'II'), (3, b'III'), (4, b'IV'), (5, b'V')]),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='zerbitzua',
            field=models.CharField(default=1, max_length=128, choices=[(1, b'zerbitzua1'), (2, b'zerbitzua2')]),
        ),
    ]
