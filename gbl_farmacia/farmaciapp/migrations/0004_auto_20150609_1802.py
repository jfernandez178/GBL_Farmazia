# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0003_auto_20150609_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pazientea',
            name='id',
        ),
        migrations.AddField(
            model_name='pazientea',
            name='idensaioan',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pazientea',
            name='ident',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
