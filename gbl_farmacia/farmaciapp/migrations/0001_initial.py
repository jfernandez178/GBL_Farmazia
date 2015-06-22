# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dispentsazio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hasieraData', models.DateField()),
                ('bukaeraData', models.DateField()),
                ('dosia', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ensaio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('egoera', models.CharField(unique=True, max_length=128)),
                ('hasieraData', models.DateField()),
                ('bukaeraData', models.DateField()),
                ('protokoloZenbakia', models.IntegerField()),
                ('titulua', models.CharField(unique=True, max_length=128)),
                ('zerbitzua', models.CharField(max_length=128)),
                ('promotorea', models.CharField(max_length=128)),
                ('estudioMota', models.CharField(max_length=128)),
                ('monitorea', models.CharField(max_length=128)),
                ('ikertzailea', models.CharField(max_length=128)),
                ('komentarioak', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnsaioErrezeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ensaioa', models.ForeignKey(to='farmaciapp.Ensaio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Errezeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('preskripzioData', models.DateField()),
                ('hurrengoPreskripzioData', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Medikamentu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ident', models.CharField(unique=True, max_length=128)),
                ('kaduzitatea', models.DateField()),
                ('bidalketaZenbakia', models.IntegerField(default=0)),
                ('bidalketaData', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MedikamentuEnsaio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ensaioa', models.ForeignKey(to='farmaciapp.Ensaio')),
                ('medikamentua', models.ForeignKey(to='farmaciapp.Medikamentu')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Paziente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ident', models.CharField(unique=True, max_length=128)),
                ('izena', models.CharField(max_length=128)),
                ('unitateKlinikoa', models.CharField(max_length=128)),
                ('pisua', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PazienteDispentsazio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dispentsazioa', models.ForeignKey(to='farmaciapp.Dispentsazio')),
                ('medikamentua', models.ForeignKey(to='farmaciapp.Medikamentu')),
                ('paziente', models.ForeignKey(to='farmaciapp.Paziente')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ensaioerrezeta',
            name='errezeta',
            field=models.ForeignKey(to='farmaciapp.Errezeta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ensaioerrezeta',
            name='paziente',
            field=models.ForeignKey(to='farmaciapp.Paziente'),
            preserve_default=True,
        ),
    ]
