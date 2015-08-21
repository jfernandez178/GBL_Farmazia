from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from farmaciapp.models import Medikamentua, Pazientea, Dispentsazioa, Ensaioa, ErabiltzaileProfila, PazienteEnsaio, MedikamentuEnsaio, EnsaioErrezeta, PazienteDispentsazio
from farmaciapp.forms import ErabiltzaileFormularioa, ErabiltzaileProfilFormularioa, EnsaioBerriFormularioa, EnsaioBilaketaFormularioa, EnsaioBilaketaFormularioa2, MedikamentuBilaketaFormularioa, MedikamentuBilaketaFormularioa2, Medikamentua, ErrezetaBerriFormularioa, DispentsazioFormularioa, ErrezetaBerriEnsaiotikFormularioa, MedikamentuBerriFormularioa, ErrezetaModifikatuFormularioa, PazienteBerriFormularioa
import time



#Modeloko entitateen sorkuntza-testak:

class PazienteaTest(TestCase):

	def test_paziente_sorkuntza(self):

		pazientea = Pazientea(idensaioan=1, izena='pazientea_proba1', unitateKlinikoa='Oncologia', pisua=80)
		pazientea.save()
		self.assertEqual((pazientea.ident >= 0), True)

		pazientea2 = Pazientea(idensaioan=1, izena='pazientea_proba1', unitateKlinikoa='Oncologia', pisua=80)
		pazientea2.save()
		pazienteKopurua = Pazientea.objects.all().count()
		self.assertTrue(pazienteKopurua == 2)



class EnsaioaTest(TestCase):

	def test_ensaio_sorkuntza(self):
		data = time.strftime('%Y-%m-%d')
		ensaioa = Ensaioa(egoera='irekita', hasieraData=data, protokoloZenbakia='prot1', titulua='ensaioa1', zerbitzua='z', promotorea='p', estudioMota='em', monitorea='m', monitoreaEmail='em', monitoreaFax=123456789, monitoreaTel=123456789, monitoreaMugikor=123456789, ikertzailea='i', komentarioak='')
		ensaioa.save()
		ensaioKopurua = Ensaioa.objects.all().count()
		self.assertTrue(ensaioKopurua == 1)

		ensaioa2 = Ensaioa(egoera='irekita', hasieraData=data, protokoloZenbakia='prot2', titulua='ensaioa2', zerbitzua='z', promotorea='p', estudioMota='em', monitorea='m', monitoreaEmail='em', monitoreaFax=123456789, monitoreaTel=123456789, monitoreaMugikor=123456789, ikertzailea='i', komentarioak='')
		ensaioa2.save()
		ensaioKopurua = Ensaioa.objects.all().count()
		self.assertTrue(ensaioKopurua == 2)

		ensaioa = Ensaioa(egoera='irekita', hasieraData=data, protokoloZenbakia='prot1', titulua='ensaioa1', zerbitzua='z', promotorea='p', estudioMota='em', monitorea='m', monitoreaEmail='em', monitoreaFax=123456789, monitoreaTel=123456789, monitoreaMugikor=123456789, ikertzailea='i', komentarioak='')
		ensaioa.save()
		ensaioKopurua = Ensaioa.objects.all().count()
		self.assertTrue(ensaioKopurua == 2)

class MedikamentuaTest(TestCase):

	def test_medikamentu_sorkuntza(self):
		data = time.strftime('%Y-%m-%d')
		medikamentua = Medikamentua(ident='med1', kit=1, lote='lote', kaduzitatea=data, bidalketaZenbakia=1, bidalketaData=data, unitateak=3)
		medikamentua.save()
		medikamentuKopurua = Medikamentua.objects.all().count()
		self.assertTrue(medikamentuKopurua == 1)

		medikamentua2 = Medikamentua(ident='med2', kit=1, lote='lote', kaduzitatea=data, bidalketaZenbakia=1, bidalketaData=data, unitateak=3)
		medikamentua2.save()
		medikamentuKopurua = Medikamentua.objects.all().count()
		self.assertTrue(medikamentuKopurua == 2)

		
