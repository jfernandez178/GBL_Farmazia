# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0028_dispentsazioa_dispentsatzailea'),
    ]

    operations = [
        migrations.AddField(
            model_name='medikamentua',
            name='superident',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medikamentua',
            name='ident',
            field=models.CharField(unique=True, max_length=128),
        ),
    ]
