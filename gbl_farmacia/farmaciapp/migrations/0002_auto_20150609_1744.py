# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('farmaciapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispentsazioa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hasieraData', models.DateField()),
                ('bukaeraData', models.DateField()),
                ('dosia', models.FloatField()),
                ('ident', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ensaioa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('egoera', models.CharField(max_length=128, blank=True)),
                ('hasieraData', models.DateField(blank=True)),
                ('bukaeraData', models.DateField(blank=True)),
                ('protokoloZenbakia', models.IntegerField(blank=True)),
                ('titulua', models.CharField(unique=True, max_length=128, blank=True)),
                ('zerbitzua', models.CharField(max_length=128, blank=True)),
                ('promotorea', models.CharField(max_length=128, blank=True)),
                ('estudioMota', models.CharField(max_length=128, blank=True)),
                ('monitorea', models.CharField(max_length=128, blank=True)),
                ('ikertzailea', models.CharField(max_length=128, blank=True)),
                ('komentarioak', models.CharField(max_length=128, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ErabiltzaileProfila',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('izena', models.CharField(max_length=128)),
                ('abizena1', models.CharField(max_length=128)),
                ('abizena2', models.CharField(max_length=128)),
                ('zerbitzua', models.CharField(max_length=128)),
                ('erabiltzailea', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Medikamentua',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ident', models.CharField(unique=True, max_length=128)),
                ('kit', models.IntegerField(default=0)),
                ('lote', models.IntegerField(default=0)),
                ('kaduzitatea', models.DateField()),
                ('bidalketaZenbakia', models.IntegerField(default=0)),
                ('bidalketaData', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PazienteEnsaio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ensaioa', models.ForeignKey(to='farmaciapp.Ensaioa')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Paziente',
            new_name='Pazientea',
        ),
        migrations.AddField(
            model_name='pazienteensaio',
            name='pazientea',
            field=models.ForeignKey(to='farmaciapp.Pazientea'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dispentsazioa',
            name='ensaioa',
            field=models.ForeignKey(to='farmaciapp.Ensaioa'),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='ensaioerrezeta',
            old_name='paziente',
            new_name='pazientea',
        ),
        migrations.AddField(
            model_name='errezeta',
            name='ident',
            field=models.CharField(default=datetime.date(2015, 6, 9), max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ensaioerrezeta',
            name='ensaioa',
            field=models.ForeignKey(to='farmaciapp.Ensaioa'),
        ),
        migrations.AlterField(
            model_name='medikamentuensaio',
            name='ensaioa',
            field=models.ForeignKey(to='farmaciapp.Ensaioa'),
        ),
        migrations.DeleteModel(
            name='Ensaio',
        ),
        migrations.AlterField(
            model_name='medikamentuensaio',
            name='medikamentua',
            field=models.ForeignKey(to='farmaciapp.Medikamentua'),
        ),
        migrations.AlterField(
            model_name='pazientedispentsazio',
            name='dispentsazioa',
            field=models.ForeignKey(to='farmaciapp.Dispentsazioa'),
        ),
        migrations.DeleteModel(
            name='Dispentsazio',
        ),
        migrations.AlterField(
            model_name='pazientedispentsazio',
            name='medikamentua',
            field=models.ForeignKey(to='farmaciapp.Medikamentua'),
        ),
        migrations.DeleteModel(
            name='Medikamentu',
        ),
    ]
