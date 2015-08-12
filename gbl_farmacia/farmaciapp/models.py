from django.db import models
from django.contrib.auth.models import User

import datetime
from datetime import date
import time



#datu-motak ikusteko:
#https://docs.djangoproject.com/en/1.7/ref/models/fields/#django.db.models.DateField


#Medikamentuari dagokion entitatea eta bere erlazioak
class Medikamentua(models.Model):
    #ident izango da medikamentuaren gako nagusia
    ident = models.CharField(primary_key=True, max_length=128)
    kit = models.IntegerField(blank=True)
    lote = models.IntegerField(blank=True)
    kaduzitatea = models.DateField(blank=True)
    bidalketaZenbakia = models.IntegerField(blank=True)
    bidalketaData = models.DateField(blank=True)

    #medikamentu horren zenbat unitate dauden Stock-ean adierazteko
    unitateak = models.IntegerField(default=1)
    bidalketaOrdua = models.TimeField(blank=True, null=True)

    #Medikamentuaren instantzia eskuratzen denean identzifikatzailearen bidez izendatuko da
    def __unicode__(self):
        return self.ident

#Pazienteari dagokion entitatea eta bere erlazioak
class Pazientea(models.Model):
    #ident izango da Pazientearen gako nagusia
    ident = models.AutoField(primary_key=True)

    #ensaioaren barruan zein id duen adierazteko
    idensaioan = models.CharField(max_length=128, blank=True)
    izena = models.CharField(max_length=128)

    #zein unitate klinikori dagokion paziente hau adierazteko   
    unitateKlinikoa = models.CharField(max_length=128, blank=True)

    #pazienteari dagozkion beharrezko datuak:
    pisua = models.FloatField()
    #datu gehiago behar badira hemen jartzen dira
    

    #IDENSAIOAN EDO IDENT???
    def __unicode__(self):
        return unicode(self.ident)


#Ensaioari dagokion entitatea eta bere erlazioak
class Ensaioa(models.Model):
    
    #Egoerak ensaioa itxita edo irekita dagoen adieraziko du
    egoera = models.CharField(max_length=128)

    hasieraData = models.DateField()

    #bukaera datak null balioa izatea onartu behar da, ensaioa sortzerakoan ez baitu bukaera datarik izago esleituta
    bukaeraData = models.DateField(blank=True, null=True)

    protokoloZenbakia = models.IntegerField(blank=True)

    #titulua bakarra izango denez ensaio bakoitzarentzat, gako nagusia izango da
    titulua = models.CharField(primary_key=True, max_length=128,unique=True)
    
    zerbitzua = models.CharField(max_length=128)
    promotorea = models.CharField(max_length=128)
    estudioMota = models.CharField(max_length=128)
    monitorea = models.CharField(max_length=128)
    ikertzailea = models.CharField(max_length=128)

    #Komentarioak atributuaren balioa hutsik uztea baimendu beharra dago, ez delako betetzeko den derrigorrezko eremu bat izango
    komentarioak = models.CharField(max_length=128, blank=True)



    #Ensaioaren instantzia eskuratzen denean tituluaren bidez izendatuko da
    def __unicode__(self):
        return self.titulua



#Dispentsazioari dagokion entitatea eta bere erlazioak
class Dispentsazioa(models.Model):
	
    bukaeraData = models.DateField()
    
    #Dispentsazioaren gako nagusia identzifikatzailea izango da
    ident = models.AutoField(primary_key=True)

    #Zein ensaiori dagon lotuta gorde behar da
    ensaioa = models.ForeignKey(Ensaioa)

    #dagokion EnsaioErrezeta objektuaren identifikatzailea
    ensaioerrezeta = models.IntegerField(default=0)

    #Aldagai honek gordeko du nork egin duen dispentsazioa
    dispentsatzailea = models.CharField(max_length=128)

    #Dispentsazioaren instantzia eskuratzen denean identifikatzailearen bidez izendatuko da
    def __unicode__(self):
        return unicode(self.ident)

   

