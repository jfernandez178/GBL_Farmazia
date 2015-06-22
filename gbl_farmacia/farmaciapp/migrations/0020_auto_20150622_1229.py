# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0019_ensaioerrezeta_sortzailea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ensaioerrezeta',
            name='sortzailea',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
