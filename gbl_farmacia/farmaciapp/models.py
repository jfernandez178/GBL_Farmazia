from django.db import models
from django.contrib.auth.models import User

import datetime
from datetime import date
import time

#datu-motak ikusteko:
#https://docs.djangoproject.com/en/1.7/ref/models/fields/#django.db.models.DateField

#Medikamentuari dagokion entitatea eta bere erlazioak
class Medikamentua(models.Model):
    #ident izango da kode bat medikamentua konkreatua denean, eta izena generikoa denean
    ident = models.CharField(primary_key=True, max_length=128, unique=True)
    kit = models.IntegerField()
    lote = models.IntegerField()
    kaduzitatea = models.DateField()
    bidalketaZenbakia = models.IntegerField()
    bidalketaData = models.DateField()



    def __unicode__(self):
        return self.ident

#Pazienteari dagokion entitatea eta bere erlazioak
class Pazientea(models.Model):
    ident = models.AutoField(primary_key=True)
    idensaioan = models.CharField(max_length=128)
    izena = models.CharField(max_length=128)
    unitateKlinikoa = models.CharField(max_length=128)
    pisua = models.FloatField()
    #datu gehiago behar badira hemen jartzen dira
    #TODO


    def __unicode__(self):
        return unicode(self.ident)


#Ensaioari dagokion entitatea eta bere erlazioak
class Ensaioa(models.Model):
    #autoinkrement bezala jarriko diogu gakoa, nahiz eta titulua ere bakarra den
    #ident = models.AutoField(primary_key=True)
	

    #egoera mota nominalekoa izango da: (irekita, itxita)
    egoera = models.CharField(max_length=128)#, default="espezifikatu gabe")
    #egoera = ((irekita, 'irekita'), (itxita, 'itxita'))
    hasieraData = models.DateField()#default=datetime.date(1000, 01, 01))
    bukaeraData = models.DateField(blank=True, null=True)#default=datetime.date(1000, 01, 01), blank=True)
    #protokoloZenbakia mota nominalekoa izango da: (I, II, III, IV, V)
    protokoloZenbakia = models.IntegerField(blank=True)#default=0)
    #protokoloZenbakia = ((I, 'I'), (II, 'II'), (III, 'III'), (IV, 'IV'), (V, 'V'))

    titulua = models.CharField(primary_key=True, max_length=128,unique=True)#, default="espezifikatu gabe")
    #zerbitzua mota nominalekoa izan daiteke...
    zerbitzua = models.CharField(max_length=128)#, default="espezifikatu gabe")
    promotorea = models.CharField(max_length=128)#, default="espezifikatu gabe")
    #estudioMota klase nominalekoa da? (ciego, doble ciego, etab.)
    estudioMota = models.CharField(max_length=128)#, default="espezifikatu gabe")
    monitorea = models.CharField(max_length=128)#, default="espezifikatu gabe")
    ikertzailea = models.CharField(max_length=128)#, default="espezifikatu gabe")
    komentarioak = models.CharField(max_length=128, blank=True)#, default="espezifikatu gabe", blank=True)
    #pazientea = models.ForeignKey(Pazientea)




    def __unicode__(self):
        return self.titulua


#Errezetari dagokion entitatea eta bere erlazioak
#ERREZETAK GAKO BAT IZAN BEHARKO LUKE DESBERDINTZEKO
#class Errezeta(models.Model):
#    preskripzioData = models.DateField()
#    hurrengoPreskripzioData = models.DateField()
#    ident = models.CharField(max_length=128)
#
#   def __unicode__(self):
#        return self.ident


#Dispentsazioari dagokion entitatea eta bere erlazioak
#DISPENTSAZIOAK GAKO BAT IZAN BEHARKO LUKE DESBERDINTZEKO
class Dispentsazioa(models.Model):
	#TODO...
    hasieraData = models.DateField()
    bukaeraData = models.DateField()
    ident = models.AutoField(primary_key=True)
    #zein ensaiori dagon asoziatuta gorde behar da
    ensaioa = models.ForeignKey(Ensaioa)

    def __unicode__(self):
        return unicode(self.ident)

   


#MANY TO MANY ERLAZIOAK NOLA ESLEITZEN DIRA? EZ DAUZKAT ONDO BEHEKO KLASEAK DEFINITUTA?

#Erlazioak adierazteko behar diren klaseak definitzen dira ondoren





class MedikamentuEnsaio(models.Model):
	medikamentua = models.ForeignKey(Medikamentua, null=True, related_name="medikamentua_ensaioan")
	ensaioa = models.ForeignKey(Ensaioa, null=True)

	def __unicode__(self):
		return unicode(self.medikamentua)# + "; " + self.ensaioa)

class PazienteDispentsazio(models.Model):
    ident = models.IntegerField(primary_key=True)
    medikamentua = models.ForeignKey(Medikamentua, null=True)
    dispentsazioa = models.ForeignKey(Dispentsazioa, null=True)
    paziente = models.ForeignKey(Pazientea, null=True)
    dosia = models.FloatField(null=True, blank=True) 
    def __unicode__(self):
        return unicode(self.ident)# + "; " + self.medikamentua + "; " + self.dispentsazioa)


class EnsaioErrezeta(models.Model):
    ident = models.AutoField(primary_key=True)
    ensaioa = models.ForeignKey(Ensaioa, null=True)
    pazientea = models.ForeignKey(Pazientea)
    preskripzioData = models.DateField(null=True)
    hurrengoPreskripzioData = models.DateField(null=True)

    #Aldagai honek kontrolatuko du zein erabiltzailek sortu duen errezeta, berak bakarrik modifikatu ahalko duelako
    sortzailea = models.CharField(max_length=128, blank=True, null=True)

    #Aldagai honek esango du ea errezeta 'pendiente' egoeran dagoen edo ez
    pendiente = models.CharField(max_length=128, default='Pendiente')
	
    def __unicode__(self):
		return unicode(self.ident)# + "; " + self.preskripzioData + "; " + self.pazientea)

class PazienteEnsaio(models.Model):
    ensaioa = models.ForeignKey(Ensaioa, null=True, related_name="pazientea_ensaioan")
    pazientea = models.ForeignKey(Pazientea, null=True)

    def __unicode__(self):
        return unicode(self.ensaioa)


#Hau bakarrik izango litzateke erabiltzaileak bere profila izan nahiko balu.
class ErabiltzaileProfila(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    erabiltzailea = models.OneToOneField(User)

    # Gehitu nahi diren atributuak
    #website = models.URLField(blank=True)
    #picture = models.ImageField(upload_to='profile_images', blank=True)
    izena = models.CharField(max_length=128)
    abizena1 = models.CharField(max_length=128)
    abizena2 = models.CharField(max_length=128)
    zerbitzua = models.CharField(max_length=128)
    #...???

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.erabiltzailea.username



#class EnsaioBerria(models.Model):
#    protokoloZenbakia = forms.IntegerField()
#    titulua = forms.CharField(max_length=128)
#    #egoera spinner bat izan behar da
#    egoera = forms.CharField(max_length=128)
#    data = forms.DateField()
#    zerbitzua = forms.CharField(max_length=128)
#    promotorea = forms.CharField(max_length=128)
#    #ikerkuntzaMota spinner bat izan behar da
#    ikerkuntza_mota = forms.CharField(max_length=128)
#    monitorea = forms.CharField(max_length=128)
#    ikertzailea = forms.CharField(max_length=128)
#    komentarioak = forms.CharField(max_length=3000)
#
#    # Override the __unicode__() method to return out something meaningful!
#    def __unicode__(self):
#        return self.titulua