#Erlazioak adierazteko behar diren klaseak definitzen dira ondoren


#Ensaioak eta Medikamentuak lotzen dituen entitatea da
class MedikamentuEnsaio(models.Model):
	medikamentua = models.ForeignKey(Medikamentua, null=True, related_name="medikamentua_ensaioan")
	ensaioa = models.ForeignKey(Ensaioa, null=True)

    #MedikamentuEnsaio instantzia eskuratzen denean medikamentuaren bidez izendatuko da
	def __unicode__(self):
		return unicode(self.medikamentua)# + "; " + self.ensaioa)

#Pazienteak eta Dispentsazioak lotzen dituen entitatea da
class PazienteDispentsazio(models.Model):
    #identifikatzaile autoinkremental hau izango da gako nagusia
    identBi = models.AutoField(primary_key=True)
    #identifikatzaile hau Dispentsazioaren identifikatzailearen berdina izango da
    ident = models.IntegerField(default=1)
    medikamentua = models.ForeignKey(Medikamentua, null=True)
    dispentsazioa = models.ForeignKey(Dispentsazioa, null=True)
    paziente = models.ForeignKey(Pazientea, null=True)
    dosia = models.IntegerField(null=True, blank=True) 

    #PazienteDispentsazioren instantzia eskuratzen denean identifikatzailearen bidez izendatuko da; hau da, dispentsazioaren identifikatzailearen bitartez
    def __unicode__(self):
        return unicode(self.ident)

#Ensaioak eta Errezetak lotzen dituen entitatea da
class EnsaioErrezeta(models.Model):
    #identifikatzaile autoinkremental bat izango da gako nagusia
    ident = models.AutoField(primary_key=True)
    ensaioa = models.ForeignKey(Ensaioa, null=True)
    pazientea = models.ForeignKey(Pazientea, null=True)
    preskripzioData = models.DateField(null=True)
    hurrengoPreskripzioData = models.DateField(null=True, blank=True)

    #Aldagai honek kontrolatuko du zein erabiltzailek sortu duen errezeta
    sortzailea = models.CharField(max_length=128, blank=True, null=True)

    #Aldagai honek esango du ea errezeta 'Pendiente' egoeran dagoen edo ez; hau da, onartuta dagoen edo ez
    pendiente = models.CharField(max_length=128, default='Pendiente')

    #Eremu zabal eta ireki bat izango da nahi diren eremuak adierazteko
    gainontzekoEremuak = models.TextField(null=True, blank=True)


    #EnsaioErrezetaren instantzia eskuratzen denean identifikatzailearen bidez izendatuko da
    def __unicode__(self):
		return unicode(self.ident)


#Pazienteak eta Ensaioak lotzen dituen entitatea da
class PazienteEnsaio(models.Model):
    ensaioa = models.ForeignKey(Ensaioa, null=True, related_name="pazientea_ensaioan")
    pazientea = models.ForeignKey(Pazientea, null=True)

    #PazienteEnsaioaren instantzia eskuratzen denean dagokion ensaioaren bidez izendatuko da
    def __unicode__(self):
        return unicode(self.ensaioa)


#Erabiltzailearen profilaren informazioa gordeko duen entitatea da
class ErabiltzaileProfila(models.Model):
    # Lerro hau beharrezkoa da. ErabiltzaileProfila linkatzen du User modeloaren instantziarekin.
    erabiltzailea = models.OneToOneField(User)

    # Gehitu nahi diren atributuak
    #website = models.URLField(blank=True)
    #picture = models.ImageField(upload_to='profile_images', blank=True)
    izena = models.CharField(max_length=128)
    abizena1 = models.CharField(max_length=128)
    abizena2 = models.CharField(max_length=128)
    zerbitzua = models.CharField(max_length=128, default=1, choices=(('Farmazia', 'Farmazia'), ('Medicina', 'Medicina')))
    #...???

    # modelo honen instantzia bat atzitzen denean zein izenekin definituko den instantzia hori adierazten du
    def __unicode__(self):
        return self.erabiltzailea.username

