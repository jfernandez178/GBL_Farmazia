# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0012_auto_20150612_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ensaioerrezeta',
            name='id',
        ),
        migrations.AddField(
            model_name='ensaioerrezeta',
            name='ident',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ensaioerrezeta',
            name='pendiente',
            field=models.CharField(default=b'Pendiente', max_length=128),
            preserve_default=True,
        ),
    ]