class DispentsazioaTest(TestCase):

	def test_dispentsazio_sorkuntza(self):
		data = time.strftime('%Y-%m-%d')
		ensaioa = Ensaioa(egoera='irekita', hasieraData=data, protokoloZenbakia='prot1', titulua='ensaioa1', zerbitzua='z', promotorea='p', estudioMota='em', monitorea='m', monitoreaEmail='em', monitoreaFax=123456789, monitoreaTel=123456789, monitoreaMugikor=123456789, ikertzailea='i', komentarioak='')
		ensaioa.save()

		disp = Dispentsazioa(bukaeraData=data, ensaioa=ensaioa, ensaioerrezeta=0, dispentsatzailea='dispentsatzailea1')
		disp.save()
		dispKopurua = Dispentsazioa.objects.all().count()
		self.assertTrue(dispKopurua == 1)

		disp = Dispentsazioa(bukaeraData=data, ensaioa=ensaioa, ensaioerrezeta=0, dispentsatzailea='dispentsatzailea1')
		disp.save()
		dispKopurua = Dispentsazioa.objects.all().count()
		self.assertTrue(dispKopurua == 2)


class MedikamentuEnsaioTest(TestCase):

	def test_medikamentuensaio_sorkuntza(self):
		data = time.strftime('%Y-%m-%d')
		medikamentua = Medikamentua(ident='med1', kit=1, lote='lote', kaduzitatea=data, bidalketaZenbakia=1, bidalketaData=data, unitateak=3)
		medikamentua.save()

		medikamentua2 = Medikamentua(ident='med2', kit=1, lote='lote', kaduzitatea=data, bidalketaZenbakia=1, bidalketaData=data, unitateak=3)
		medikamentua2.save()

		ensaioa = Ensaioa(egoera='irekita', hasieraData=data, protokoloZenbakia='prot1', titulua='ensaioa1', zerbitzua='z', promotorea='p', estudioMota='em', monitorea='m', monitoreaEmail='em', monitoreaFax=123456789, monitoreaTel=123456789, monitoreaMugikor=123456789, ikertzailea='i', komentarioak='')
		ensaioa.save()

		medikamentuensaio = MedikamentuEnsaio(medikamentua=medikamentua, ensaioa=ensaioa)
		medikamentuensaio.save()
		medensaiokopurua = MedikamentuEnsaio.objects.all().count()
		self.assertEquals(medensaiokopurua, 1)

		medikamentuensaio2 = MedikamentuEnsaio(medikamentua=medikamentua2, ensaioa=ensaioa)
		medikamentuensaio2.save()
		medensaiokopurua = MedikamentuEnsaio.objects.all().count()
		self.assertEquals(medensaiokopurua, 2)


class PazienteDispentsazioTest(TestCase):

	def test_pazientedispentsazio_sorkuntza(self):
		data = time.strftime('%Y-%m-%d')
		medikamentua1 = Medikamentua(ident='med1', kit=1, lote='lote', kaduzitatea=data, bidalketaZenbakia=1, bidalketaData=data, unitateak=3)
		medikamentua1.save()

		pazientea = Pazientea(idensaioan=1, izena='pazientea_proba1', unitateKlinikoa='Oncologia', pisua=80)
		pazientea.save()

		ensaioa1 = Ensaioa(egoera='irekita', hasieraData=data, protokoloZenbakia='prot1', titulua='ensaioa1', zerbitzua='z', promotorea='p', estudioMota='em', monitorea='m', monitoreaEmail='em', monitoreaFax=123456789, monitoreaTel=123456789, monitoreaMugikor=123456789, ikertzailea='i', komentarioak='')
		ensaioa1.save()

		dispentsazioa1 = Dispentsazioa(bukaeraData=data, ensaioa=ensaioa1, ensaioerrezeta=0, dispentsatzailea='dispentsatzailea1')
		dispentsazioa1.save()

		pazientedispentsazio = PazienteDispentsazio(ident=dispentsazioa1.ident, medikamentua=medikamentua1, dispentsazioa=dispentsazioa1, paziente=pazientea)
		pazientedispentsazio.save()
		pazdispkopurua = PazienteDispentsazio.objects.all().count()
		self.assertEquals(pazdispkopurua, 1)

		pazientedispentsazio2 = PazienteDispentsazio(ident=dispentsazioa1.ident, medikamentua=medikamentua1, dispentsazioa=dispentsazioa1, paziente=pazientea)
		pazientedispentsazio2.save()
		pazdispkopurua = PazienteDispentsazio.objects.all().count()
		self.assertEquals(pazdispkopurua, 2)


