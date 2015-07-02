# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0026_auto_20150627_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispentsazioa',
            name='hasieraData',
        ),
    ]
