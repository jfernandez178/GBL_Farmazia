# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0015_auto_20150616_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medikamentua',
            name='id',
        ),
        migrations.AlterField(
            model_name='ensaioerrezeta',
            name='ensaioa',
            field=models.ForeignKey(to='farmaciapp.Ensaioa', null=True),
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='ident',
            field=models.CharField(max_length=128, unique=True, serialize=False, primary_key=True),
        ),
    ]