class EnsaioErrezetaTest(TestCase):

	def test_ensaioerrezeta_sorkuntza(self):
		data = time.strftime('%Y-%m-%d')
		pazientea = Pazientea(idensaioan=1, izena='pazientea_proba1', unitateKlinikoa='Oncologia', pisua=80)
		pazientea.save()

		ensaioa1 = Ensaioa(egoera='irekita', hasieraData=data, protokoloZenbakia='prot1', titulua='ensaioa1', zerbitzua='z', promotorea='p', estudioMota='em', monitorea='m', monitoreaEmail='em', monitoreaFax=123456789, monitoreaTel=123456789, monitoreaMugikor=123456789, ikertzailea='i', komentarioak='')
		ensaioa1.save()

		ensaioerrezeta = EnsaioErrezeta(ensaioa=ensaioa1, pazientea=pazientea, preskripzioData=data, pendiente='Pendiente')
		ensaioerrezeta.save()
		ensaioerrezetakopurua = EnsaioErrezeta.objects.all().count()
		self.assertEquals(ensaioerrezetakopurua, 1)

		ensaioerrezeta2 = EnsaioErrezeta(ensaioa=ensaioa1, pazientea=pazientea, preskripzioData=data, pendiente='Pendiente')
		ensaioerrezeta2.save()
		ensaioerrezetakopurua = EnsaioErrezeta.objects.all().count()
		self.assertEquals(ensaioerrezetakopurua, 2)



class PazienteEnsaioTest(TestCase):

	def test_pazienteensaio_sorkuntza(self):
		data = time.strftime('%Y-%m-%d')
		pazientea = Pazientea(idensaioan=1, izena='pazientea_proba1', unitateKlinikoa='Oncologia', pisua=80)
		pazientea.save()

		ensaioa1 = Ensaioa(egoera='irekita', hasieraData=data, protokoloZenbakia='prot1', titulua='ensaioa1', zerbitzua='z', promotorea='p', estudioMota='em', monitorea='m', monitoreaEmail='em', monitoreaFax=123456789, monitoreaTel=123456789, monitoreaMugikor=123456789, ikertzailea='i', komentarioak='')
		ensaioa1.save()

		ensaioa2 = Ensaioa(egoera='irekita', hasieraData=data, protokoloZenbakia='prot2', titulua='ensaioa2', zerbitzua='z', promotorea='p', estudioMota='em', monitorea='m', monitoreaEmail='em', monitoreaFax=123456789, monitoreaTel=123456789, monitoreaMugikor=123456789, ikertzailea='i', komentarioak='')
		ensaioa2.save()

		pazienteensaio = PazienteEnsaio(ensaioa=ensaioa1, pazientea=pazientea)
		pazienteensaio.save()
		pazienteensaiokopurua = PazienteEnsaio.objects.all().count()
		self.assertEquals(pazienteensaiokopurua, 1)

		pazienteensaio2 = PazienteEnsaio(ensaioa=ensaioa1, pazientea=pazientea)
		pazienteensaio2.save()
		pazienteensaiokopurua = PazienteEnsaio.objects.all().count()
		self.assertEquals(pazienteensaiokopurua, 2)


class ErabiltzaileTest(TestCase):

	def test_erabiltzaile_sorkuntza(self):

		user1 = User(username='u1', password='1234', email='a@a.com')
		user1.save()

		profila1 = ErabiltzaileProfila(erabiltzailea=user1, izena='u1', abizena1='a', abizena2='a2', zerbitzua='Farmazia')
		profila1.save()
		erabiltzailekop = ErabiltzaileProfila.objects.all().count()
		self.assertEquals(erabiltzailekop, 1)

		erabiltzailesoilkopurua = User.objects.all().count()
		self.assertEquals(erabiltzailesoilkopurua, 1)
		














