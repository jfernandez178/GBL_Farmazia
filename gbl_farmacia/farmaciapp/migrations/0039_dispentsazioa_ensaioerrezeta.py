# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0038_ensaioerrezeta_gainontzekoeremuak'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispentsazioa',
            name='ensaioerrezeta',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
