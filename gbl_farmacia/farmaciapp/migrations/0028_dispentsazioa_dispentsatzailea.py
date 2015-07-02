# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0027_remove_dispentsazioa_hasieradata'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispentsazioa',
            name='dispentsatzailea',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
