# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmaciapp', '0052_pazientea_idensaioan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pazientea',
            name='idensaioan',
        ),
    ]
