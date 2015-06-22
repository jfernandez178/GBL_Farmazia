# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0002_auto_20150609_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ensaioerrezeta',
            name='errezeta',
        ),
        migrations.DeleteModel(
            name='Errezeta',
        ),
        migrations.AddField(
            model_name='ensaioerrezeta',
            name='hurrengoPreskripzioData',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ensaioerrezeta',
            name='preskripzioData',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