#Aplikazioan zehar erabiliko diren sorkuntza-formulario test-ak:

class EnsaioSorkuntzaTest(TestCase):

	def test_ensaio_sorkuntza_form(self):
		data = time.strftime('%Y-%m-%d')
		form_data = {'hasieraData':data, 'protokoloZenbakia':'protzenb1', 'titulua':'ensaioa1', 'zerbitzua':'z', 'promotorea':'p', 'estudioMota':'em', 'monitorea':'mon', 'ikertzailea':'ik'}
		form = EnsaioBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())

		form_data = {'hasieraData':data, 'titulua':'ensaioa1', 'zerbitzua':'z', 'promotorea':'p', 'estudioMota':'em', 'monitorea':'mon', 'ikertzailea':'ik'}
		form = EnsaioBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())

		form_data = {'hasieraData':data, 'protokoloZenbakia':'1', 'zerbitzua':'z', 'promotorea':'p', 'estudioMota':'em', 'monitorea':'mon', 'ikertzailea':'ik'}
		form = EnsaioBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())

		form_data = {'hasieraData':data, 'protokoloZenbakia':'1', 'titulua':'ensaioa1',  'promotorea':'p', 'estudioMota':'em', 'monitorea':'mon', 'ikertzailea':'ik'}
		form = EnsaioBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())

		form_data = {'hasieraData':data, 'protokoloZenbakia':'1', 'titulua':'ensaioa1', 'zerbitzua':'z', 'estudioMota':'em', 'monitorea':'mon', 'ikertzailea':'ik'}
		form = EnsaioBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())

		form_data = {'hasieraData':data, 'protokoloZenbakia':'1', 'titulua':'ensaioa1', 'zerbitzua':'z', 'promotorea':'p', 'monitorea':'mon', 'ikertzailea':'ik'}
		form = EnsaioBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())

		form_data = {'hasieraData':data, 'protokoloZenbakia':'1', 'titulua':'ensaioa1', 'zerbitzua':'z', 'promotorea':'p', 'estudioMota':'em',  'ikertzailea':'ik'}
		form = EnsaioBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())

		form_data = {'hasieraData':data, 'protokoloZenbakia':'1', 'titulua':'ensaioa1', 'zerbitzua':'z', 'promotorea':'p', 'estudioMota':'em', 'monitorea':'mon'}
		form = EnsaioBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())




class PazienteSorkuntzaTest(TestCase):

	def test_paziente_sorkuntza_form(self):
		form_data = {'izena':'izena', 'pisua':80}
		form = PazienteBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())

		form_data = {'pisua':80}
		form = PazienteBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())

		form_data = {'izena':'izena'}
		form = PazienteBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())


class ErrezetaSorkuntzaTest(TestCase):

	def test_errezeta_sorkuntza_form(self):
		data = time.strftime('%Y-%m-%d')
		ensaioa = Ensaioa(egoera='irekita', hasieraData=data, protokoloZenbakia='prot1', titulua='ensaioa1', zerbitzua='z', promotorea='p', estudioMota='em', monitorea='m', ikertzailea='i')
		ensaioa.save()
		pazientea = Pazientea(izena='pazientea1', pisua=90)
		pazientea.save()
		form_data = {'ensaioa':ensaioa.titulua, 'hurrengoPreskripzioData':data, 'pazientea':pazientea.ident, 'pendiente':'Pendiente', 'preskripzioData':data, 'sortzailea':'sortzailea'}
		form = ErrezetaBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())

		form_data = {'ensaioa':ensaioa.titulua, 'hurrengoPreskripzioData':data, 'pazientea':pazientea.ident, 'pendiente':'Pendiente', 'preskripzioData':data, 'sortzailea':'sortzailea'}
		form = ErrezetaBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())

		form_data = {'hurrengoPreskripzioData':data, 'pazientea':pazientea.ident, 'pendiente':'Pendiente', 'preskripzioData':data, 'sortzailea':'sortzailea'}
		form = ErrezetaBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())

		form_data = {'ensaioa':ensaioa.titulua, 'pazientea':pazientea.ident, 'pendiente':'Pendiente', 'preskripzioData':data, 'sortzailea':'sortzailea'}
		form = ErrezetaBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())

		form_data = {'ensaioa':ensaioa.titulua, 'hurrengoPreskripzioData':data, 'pazientea':pazientea.ident, 'preskripzioData':data, 'sortzailea':'sortzailea'}
		form = ErrezetaBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())

		
		form_data = {'ensaioa':ensaioa.titulua, 'hurrengoPreskripzioData':data, 'pazientea':pazientea.ident, 'pendiente':'Pendiente', 'preskripzioData':data}
		form = ErrezetaBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())


