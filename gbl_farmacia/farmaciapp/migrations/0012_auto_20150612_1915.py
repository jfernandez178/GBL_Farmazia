# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0011_auto_20150612_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ensaioa',
            name='id',
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='titulua',
            field=models.CharField(max_length=128, unique=True, serialize=False, primary_key=True),
        ),
    ]
