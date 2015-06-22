import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gbl_farmacia.settings')

import django
django.setup()

import datetime
from datetime import date
import time

from farmaciapp.models import Medikamentua, Ensaioa, Errezeta, Dispentsazioa, Pazientea, MedikamentuEnsaio, PazienteDispentsazio, EnsaioErrezeta


def populate():

#instantzia desberdinak gehitu ditugu
#medikamentuak
    fecha = datetime.date(2015,03,12)
    medikamentua1 = gehitu_medikamentua('ident1', fecha, 1, datetime.date(2014,03,12))
    fecha = datetime.date(2015,04,12)
    medikamentua2 = gehitu_medikamentua('ident2', fecha, 2, datetime.date(2013,03,12))
    fecha = datetime.date(2015,05,12)
    medikamentua3 = gehitu_medikamentua('ident3', fecha, 3, datetime.date(2012,03,12))

#pazienteak
    pazientea1 = gehitu_pazientea('ident1', 'izena1', 'unitateklinikoa1', 80)
    pazientea2 = gehitu_pazientea('ident2', 'izena2', 'unitateklinikoa2', 90)
    pazientea3 = gehitu_pazientea('ident3', 'izena1', 'unitateklinikoa2', 70.6)
    pazientea4 = gehitu_pazientea('ident4', 'izena3', 'unitateklinikoa1', 60)

#ensaioak
#Bukaera data ez badago esleituta, datetime.date(1000, 1, 1) jarriko dugu
    ensaioa1 = gehitu_ensaioa('irekita', datetime.date(2015,03, 12), datetime.date(1000, 01, 01), 1, 'ensaioa1', 'Farmazia', 'promotorea1', 'doble ciego', 'monitorea1', 'ikertzailea1', 'komentarioak', pazientea1)
    ensaioa1 = gehitu_ensaioa('irekita', datetime.date(2015,02, 12), datetime.date(1000, 01, 01), 2, 'ensaioa2', 'Farmazia', 'promotorea2', 'doble ciego', 'monitorea2', 'ikertzailea1', 'komentarioak', pazientea2)
    ensaioa1 = gehitu_ensaioa('irekita', datetime.date(2015,03, 15), datetime.date(1000, 01, 01), 3, 'ensaioa3', 'Farmazia', 'promotorea3', 'ciego', 'monitorea2', 'ikertzailea1', 'komentarioak', pazientea3)
    ensaioa1 = gehitu_ensaioa('itxita', datetime.date(2015,01, 12), datetime.date(2015, 03, 24), 1, 'ensaioa4', 'Farmazia', 'promotorea1', 'ciego', 'monitorea3', 'ikertzailea2', 'komentarioak', pazientea4)


#dispentsazioak
#Bukaera data ez badago esleituta, datetime.date(1000, 1, 1) jarriko dugu
    dispentsazioa1 = gehitu_dispentsazioa('ident1', datetime.date(2015,01, 12), datetime.date(2015,04, 12), 10, pazientea1, medikamentua1)
    dispentsazioa1 = gehitu_dispentsazioa('ident2', datetime.date(2015,02, 12), datetime.date(2015,04, 12), 1, pazientea2, medikamentua2)
    dispentsazioa1 = gehitu_dispentsazioa('ident3', datetime.date(2015,01, 12), datetime.date(2015,04, 12), 30, pazientea1, medikamentua1)
    dispentsazioa1 = gehitu_dispentsazioa('ident4', datetime.date(2015,03, 12), datetime.date(2015,04, 12), 40, pazientea2, medikamentua2)
    dispentsazioa1 = gehitu_dispentsazioa('ident5', datetime.date(2015,04, 12), datetime.date(1000,01, 01), 10, pazientea3, medikamentua3)
    dispentsazioa1 = gehitu_dispentsazioa('ident6', datetime.date(2015,05, 12), datetime.date(1000,01, 01), 60, pazientea4, medikamentua4)