class MedikamentuSorkuntzaTest(TestCase):

	def test_medikamentu_sorkuntza_form(self):
		data = time.strftime('%Y-%m-%d')
		form_data = {'ident':'medik1', 'lote':'lotea', 'kit':1, 'kaduzitatea':data, 'bidalketaZenbakia':1, 'bidalketaData':data, 'unitateak':3}
		form = MedikamentuBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())

		form_data = {'lote':'lotea', 'kit':1, 'kaduzitatea':data, 'bidalketaZenbakia':1, 'bidalketaData':data, 'unitateak':3}
		form = MedikamentuBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())

		form_data = {'ident':'medik1', 'kit':1, 'kaduzitatea':data, 'bidalketaZenbakia':1, 'bidalketaData':data, 'unitateak':3}
		form = MedikamentuBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())

		form_data = {'ident':'medik1', 'lote':'lotea', 'kaduzitatea':data, 'bidalketaZenbakia':1, 'bidalketaData':data, 'unitateak':3}
		form = MedikamentuBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())

		form_data = {'ident':'medik1', 'lote':'lotea', 'kit':1, 'bidalketaZenbakia':1, 'bidalketaData':data, 'unitateak':3}
		form = MedikamentuBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())

		form_data = {'ident':'medik1', 'lote':'lotea', 'kit':1, 'kaduzitatea':data, 'bidalketaData':data, 'unitateak':3}
		form = MedikamentuBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())

		form_data = {'ident':'medik1', 'lote':'lotea', 'kit':1, 'kaduzitatea':data, 'bidalketaZenbakia':1, 'unitateak':3}
		form = MedikamentuBerriFormularioa(data=form_data)
		self.assertTrue(form.is_valid())

		form_data = {'ident':'medik1', 'lote':'lotea', 'kit':1, 'kaduzitatea':data, 'bidalketaZenbakia':1, 'bidalketaData':data}
		form = MedikamentuBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())


		medikamentua = Medikamentua(ident='m1', unitateak=3, kit=1, kaduzitatea=data, bidalketaZenbakia=1, bidalketaData=data)
		medikamentua.save()
		#Existitzen den gako bat duen medikamentu bat sortu
		form_data = {'ident':'m1', 'lote':'lotea', 'kit':1, 'kaduzitatea':data, 'bidalketaZenbakia':1, 'bidalketaData':data, 'unitateak':3}
		form = MedikamentuBerriFormularioa(data=form_data)
		self.assertFalse(form.is_valid())




#Testeatutako funtzioez gain, aplikazioan zehar erabiliko diren funtzionalitate garrantzitsuenen test-ak (bistak):

class EnsaioaBilatuViewTest(TestCase):

	def test_ensaioa_bilatu_view(self):

		response = self.client.post('/farmaciapp/aukera_menua/ensaio_kontsulta/ensaio_bilaketa/', {})
		#debe redirigir la respuesta a otra pagina
		self.assertEquals(response.status_code, 302)

		#response = self.client.get(reverse('ensaio_bilaketa'))
        #self.assertContains(response, "No polls are available.")
        #self.assertEquals(response.context, [])