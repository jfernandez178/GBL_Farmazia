# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0041_auto_20150813_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ensaioa',
            name='protokoloZenbakia',
            field=models.CharField(unique=True, max_length=128, blank=True),
        ),
    ]
