# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0043_auto_20150813_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ensaioa',
            name='monitoreaEmail',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='monitoreaFax',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='monitoreaMugikor',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ensaioa',
            name='monitoreaTel',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
