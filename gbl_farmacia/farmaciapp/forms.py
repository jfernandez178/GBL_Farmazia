from django import forms
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget
from farmaciapp.models import Medikamentua, Pazientea, Dispentsazioa, Ensaioa, ErabiltzaileProfila, PazienteEnsaio, MedikamentuEnsaio, EnsaioErrezeta, PazienteDispentsazio





#from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget
#from functools import partial
#DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class ErabiltzaileFormularioa(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


#Hau bakarrik izango litzateke erabiltzaileak bere profila izan nahiko balu.
class ErabiltzaileProfilFormularioa(forms.ModelForm):
    class Meta:
        model = ErabiltzaileProfila
        fields = ('izena', 'abizena1', 'abizena2', 'zerbitzua')


#Ondorengo formularioa ensaio berri bat sortzeko erabiliko da
class EnsaioBerriFormularioa(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(EnsaioBerriFormularioa, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['bukaeraData'].required = False
        self.fields['hasieraData'].widget.attrs = {'class': 'vDateField'}
        self.fields['bukaeraData'].widget.attrs = {'class': 'vDateField'}
        self.fields['bukaeraData'].widget = forms.HiddenInput()
        self.fields['egoera'].widget = forms.HiddenInput()
        self.fields['egoera'].required = False


    class Meta:
		model = Ensaioa


#Ondorengo formularioa ensaioen bilaketak egiteko erabiliko da
class EnsaioBilaketaFormularioa(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(EnsaioBilaketaFormularioa, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['egoera'].required = False
        self.fields['egoera'].widget = forms.HiddenInput()
        self.fields['hasieraData'].required = False
        self.fields['bukaeraData'].widget.attrs = {'class': 'vDateField'}
        self.fields['hasieraData'].widget.attrs = {'class': 'vDateField'}
        self.fields['protokoloZenbakia'].required = False
        self.fields['titulua'].required = False
        self.fields['zerbitzua'].required = False
        self.fields['promotorea'].required = False
        self.fields['estudioMota'].required = False
        self.fields['monitorea'].required = False
        self.fields['ikertzailea'].required = False
        self.fields['komentarioak'].widget = forms.HiddenInput()



    class Meta:
        model = Ensaioa
        #widgets = {
        #    'hasieraData': SuitSplitDateTimeWidget,
        #    'bukaeraData': SuitSplitDateTimeWidget,
        #}


class EnsaioBilaketaFormularioa2(forms.ModelForm):
    #Hau da adierazteko ez direla derrigorrezkoak eremuak; hau da, hutsik jarri daitezkeela bilaketarako
    def __init__(self, *args, **kwargs):
        super(EnsaioBilaketaFormularioa2, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['ensaioa'].required = False
        self.fields['ensaioa'].widget = forms.HiddenInput()
        self.fields['pazientea'].required = False
        self.fields['pazientea'].null = True
        self.fields['ensaioa'].null = True


    class Meta:
        model = PazienteEnsaio



class MedikamentuBilaketaFormularioa(forms.ModelForm):
    #Hau da adierazteko ez direla derrigorrezkoak eremuak; hau da, hutsik jarri daitezkeela bilaketarako
    def __init__(self, *args, **kwargs):
        super(MedikamentuBilaketaFormularioa, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['ident'].required = False
        self.fields['kit'].required = False
        self.fields['lote'].required = False
        self.fields['kaduzitatea'].required = False
        self.fields['kaduzitatea'].widget.attrs = {'class': 'vDateField'}

        self.fields['bidalketaZenbakia'].required = False
        self.fields['bidalketaData'].required = False
        self.fields['bidalketaData'].widget.attrs = {'class': 'vDateField'}
        self.fields['bidalketaOrdua'].required = False
        self.fields['bidalketaOrdua'].widget.attrs = {'class': 'vTimeField'}
        self.fields['unitateak'].required = False
        self.fields['unitateak'].widget = forms.HiddenInput()

        #self.fields['ensaioa'].widget = forms.HiddenInput()
        

    class Meta:
        model = Medikamentua

class MedikamentuBilaketaFormularioa2(forms.ModelForm):
    #Hau da adierazteko ez direla derrigorrezkoak eremuak; hau da, hutsik jarri daitezkeela bilaketarako
    def __init__(self, *args, **kwargs):
        super(MedikamentuBilaketaFormularioa2, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['medikamentua'].required = False
        self.fields['ensaioa'].required = False
        self.fields['medikamentua'].widget = forms.HiddenInput()



    class Meta:
        model = MedikamentuEnsaio


class ErrezetaBerriFormularioa(forms.ModelForm):
    preskripzioData = forms.DateField(widget=forms.DateInput())
    hurrengoPreskripzioData = forms.DateField(widget=forms.DateInput())
    
    #Hau da adierazteko ez direla derrigorrezkoak eremuak; hau da, hutsik jarri daitezkeela bilaketarako
    def __init__(self, *args, **kwargs):
        super(ErrezetaBerriFormularioa, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['ensaioa'].required = True
        self.fields['pazientea'].required = False
        self.fields['preskripzioData'].required = False
        self.fields['preskripzioData'].widget.attrs = {'class': 'vDateField'}
        self.fields['hurrengoPreskripzioData'].required = False
        self.fields['hurrengoPreskripzioData'].widget.attrs = {'class': 'vDateField'}
        self.fields['pendiente'].required = False
        self.fields['pendiente'].widget = forms.HiddenInput()
        self.fields['sortzailea'].widget = forms.HiddenInput()
        self.fields['pazientea'].widget = forms.HiddenInput()
        self.fields['preskripzioData'].widget = forms.HiddenInput()
        self.fields['hurrengoPreskripzioData'].widget = forms.HiddenInput()



    class Meta:
        model = EnsaioErrezeta


class ErrezetaBerriEnsaiotikFormularioa(forms.ModelForm):

    preskripzioData = forms.DateField(widget=forms.DateInput())
    hurrengoPreskripzioData = forms.DateField(widget=forms.DateInput())
    #Hau da adierazteko ez direla derrigorrezkoak eremuak; hau da, hutsik jarri daitezkeela bilaketarako
    def __init__(self, *args, **kwargs):
        super(ErrezetaBerriEnsaiotikFormularioa, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['ensaioa'].required = False
        self.fields['pazientea'].required = True
        self.fields['preskripzioData'].required = True
        self.fields['preskripzioData'].widget.attrs = {'class': 'vDateField'}
        self.fields['hurrengoPreskripzioData'].widget.attrs = {'class': 'vDateField'}
        self.fields['hurrengoPreskripzioData'].required = False
        self.fields['pendiente'].required = False
        self.fields['pendiente'].widget = forms.HiddenInput()
        self.fields['ensaioa'].widget = forms.HiddenInput()
        self.fields['sortzailea'].widget = forms.HiddenInput()


    class Meta:
        model = EnsaioErrezeta

class DispentsazioFormularioa(forms.ModelForm):
    #Bi eremu hauek markatuko dute noiztik norako dispentsazioak ikusi nahi diren
    dataNoiztik = forms.DateField(widget=AdminDateWidget)#, id='datepicker')
    dataNoiztik.required = False
    dataNoizArte = forms.DateField(widget=AdminDateWidget)#, id='datepicker')
    dataNoizArte.required = False
    def __init__(self, *args, **kwargs):
        super(DispentsazioFormularioa, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['medikamentua'].required = False
        self.fields['dispentsazioa'].required = False
        self.fields['paziente'].required = False
        self.fields['medikamentua'].widget = forms.HiddenInput()
        self.fields['dispentsazioa'].widget = forms.HiddenInput()
        self.fields['ident'].required = False
        self.fields['ident'].widget = forms.HiddenInput()
        self.fields['dosia'].widget = forms.HiddenInput()
        self.fields['dosia'].required = False

    class Meta:
        model = PazienteDispentsazio


class MedikamentuBerriFormularioa(forms.ModelForm):
    #Eremu berriak jarriko ditut, orduaren aukeraketa errazago izan dadin
    ordua = forms.IntegerField(min_value=00, max_value=23)
    minutuak = forms.IntegerField(min_value=00, max_value=59)
    ordua.required = False
    minutuak.required = False

    def __init__(self, *args, **kwargs):
        super(MedikamentuBerriFormularioa, self).__init__(*args, **kwargs)
        # Making name required
        #self.fields['bidalketaOrdua'].widget.attrs = {'class': 'vTimeField'}
        self.fields['bidalketaOrdua'].widget = forms.HiddenInput()
        self.fields['bidalketaData'].widget.attrs = {'class': 'vDateField'}
        self.fields['kaduzitatea'].widget.attrs = {'class': 'vDateField'}
        self.fields['kit'].required = True



    class Meta:
        model = Medikamentua


class ErrezetaModifikatuFormularioa(forms.ModelForm):

    preskripzioData = forms.DateField(widget=forms.DateInput())
    hurrengoPreskripzioData = forms.DateField(widget=forms.DateInput())
    pazientearen_pisua = forms.FloatField()
    #Hau da adierazteko ez direla derrigorrezkoak eremuak; hau da, hutsik jarri daitezkeela bilaketarako
    def __init__(self, *args, **kwargs):
        super(ErrezetaModifikatuFormularioa, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['ensaioa'].required = False
        self.fields['pazientea'].required = True
        self.fields['preskripzioData'].required = True
        self.fields['preskripzioData'].widget.attrs = {'class': 'vDateField'}
        self.fields['hurrengoPreskripzioData'].required = False
        self.fields['hurrengoPreskripzioData'].widget.attrs = {'class': 'vDateField'}
        self.fields['pendiente'].required = False
        self.fields['pendiente'].widget = forms.HiddenInput()
        self.fields['ensaioa'].widget = forms.HiddenInput()
        self.fields['sortzailea'].widget = forms.HiddenInput()


    class Meta:
        model = EnsaioErrezeta


class PazienteBerriFormularioa(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PazienteBerriFormularioa, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['idensaioan'].required = False
        self.fields['idensaioan'].widget = forms.HiddenInput()



    class Meta:
        model = Pazientea