#errezetak
    errezeta1 = gehitu_errezeta('ident1', datetime.date(2015,05, 12),datetime.date(2015,05, 18),ensaioa1, pazientea1)
    errezeta2 = gehitu_errezeta('ident2', datetime.date(2015,03, 12),datetime.date(2015,05, 12),ensaioa2, pazientea2)
    errezeta3 = gehitu_errezeta('ident3', datetime.date(2015,02, 12),datetime.date(2015,05, 12),ensaioa3, pazientea3)

 

    # Print out what we have added to the user.
    #for c in Category.objects.all():
    #    for p in Page.objects.filter(category=c):
    #        print "- {0} - {1}".format(str(c), str(p))

#medikamentua gehitzeko funztioa; lehenik, existitzen den begiratu, eta horrela ez bada sortu egiten da
def gehitu_medikamentua(ident, kaduzitatea, bidelketaZenbakia, bidalketaData):
    m = Medikamentua.objects.get_or_create(ident=ident)[0]
    m.kaduzitatea = kaduzitatea
    m.bidalketaZenbakia = bidalketaZenbakia
    m.bidalketaData = bidalketaData
    m.save()
    return m

#ensaioa gehitzeko funztioa; lehenik, existitzen den begiratu, eta horrela ez bada sortu egiten da
def gehitu_ensaioa(egoera, hasieraData, bukaeraData, protokoloZenbakia, titulua, zerbitzua, promotorea, estudioMota, monitorea, ikertzailea, komentarioak, pazientea):
    e = Ensaioa.objects.get_or_create(titulua=titulua, hasieraData=hasieraData, pazientea =pazientea)[0]
    e.egoera = egoera
    e.bukaeraData = bukaeraData
    e.protokoloZenbakia = protokoloZenbakia
    e.zerbitzua = zerbitzua
    e.promotorea = promotorea
    e.estudioMota = estudioMota
    e.monitorea = monitorea
    e.ikertzailea = ikertzailea
    e.komentarioak = komentarioak
    e.save()
    return e

#errezeta gehitzeko funztioa; lehenik, existitzen den begiratu, eta horrela ez bada sortu egiten da
#KASU HONETAN, ERLAZIO HIRUTARRA ADIERAZIKO DA, EZ BAITU ZENTZURIK BAKARRIK ERREZETA ADIERAZTEA
def gehitu_errezeta(ident, preskripzioData, hurrengoPreskripzioData, ensaioa, pazientea):
    er = Errezeta.objects.get_or_create(ident=ident)[0]
    er.preskripzioData = preskripzioData
    er.hurrengoPreskripzioData = hurrengoPreskripzioData
    er.save()

    ee = EnsaioErrezeta.objects.get_or_create(ensaioa=ensaioa, errezeta=errezeta, pazientea=pazientea)[0]

    return ee

#pazientea gehitzeko funztioa; lehenik, existitzen den begiratu, eta horrela ez bada sortu egiten da
def gehitu_pazientea(ident, izena, unitateKlinikoa, pisua):
    p = Pazientea.objects.get_or_create(ident=ident)[0]
    p.izena = izena
    p.unitateKlinikoa = unitateKlinikoa
    p.pisua = pisua
    p.save()
    return p

#dispentsazioa gehitzeko funztioa; lehenik, existitzen den begiratu, eta horrela ez bada sortu egiten da
#KASU HONETAN, ERLAZIO HIRUTARRA ADIERAZIKO DA, EZ BAITU ZENTZURIK BAKARRIK DISPENTSAZIOA ADIERAZTEA
#def gehitu_dispentsazioa(hasieraData, bukaeraData, dosia):
#    d = Dispentsazioa.objects.get_or_create(name=name)[0]
#    return c
def gehitu_dispentsazioa(ident, hasieraData, bukaeraData, dosia, pazientea, medikamentua):
    d = Dispentsazioa.objects.get_or_create(ident=ident)[0]
    d.hasieraData = hasieraData
    d.bukaeraData = bukaeraData
    d.dosia = dosia
    d.save()
    pd = PazienteDispentsazio.objexts.get_or_create(medikamentua=medikamentua, pazientea=pazientea,dispentsazioa=d)[0]
    return pd


# Start execution here!
if __name__ == '__main__':
    print "Farmaciapp-eko populazio-script-a martxan..."
    populate()