# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0006_auto_20150610_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ensaioa',
            name='bukaeraData',
            field=models.DateField(null=True, blank=True),
        ),
    ]
