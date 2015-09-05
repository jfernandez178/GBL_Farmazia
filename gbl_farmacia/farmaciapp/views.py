from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from farmaciapp.forms import ErabiltzaileFormularioa, ErabiltzaileProfilFormularioa, EnsaioBerriFormularioa, EnsaioBilaketaFormularioa, EnsaioBilaketaFormularioa2, MedikamentuBilaketaFormularioa, MedikamentuBilaketaFormularioa2, Medikamentua, ErrezetaBerriFormularioa, DispentsazioFormularioa, ErrezetaBerriEnsaiotikFormularioa, MedikamentuBerriFormularioa, ErrezetaModifikatuFormularioa, PazienteBerriFormularioa
from farmaciapp.models import Ensaioa, ErabiltzaileProfila, PazienteEnsaio, Pazientea, EnsaioErrezeta, MedikamentuEnsaio, Dispentsazioa, PazienteDispentsazio
from django.db.models import Q, Sum
from django.contrib.auth.models import User
import datetime
from dateutil import parser
import time

from random import randint
import sys


#PDF dokumentuen sorrerarako beharrezkoak
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO

#Orrialde nagusia
def index(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/farmaciapp/aukera_menua/')
    else:
        # Hiztegi bat pasatzen da ereduari pasatzeko mezu bezala
        context_dict = {'boldmessage': "Farmaciapp Orrialde Nagusian zaude!"}

        # Jasotako emaitza pasatzen zaio, bezeroari erakusteko
        return render(request, 'farmaciapp/index.html', context_dict)
   

#Erabitzaile bat erregistratzeko erabiliko den interfazearen logika adierazten du
def erregistratu(request):

    #Erregistratu den edo ez adieraziko duen aldagaia
    erregistratuta = False

    if request.method == 'POST':
        #Formularioko parametroak jasotzen dira
        erabiltzaile_form = ErabiltzaileFormularioa(data=request.POST)
        erabiltzaile_profil_form = ErabiltzaileProfilFormularioa(data=request.POST)



        #Bi formularioak zuzenak badira konprobatzen da
        if erabiltzaile_form.is_valid() and erabiltzaile_profil_form.is_valid():
            # Erabiltzailearen informazioa gordetzen da datu-basean
            erabiltzailea = erabiltzaile_form.save()

            #Pasahitza hash bidez kodetu eta berriz gordetzen da
            erabiltzailea.set_password(erabiltzailea.password)
            erabiltzailea.save()

            #Erabiltzailearen profila ere gordetzen da
            profila = erabiltzaile_profil_form.save(commit=False)
            profila.erabiltzailea = erabiltzailea

            #Konprobatzen da ea erabiltzailea autentikatuta dagoen
            #Baiezko kasuan, administratzaileak beste erabiltzaile bat sortu nahi duela adierazten da
            if request.user.is_authenticated():
                if 'admin' in request.POST:
                    #checkbox-a markatu badu
                    #Administratzaile rola eman behar zaio
                    profila.zerbitzua = 'admin'

            #Profila gordetzen da
            profila.save()

            #Erregistratu dela adierazten duen aldagaia
            erregistratuta = True

        #Formularioaren betetzea ez baldin bada zuzena izan errore mezua erakutsiko da
        else:
            print erabiltzaile_form.errors, erabiltzaile_profil_form.errors

    #Ez bada POST eskaera bat
    else:
        erabiltzaile_form = ErabiltzaileFormularioa()
        erabiltzaile_profil_form = ErabiltzaileProfilFormularioa()

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request,
            'farmaciapp/erregistratu.html',
            {'pendienteak':errezeta_pendienteak.count, 'erabiltzaile_form': erabiltzaile_form, 'erabiltzaile_profil_form': erabiltzaile_profil_form, 'erregistratuta': erregistratuta} )


#Erabiltzaileak login egiteko beharreko bista
def erabiltzailea_login(request):

    #POST bada erabilitako HTTP metodoa
    if request.method == 'POST':
        #Erabitzailearen erabiltzaile-izena eta pasahitza jasotzen dira eskaeratik
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Django-k konprobatzen du ea autentikazioa zuzena den
        user = authenticate(username=username, password=password)

        #Erabiltzaile objektua zuzena bada, ongi hasi du sesioa
        if user:
            #Kontua irekita badago
            if user.is_active:
                #Sesioa hasterakoan erabiltzailearen menu nagusira eramango zaio erabiltzaileari
                login(request, user)
                return HttpResponseRedirect('/farmaciapp/aukera_menua/')
            else:
                #Kontua ez badago aktibatuta
                return HttpResponse("Zure kontua desgaituta dago...")
        else:
            #Ez badu ongi hasi sesioa
            print "Sesio-irekiera desegokia: {0}, {1}".format(username, password)
            return HttpResponse("Erabiltzailea edo pasahitza ez dira egokiak!<br/><br/><a href='/farmaciapp/login/'>Atzera</a>")

   #Ez bada POST eskaera bat
    else:
        
        return render(request, 'farmaciapp/login.html', {})


#Etiketa hau erabiltzen da adierazteko, aukera hau erabiltzaileak sesioa irekita duenean bakarrik egongo dela ikusgai
@login_required
def erabiltzailea_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/farmaciapp/')


@login_required
def aukera_menua(request):
    #Erbailtzaile mota konprobatu behar da
        #Farmazia zerbitzukoa bada, orrialde mota bat erakutsiko da
        #Ez bada Farmazia zerbitzukoa, beste bat

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(Q(erabiltzailea=request.user))[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'


    #Aukera menura eramango gaitu
    return render(request, 'farmaciapp/aukera_menua.html', {'pendienteak':errezeta_pendienteak.count, 'farmazia':farmazia, 'mota':erabiltzaile_mota, 'admin':admin})



@login_required
def ensaioak_kontsultatu_botoia(request):
    

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(Q(erabiltzailea=request.user))[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    # Honek eramango gaitu ensaioen kontsulta kudeatuko duen orrialdera
    return render(request, 'farmaciapp/ensaio_menua.html', {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'farmazia':farmazia, 'mota':erabiltzaile_mota})



@login_required
def ensaioak_bilatu(request):
    
    #kodearen inplementaziorako lagunduko duten aldagai laguntzaileak
    pazientea_id = ''
    pazientea = ''
    ensaio_bilaketa_form2 = []
    pazientea_duten_ensaioak = []

    #Zein datatatik eta zein dataraino bilatu nahi den atributuak zehaztu diren edo ez adierazten duten aldagaiak
    flagNoiztik = False
    flagNoizarte = False

    #zenbat ensaio aurkitu diren adierazten duen aldagaia
    zenbat_ensaio = 0

    #Pazientearen arabera bilatu nahi izan bada
    if 'pazientea' in request.POST:
        pazientea_id = request.POST['pazientea']
        try:
            #Definitutako Pazientea existitzen bada
            pazientea = Pazientea.objects.get(ident=pazientea_id)
        except:
            #Ez baldin bada existitzen pazientea ez dela definitu jakina da
            pazientea_id = -1
            pazientea = None

    #Honek eramango gaitu errezetaren sorkuntza kudeatuko duen orrialdera
    if request.method == 'POST':
        ensaio_bilaketa_form = EnsaioBilaketaFormularioa(data=request.POST)
        ensaio_bilaketa_form2 = EnsaioBilaketaFormularioa2(data=request.POST)

        # Baldintza hauek betetzen baldin badira, zuzena da informazio bidalketa
        if ((ensaio_bilaketa_form.is_valid() or request.POST['titulua'] != '') and ensaio_bilaketa_form2.is_valid()):
           
            if(pazientea!=None):

                #Medicina arlokoa bada, bakarrik bere azpizerbitzuko ensaioak ikusi ahalko ditu
                erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0]
                
                if erabiltzaile_mota.zerbitzua == 'Medicina':

                    #Bilaketak egiteko flag hauek erabiliko ditugu, jakiteko erbailtzaileak zein aukera hautatu dituen bilaketarako
                    if(request.POST['hasieraData']!=''):
                        flagNoiztik = True

                    if(request.POST['bukaeraData']!=''):
                        flagNoizarte = True

                    if (flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)


                    if (not flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)

                    
                    if (flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)

                    
                    if (not flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)

                else:

                    #Bilaketak egiteko flag hauek erabiliko ditugu, jakiteko erbailtzaileak zein aukera hautatu dituen bilaketarako
                    if(request.POST['hasieraData']!=''):
                        flagNoiztik = True

                    if(request.POST['bukaeraData']!=''):
                        flagNoizarte = True

                    if (flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)


                    if (not flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)

                    
                    if (flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)

                    
                    if (not flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)



            else:
                #Medicina arlokoa bada, bakarrik bere azpizerbitzuko ensaioak ikusi ahalko ditu
                erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0]
                if erabiltzaile_mota.zerbitzua == 'Medicina':


                    #Bilaketak egiteko flag hauek erabiliko ditugu, jakiteko erbailtzaileak zein aukera hautatu dituen bilaketarako
                    if(request.POST['hasieraData']!=''):
                        flagNoiztik = True

                    if(request.POST['bukaeraData']!=''):
                        flagNoizarte = True

                    if (flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)


                    if (not flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)

                    
                    if (flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)

                    
                    if (not flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua=erabiltzaile_mota.azpizerbitzua) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)


                else:


                    #Bilaketak egiteko flag hauek erabiliko ditugu, jakiteko erbailtzaileak zein aukera hautatu dituen bilaketarako
                    if(request.POST['hasieraData']!=''):
                        flagNoiztik = True

                    if(request.POST['bukaeraData']!=''):
                        flagNoizarte = True

                    if (flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)


                    if (not flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(bukaeraData_lte=request.POST['bukaeraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)

                    
                    if (flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__gte=request.POST['hasieraData']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)

                    
                    if (not flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(egoera='irekita'))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                        zenbat_ensaio = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(egoera='irekita')).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)


  
        else:
            bilaketa_emaitzak = []

    else:
        ensaio_bilaketa_form = EnsaioBilaketaFormularioa()
        ensaio_bilaketa_form2 = EnsaioBilaketaFormularioa2()
        bilaketa_emaitzak = []
       

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request,
            'farmaciapp/ensaioak_bilatu.html',
            {'zenbatEnsaio':zenbat_ensaio, 'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'pazientea_id': pazientea_id, 'pazientea': pazientea, 'bilaketa_emaitzak': bilaketa_emaitzak, 'ensaio_bilaketa_form': ensaio_bilaketa_form, 'ensaio_bilaketa_form2': ensaio_bilaketa_form2, 'pazientea_duten_ensaioak': pazientea_duten_ensaioak} )
    

@login_required
def ensaioa_sortu(request):

    #Ensaioa sortu den edo ez adieraziko duen aldagaia
    sortuta = False
    ensaioa_titulua = ''
    
    if request.method == 'POST':
        ensaio_form = EnsaioBerriFormularioa(data=request.POST)

        #Ensaioa sortzeko beharrezko eremuak bete badira

        if ensaio_form.is_valid():

            #Falta diren eremuak bete eta ensaioaren informazia gordetzen da
            ensaioa = ensaio_form.save(commit=False)
            ensaioa.egoera = 'irekita'
            ensaioa_titulua = request.POST['protokoloZenbakia']

            ensaioa.save()
            
            sortuta = True

       
        else:
            print ensaio_form.errors

    else:
        ensaio_form = EnsaioBerriFormularioa()

    

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))



    return render(request,
            'farmaciapp/ensaioa_sortu.html',
            {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'ensaio_form': ensaio_form, 'sortuta': sortuta, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'ensaioa_titulua':ensaioa_titulua} )



def ensaioa_info(request, ensaioa_protokolo_zenb):

    #Ensaioaren informazioa eskuratzen da
    context_dict = {}
    context_dict['egoera'] = None
    context_dict['hasieraData'] = None
    context_dict['bukaeraData'] = None
    context_dict['protokoloZenbakia'] = None
    context_dict['titulua'] = None
    context_dict['zerbitzua'] = None
    context_dict['promotorea'] = None
    context_dict['estudioMota'] = None
    context_dict['monitoreaTel'] = None
    context_dict['monitoreaFax'] = None
    context_dict['monitoreaMugikor'] = None
    context_dict['monitoreaEmail'] = None
    context_dict['monitorea'] = None
    context_dict['ikertzailea'] = None
    context_dict['komentarioak'] = None
    context_dict['medikamentuak'] = None


    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    context_dict['mota'] = erabiltzaile_mota
    context_dict['farmazia'] = farmazia
    context_dict['admin'] = 'admin'
      
    try:

        ensaioa = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)
        context_dict['egoera'] = ensaioa.egoera
        context_dict['hasieraData'] = ensaioa.hasieraData
        context_dict['bukaeraData'] = ensaioa.bukaeraData
        context_dict['protokoloZenbakia'] = ensaioa.protokoloZenbakia
        context_dict['titulua'] = ensaioa.titulua
        context_dict['zerbitzua'] = ensaioa.zerbitzua
        context_dict['promotorea'] = ensaioa.promotorea
        context_dict['estudioMota'] = ensaioa.estudioMota
        context_dict['monitoreaTel'] = ensaioa.monitoreaTel
        context_dict['monitoreaFax'] = ensaioa.monitoreaFax
        context_dict['monitoreaMugikor'] = ensaioa.monitoreaMugikor
        context_dict['monitoreaEmail'] = ensaioa.monitoreaEmail
        context_dict['monitorea'] = ensaioa.monitorea
        context_dict['ikertzailea'] = ensaioa.ikertzailea
        context_dict['komentarioak'] = ensaioa.komentarioak

        #zeintzuk medikamentu dituen agertuko da lehenik
        ensaioa = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)
        medikamentuen_lista = MedikamentuEnsaio.objects.filter(Q(ensaioa=ensaioa))#.values('medikamentua').distinct()
        context_dict['medikamentuak'] = medikamentuen_lista

    except Ensaioa.DoesNotExist:
        pass

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))
    context_dict['pendienteak'] = errezeta_pendienteak.count
   
    return render(request, 'farmaciapp/ensaioa_info_especial.html', context_dict)




@login_required
def dispentsazioak_aztertu(request, ensaioa_protokolo_zenb):
    #Ensaioaren dispentsazioak aztertuko dira

    #Aldagai laguntzaileak
    flagNoizarte = False
    flagNoiztik = False
    flagPazientea = False
    bilaketa_emaitzak = []
    pazienteaEnsaioan = None
    paziente_id="ezebez"
    noiztik = ''
    noizarte = ''
    pazienteidreal = ''


    if request.method == 'POST':
        
        dispentsazio_form = DispentsazioFormularioa(data=request.POST, ensaioa_protokolo_zenb=ensaioa_protokolo_zenb)

        #Formularioko datuak zuzenak badira 
        if (dispentsazio_form.is_valid() and 'dataNoiztik' in request.POST):
            paziente_id = None
            pazienteidreal = request.POST['paziente']
            noiztik = request.POST['dataNoiztik']
            noizarte = request.POST['dataNoizArte']
            
            #Lehenengo, ensaio horretan dauden dispentsazio guztiak lortzen dira, gero, pazientearekiko filtratzeko
            dispentsazioak_ensaioan = Dispentsazioa.objects.filter(Q(ensaioa__protokoloZenbakia=ensaioa_protokolo_zenb))
                
            #Lehenik, paziente konkretu bat aukeratu duen edo ez ikusi behar da
            if 'paziente' in request.POST:
                paziente_id = request.POST['paziente']

                if len(paziente_id)>0:
                    #paziente konkretu bat bat espezifikatu baldin bada
                    paziente_id = request.POST['paziente']
                else:
                    #ez bada paziente konkreturik espezifikatu
                    paziente_id = -1
                    


            #Bilaketak egiteko flag hauek erabiliko ditugu, jakiteko erbailtzaileak zein aukera hautatu dituen bilaketarako
            if(request.POST['dataNoiztik']!=''):
                flagNoiztik = True

            if(request.POST['dataNoizArte']!=''):
                flagNoizarte = True

            #Paziente konkretu bat espezifikatu baldin bada
            if paziente_id != -1:
            
                if (flagNoiztik and flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik']) and Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte']) and Q(paziente__ident=paziente_id)).distinct()
                
                if (not flagNoiztik and flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte']) and Q(paziente__ident=paziente_id)).distinct()
                
                if (flagNoiztik and not flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik']) and Q(paziente__ident=paziente_id)).distinct()
                
                if (not flagNoiztik and not flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(paziente__ident=paziente_id)).distinct()
                    flag = pazienteaEnsaioan
            
            else:

                if (flagNoiztik and flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik']) and Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte'])).distinct()

                if (not flagNoiztik and flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte'])).distinct()

                if (flagNoiztik and not flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik'])).distinct()

                if (not flagNoiztik and not flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan)).distinct()
                    flag = pazienteaEnsaioan

  
        else:
            bilaketa_emaitzak = []
            print dispentsazio_form.errors


    else:
        dispentsazio_form = DispentsazioFormularioa(ensaioa_protokolo_zenb=ensaioa_protokolo_zenb)
        bilaketa_emaitzak = []


    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(Q(erabiltzailea=request.user))[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    #Honek eramango gaitu medikamentuen bilaketa emaitza erakutsiko duen orrialdera
    return render(request,
            'farmaciapp/dispentsazioak_aztertu.html',
            {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'farmazia':farmazia, 'mota':erabiltzaile_mota, 'pazienteidreal':pazienteidreal, 'noiztik': noiztik, 'noizarte': noizarte, 'paziente_id': paziente_id, 'pazientea': pazienteaEnsaioan, 'ensaioa': ensaioa_protokolo_zenb, 'bilaketa_emaitzak': bilaketa_emaitzak, 'dispentsazio_form': dispentsazio_form, 'ensaioa_titulua':ensaioa_protokolo_zenb} )
  


@login_required
def dispentsazioa_info(request, ensaioa_protokolo_zenb, dispentsazioa_ident):

    #Hemen dispentsazioaren informazioa ikusi ahalko da
    context_dict = {}
    ensaioa_titulua = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb).titulua
    context_dict['dispentsazioa'] = dispentsazioa_ident
    context_dict['ensaioa'] = ensaioa_titulua
    context_dict['protokoloZenbakia'] = ensaioa_protokolo_zenb
    context_dict['dispentsatzailea'] = None

    context_dict['medikamentuen_informazioa'] = None    
    context_dict['bukaeraData'] = None
    context_dict['pazientea'] = None
    context_dict['farmazia'] = 'Farmazia'
    context_dict['mota'] = ErabiltzaileProfila.objects.filter(Q(erabiltzailea=request.user))[0].zerbitzua
    context_dict['admin'] = 'admin'
    context_dict['gainontzekoEremuak'] = None

    context_dict['errezetaIzena'] = None
    
    
      
    try:
        paz_dis = PazienteDispentsazio.objects.filter(dispentsazioa__ident=dispentsazioa_ident)
        paziente_id = paz_dis[0].paziente

        #Dispentsatu diren medikamentuak eskuratuko ditugu
        paziente_dispentsazioak = PazienteDispentsazio.objects.filter(dispentsazioa__ident=dispentsazioa_ident, paziente=paziente_id)
        context_dict['medikamentuen_informazioa'] = paziente_dispentsazioak
        context_dict['dispentsazioa'] = dispentsazioa_ident
        context_dict['ensaioa'] = ensaioa_titulua
        context_dict['bukaeraData'] = Dispentsazioa.objects.get(ident=dispentsazioa_ident).bukaeraData
        context_dict['pazientea'] = paziente_id
        context_dict['dispentsatzailea'] = Dispentsazioa.objects.get(ident=dispentsazioa_ident).dispentsatzailea
       
        errezeta = EnsaioErrezeta.objects.get(ident=Dispentsazioa.objects.get(ident=dispentsazioa_ident).ensaioerrezeta)
        context_dict['gainontzekoEremuak'] = errezeta.gainontzekoEremuak
        context_dict['errezetaIzena'] = errezeta.errezetaIzena
        

    except PazienteDispentsazio.DoesNotExist:
        pass

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))
    context_dict['pendienteak'] = errezeta_pendienteak.count
   
    return render(request, 'farmaciapp/dispentsazioa_info.html', context_dict)




@login_required
def errezeta_sortu_ensaiotik(request, ensaioa_protokolo_zenb):
    
    #Errezeta sortu den edo ez jakiteko erabiliko den aldagaia
    sortuta = False

    #Zein mezu pantailaratuko den definitzeko balio duen aldagaia
    mezua = ''
    if request.method == 'POST':
        errezeta_form = ErrezetaBerriEnsaiotikFormularioa(data=request.POST, ensaioa_protokolo_zenb=ensaioa_protokolo_zenb)
        #Formularioa zuzen bete baldin bada
        if errezeta_form.is_valid():
            #Bilatu behar da ea ensaio horrentzako errezeta hori sortuta dagoen, berdina ez sortzeko
            ensaioa = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)

            pazientea = Pazientea.objects.get(ident=request.POST['pazientea'])
            try:
                ensaioerrezeta = EnsaioErrezeta.objects.get(ensaioa=ensaioa, pazientea=pazientea, preskripzioData=request.POST['preskripzioData'], hurrengoPreskripzioData=request.POST['hurrengoPreskripzioData'])
                mezua = 'Errezeta hori sortuta dago!'
            except:
                errezeta = errezeta_form.save(commit=False)
                errezeta.ensaioa = ensaioa
                errezeta.pendiente = 'Pendiente'
                errezeta.sortzailea = request.user
                errezeta.errezetaIzena = ensaioa.protokoloZenbakia + "-" + pazientea.idensaioan
                errezeta.save()

                #Errezeta sortu dela adierazten duen aldagaia eguneratzen da
                sortuta = True

        
        else:
            print errezeta_form.errors

    else:
        errezeta_form = ErrezetaBerriEnsaiotikFormularioa(ensaioa_protokolo_zenb=ensaioa_protokolo_zenb)
   

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(Q(erabiltzailea=request.user))[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

   
    return render(request,
            'farmaciapp/errezeta_ensaiotik.html',
            {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'sortuta': sortuta, 'mezua':mezua, 'errezeta_form': errezeta_form, 'sortuta': sortuta, 'titulua':ensaioa_protokolo_zenb})#, 'mota':erabiltzaile_mota, 'farmazia':farmazia} )




@login_required
def errezeta_sortu_ensaiotik_botoia(request, ensaioa_protokolo_zenb):
 
    #Ensaioa sortzeko formularioaren orrialdea erakutsiko da

    #Aldagai hau erabiliko da kontrolatzeko zein orrialdetara joan "atzera" aukera ematerakoan
    eratorpena = 'errezeta_info'

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(Q(erabiltzailea=request.user))[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    #Errezetako pazienteen zerrenda egiteko erabiliko da

    errezeta_form = ErrezetaBerriEnsaiotikFormularioa(ensaioa_protokolo_zenb=ensaioa_protokolo_zenb)


    return render(request, 'farmaciapp/errezeta_ensaiotik.html', {'pendienteak':errezeta_pendienteak.count, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'admin':admin, 'eratorpena':eratorpena, 'errezeta_form':errezeta_form, 'titulua':ensaioa_protokolo_zenb})


@login_required
def medikamentua_ezabatu(request, medikamentua_identKodetua):
    
    #Medikamentua ezabatuko da bai Stock-etik eta bai erlazionatuta dagoen ensaio eta errezetetatik
    medikamentua = Medikamentua.objects.get(identKodetua=medikamentua_identKodetua)
    medikamentua.delete()

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    context_dict = {}
    context_dict['mota'] = erabiltzaile_mota
    context_dict['farmazia'] = farmazia
    context_dict['admin'] = 'admin'
    context_dict['ezabatuta'] = True

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))
    context_dict['pendienteak'] = errezeta_pendienteak.count


    return render(request, 'farmaciapp/medikamentua_info.html', context_dict)






@login_required
def medikamentua_kendu_ensaiotik(request, ensaioa_protokolo_zenb, medikamentua_identKodetua):
    
    #Medikamentua kenduko da ensaiotik, baina Stock-ean mantenduko da
    medikamentua = MedikamentuEnsaio.objects.get(medikamentua__identKodetua=medikamentua_identKodetua)
    medikamentua.delete()

    #zeintzuk medikamentu dituen agertuko da lehenik
    ensaioa = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)
    medikamentuen_lista = MedikamentuEnsaio.objects.filter(Q(ensaioa=ensaioa))#.values('medikamentua').distinct()
    
    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'
    mezua = 'Medikamentua ondo ezabatu da'
    medikamentua_form = MedikamentuBerriFormularioa()

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    #Ensaioari medikamentuak gehitzeaz arduratuko den orrialdera eramango gaitu
    return render(request, 'farmaciapp/medikamentuak_gehitu_ensaioari.html', {'pendienteak':errezeta_pendienteak.count, 'mezua':mezua, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'medikamentua_form':medikamentua_form, 'medikamentuen_lista': medikamentuen_lista, 'titulua':ensaioa_protokolo_zenb})

@login_required
def ensaioaren_medikamentu_dispentsazio_info(request, ensaioa_protokolo_zenb, medikamentua_identKodetua):

    #Medikamentu horren dispentsazioen informazioa agertuko da
    
    #Ensaio horren gaineko eta medikamentu horren gaineko dispentsazioak lortzen dira
    medikamentuaren_ensaioaren_dispentsazioak = Dispentsazioa.objects.filter(Q(ensaioa__protokoloZenbakia=ensaioa_protokolo_zenb) & Q(dispentsazioa_pazientearekiko__medikamentua=medikamentua_identKodetua))

    #Eman diren dosi totalak kalkulatuko dira
    dosiak_dict = PazienteDispentsazio.objects.filter(Q(dispentsazioa__ensaioa__protokoloZenbakia=ensaioa_protokolo_zenb) & Q(medikamentua__identKodetua=medikamentua_identKodetua)).aggregate(Sum('dosia'))
    dosiak = dosiak_dict['dosia__sum']

    #Zenbat dauden kalkulatuko da
    medikamentua = Medikamentua.objects.get(identKodetua=medikamentua_identKodetua)

    unitate_totalak = medikamentua.unitateak_historikoa

    #zein pazienteri egin zaien dispentsazioak gordeko da
    pazienteak = PazienteDispentsazio.objects.filter(Q(dispentsazioa__ensaioa__protokoloZenbakia=ensaioa_protokolo_zenb) & Q(medikamentua__identKodetua=medikamentua_identKodetua))


    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    ensaioa_titulua = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    medikamentua = Medikamentua.objects.get(identKodetua=medikamentua_identKodetua)



    return render(request, 'farmaciapp/ensaioaren_medikamentu_dispentsazio_info.html', {'pazienteak':pazienteak, 'dosiak':dosiak, 'unitate_totalak':unitate_totalak, 'medikamentua':medikamentua, 'titulua':ensaioa_titulua, 'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'bilaketa_emaitzak':medikamentuaren_ensaioaren_dispentsazioak})


@login_required
def ensaioaren_medikamentuak_aztertu(request, ensaioa_protokolo_zenb):

    #Ensaioari esleituta dauden medikamentuen zerrenda pantailaratuko da
    bilaketa_emaitzak = Medikamentua.objects.filter(Q(medikamentua_ensaioan__ensaioa__protokoloZenbakia=ensaioa_protokolo_zenb))

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #Aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    ensaioa_titulua = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    #Ensaioari medikamentuak gehitzeaz arduratuko den orrialdera eramango gaitu
    return render(request, 'farmaciapp/ensaioaren_medikamentu_orria.html', {'protokoloZenbakia':ensaioa_protokolo_zenb, 'titulua':ensaioa_titulua, 'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'bilaketa_emaitzak':bilaketa_emaitzak})





@login_required
def medikamentuak_gehitu_ensaioari_botoia(request, ensaioa_protokolo_zenb):

    #aldagai laguntzaileak
    mezua = ''

    medikamentua_form = MedikamentuBerriFormularioa()
    
    #Behintzat medikamentuaren titulua espezifikatzen bada, medikamentuaren gehikuntza tratatuko da
    if(request.method == 'POST'):
        
        if(request.POST['ident']!=''):
            
            medikamentua_form = MedikamentuBerriFormularioa(data=request.POST)

            #Betetako formularioa zuzena bada
            if medikamentua_form.is_valid():
               
                if request.POST['ident'] != '':
                    
                    try:
                        #Medikamentua existitzen bada, informazioa eguneratuko zaio
                        medikamentua_konprobatu = Medikamentua.objects.get(ident=request.POST['ident'])
                        zenbat_unitate = int(medikamentua_konprobatu.unitateak)
                        mezua = zenbat_unitate
                        zenbat_unitate = zenbat_unitate + int(request.POST['unitateak'])
                        mezua = zenbat_unitate
                        medikamentua_konprobatu.unitateak = zenbat_unitate

                        #medikamentuak izan dituen unitateen historikoa eguneratzen da
                        unitate_totalak = int(medikamentua_konprobatu.unitateak_historikoa) + int(request.POST['unitateak'])
                        medikamentua_konprobatu.unitateak_historikoa = unitate_totalak
                        
                        #Orain konprobatzen da ea erabiltzaileak ordua espezifikatu duen edo ez
                        if request.POST['ordua'] != '' and request.POST['minutuak'] != '':
                            #Ordua espezifikatu badu
                            ordua = request.POST['ordua']
                            minutuak = request.POST['minutuak']
                            ordu_berria_string = ordua + ':' + minutuak
                            bidalketa_ordu_berria = parser.parse(ordu_berria_string).date()
                            bidalketa_ordu_berria = bidalketa_ordu_berria.strftime('%H:%M')

                            medikamentua_konprobatu.bidalketaOrdua = bidalketa_ordu_berria

                        medikamentua_konprobatu.save()
                    except:
                        #Medikamentua ez bada existitzen, medikamentu berria erregistratuko da

                        medikamentua = medikamentua_form.save(commit=False)

                        #identKodetua zenbaki bat izango da, random bidez lortua, baina bakarra izango dena
                        idkod = randint(0,sys.maxint)
                        baliozkoa = False
                        while not baliozkoa:
                            try:
                                medikamentua_existitzen_da = Medikamentua.objects.get(identKodetua=idkod)
                                idkod = randint(0, sys.maxint)
                            except:
                                baliozkoa = True

                        #behin aurkitu dela balio duen zenbaki bat, medikamentuari esleituko zaio zenbaki hori
                        medikamentua.identKodetua = idkod

                        #medikamentuak izan dituen unitateen historikoa eguneratzen da
                        unitate_totalak = int(request.POST['unitateak'])
                        medikamentua.unitateak_historikoa = unitate_totalak
                        
                        #Orain konprobatzen da ea erabiltzaileak ordua espezifikatu duen edo ez
                        if request.POST['ordua'] != '' and request.POST['minutuak'] != '':
                            #Ordua espezifikatu badu
                            ordua = request.POST['ordua']
                            minutuak = request.POST['minutuak']
                            ordu_berria_string = ordua + ':' + minutuak
                            bidalketa_ordu_berria = parser.parse(ordu_berria_string).date()
                            bidalketa_ordu_berria = bidalketa_ordu_berria.strftime('%H:%M')

                            medikamentua.bidalketaOrdua = bidalketa_ordu_berria

                        medikamentua.save()

                        #Orain medikamentuEnsaio modeloaren instantzia bat sortu behar da, erlazioa egiteko
                        ensaioa = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)
                        medikamentuEnsaio = MedikamentuEnsaio(medikamentua=medikamentua, ensaioa=ensaioa)
                        medikamentuEnsaio.save()
                        mezua = 'Medikamentua gehitu da ensaioan'

                
                    #Medikamentua ondo gehitu dela adierazten da 
                    sortuta = True

            else:
               

                medikamentua_konprobatu = Medikamentua.objects.get(ident=request.POST['ident'])

                #Ensaio horrek medikamentu hau daukan konprobatzen da
                try:
                    ensaioa_titulua = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb).titulua
                    ensaioak_badu_medikamentua = MedikamentuEnsaio.objects.get(ensaioa=ensaioa_titulua, medikamentua=request.POST['ident'])
                except:
                    #Ez badauka medikamentu hau, gehitu egin behar zaio
                    ensaioa = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)
                    
                    ensaioak_badu_medikamentua = MedikamentuEnsaio(ensaioa=ensaioa, medikamentua=medikamentua_konprobatu)
                    ensaioak_badu_medikamentua.save()

                    
                zenbat_unitate = int(medikamentua_konprobatu.unitateak)
                
                zenbat_unitate = zenbat_unitate + int(request.POST['unitateak'])
                
                medikamentua_konprobatu.unitateak = zenbat_unitate

                #medikamentuak izan dituen unitateen historikoa eguneratzen da
                unitate_totalak = int(medikamentua_konprobatu.unitateak_historikoa) + int(request.POST['unitateak'])
                medikamentua_konprobatu.unitateak_historikoa = unitate_totalak
                        


                #Orain konprobatzen da ea erabiltzaileak ordua espezifikatu duen edo ez
                if request.POST['ordua'] != '' and request.POST['minutuak'] != '':
                    #Ordua espezifikatu badu
                    ordua = request.POST['ordua']
                    minutuak = request.POST['minutuak']
                    ordu_berria_string = ordua + ':' + minutuak
                    bidalketa_ordu_berria = parser.parse(ordu_berria_string).date()
                    bidalketa_ordu_berria = bidalketa_ordu_berria.strftime('%H:%M')
                    medikamentua_konprobatu.bidalketaOrdua = bidalketa_ordu_berria
                            
                medikamentua_konprobatu.save()

                mezua = 'Medikamentuaren informazioa eguneratu da'



                
    #Lehen aldia bada, eta ez bada espezifikatu titulorik, formularioa erakutsi beharko da orrialdean
    else:
        medikamentua_form = MedikamentuBerriFormularioa()

    #zeintzuk medikamentu dituen agertuko da lehenik
    ensaioa = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)
    medikamentuen_lista = MedikamentuEnsaio.objects.filter(Q(ensaioa=ensaioa))#.values('medikamentua').distinct()
    
    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    #Ensaioari medikamentuak gehitzeaz arduratuko den orrialdera eramango gaitu
    return render(request, 'farmaciapp/medikamentuak_gehitu_ensaioari.html', {'pendienteak':errezeta_pendienteak.count, 'mezua':mezua, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'medikamentua_form':medikamentua_form, 'medikamentuen_lista': medikamentuen_lista, 'titulua':ensaioa_protokolo_zenb})





@login_required
def ensaioen_historikoa_ikusi_botoia(request):
    #Honek eramango gaitu ensaioen historikoa erakutsiko duen orrialdera

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    ensaio_bilaketa_form = EnsaioBilaketaFormularioa()
    ensaio_bilaketa_form2 = EnsaioBilaketaFormularioa2()

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request, 'farmaciapp/ensaioen_historikoa.html', {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'ensaio_bilaketa_form2':ensaio_bilaketa_form2, 'ensaio_bilaketa_form':ensaio_bilaketa_form, 'mota':erabiltzaile_mota, 'farmazia':farmazia})


@login_required
def ensaioen_historikoa_ikusi(request):

    #Hemen lortuko da bilaketa filtroetatik lotutako emaitza
    bilaketa_emaitzak = []

    #Jakiteko zenbat ensaio dauden
    zenbat_ensaio = 0

    if request.method == 'POST':

        ensaio_bilaketa_form = EnsaioBilaketaFormularioa(data=request.POST)
        ensaio_bilaketa_form2 = EnsaioBilaketaFormularioa2(data=request.POST)

        if 'pazientea' in request.POST:
            pazientea_id = request.POST['pazientea']
            try:
                pazientea = Pazientea.objects.get(ident=pazientea_id)
            except:
                pazientea_id = -1
                pazientea = None

        #Bidalitako informazioa zuzena bada
        if ((ensaio_bilaketa_form.is_valid() or request.POST['titulua'] != '') and ensaio_bilaketa_form2.is_valid()):
           
            if(pazientea!=None):

                bilaketa_emaitzak = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__icontains=request.POST['hasieraData']) & Q(egoera='itxita') & Q(monitorea__icontains=request.POST['monitorea']))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                zenbat_ensaio = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__icontains=request.POST['hasieraData']) & Q(egoera='itxita') & Q(monitorea__icontains=request.POST['monitorea'])).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)

            else:
                bilaketa_emaitzak = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__icontains=request.POST['hasieraData']) & Q(egoera='itxita')  & Q(monitorea__icontains=request.POST['monitorea']))# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                zenbat_ensaio = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__icontains=request.POST['hasieraData']) & Q(egoera='itxita')  & Q(monitorea__icontains=request.POST['monitorea'])).count()# & Q(monitoreaEmail__icontains=request.POST['monitoreaEmail']) & Q(monitoreaFax__icontains=request.POST['monitoreaFax']) & Q(monitoreaTel__icontains=request.POST['monitoreaTel']) & Q(monitoreaMugikor__icontains=request.POST['monitoreaMugikor']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)

        else:
            bilaketa_emaitzak = []

    else:
        ensaio_bilaketa_form = EnsaioBilaketaFormularioa()
        ensaio_bilaketa_form2 = EnsaioBilaketaFormularioa2()
        bilaketa_emaitzak = []



    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    return render(request,
            'farmaciapp/ensaioen_historikoa.html',
            {'zenbatEnsaio':zenbat_ensaio, 'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'bilaketa_emaitzak': bilaketa_emaitzak, 'ensaio_bilaketa_form': ensaio_bilaketa_form, 'ensaio_bilaketa_form2': ensaio_bilaketa_form2} )



@login_required
def ensaioa_itxi(request, ensaioa_protokolo_zenb):
    #Ensaioa itxiko da, bere itxiera data eguneko data jarriz
    
    #Eguneko data lortzen da
    eguneko_data = time.strftime("%Y-%m-%d")

    #Ensaioa eskuratu eta egoera 'itxita' balioarekin ezartzen da
    ensaioa = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)
    ensaioa.bukaeraData = eguneko_data
    ensaioa.egoera = 'itxita'
    ensaioa.save()

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    ensaio_bilaketa_form = EnsaioBilaketaFormularioa()
    ensaio_bilaketa_form2 = EnsaioBilaketaFormularioa2()

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request, 'farmaciapp/ensaioak_bilatu.html', {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'ensaio_bilaketa_form':ensaio_bilaketa_form, 'ensaio_bilaketa_form2':ensaio_bilaketa_form2})





@login_required
def itxitako_ensaioa_info(request, ensaioa_protokolo_zenb):
    #Aukeratutako ensaioaren informazioa erakutsiko da
    context_dict = {}
    context_dict['egoera'] = None
    context_dict['hasieraData'] = None
    context_dict['bukaeraData'] = None
    context_dict['protokoloZenbakia'] = None
    context_dict['titulua'] = None
    context_dict['zerbitzua'] = None
    context_dict['promotorea'] = None
    context_dict['estudioMota'] = None
    context_dict['monitoreaTel'] = None
    context_dict['monitoreaFax'] = None
    context_dict['monitoreaMugikor'] = None
    context_dict['monitoreaEmail'] = None
    context_dict['monitorea'] = None
    context_dict['ikertzailea'] = None
    context_dict['komentarioak'] = None
    context_dict['medikamentuak'] = None


    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    context_dict['mota'] = erabiltzaile_mota
    context_dict['farmazia'] = farmazia
    context_dict['admin'] = 'admin'
    try:
        ensaioa = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)
        context_dict['egoera'] = ensaioa.egoera
        context_dict['hasieraData'] = ensaioa.hasieraData
        context_dict['bukaeraData'] = ensaioa.bukaeraData
        context_dict['protokoloZenbakia'] = ensaioa.protokoloZenbakia
        context_dict['titulua'] = ensaioa.titulua
        context_dict['zerbitzua'] = ensaioa.zerbitzua
        context_dict['promotorea'] = ensaioa.promotorea
        context_dict['estudioMota'] = ensaioa.estudioMota
        context_dict['monitoreaTel'] = ensaioa.monitoreaTel
        context_dict['monitoreaFax'] = ensaioa.monitoreaFax
        context_dict['monitoreaMugikor'] = ensaioa.monitoreaMugikor
        context_dict['monitoreaEmail'] = ensaioa.monitoreaEmail
        context_dict['monitorea'] = ensaioa.monitorea
        context_dict['ikertzailea'] = ensaioa.ikertzailea
        context_dict['komentarioak'] = ensaioa.komentarioak

        #zeintzuk medikamentu dituen agertuko da lehenik
        ensaioa = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)
        medikamentuen_lista = MedikamentuEnsaio.objects.filter(Q(ensaioa=ensaioa.titulua))#.values('medikamentua').distinct()
        context_dict['medikamentuak'] = medikamentuen_lista

    except Ensaioa.DoesNotExist:
        pass

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))
    context_dict['pendienteak'] = errezeta_pendienteak.count
   
    return render(request, 'farmaciapp/itxitako_ensaioa_info.html', context_dict)




@login_required
def itxitako_ensaioen_dispentsazioak(request, ensaioa_protokolo_zenb):
    #Ensaioaren dispentsazioak aztertuko dira

    #Aldagai laguntzaileak
    flagNoizarte = False
    flagNoiztik = False
    flagPazientea = False
    bilaketa_emaitzak = []
    pazienteaEnsaioan = None
    paziente_id="ezebez"
    noiztik = ''
    noizarte = ''
    pazienteidreal = ''

    if request.method == 'POST':
        
        dispentsazio_form = DispentsazioFormularioa(data=request.POST, ensaioa_protokolo_zenb=ensaioa_protokolo_zenb)

        #Jasotako datuak zuzenak badira
        if (dispentsazio_form.is_valid() and 'dataNoiztik' in request.POST):
            paziente_id = None
            pazienteidreal = request.POST['paziente']
            noiztik = request.POST['dataNoiztik']
            noizarte = request.POST['dataNoizArte']
            
            #Lehenengo, ensaio horretan dauden dispentsazio guztiak lortzen dira, gero, pazientearekiko filtratzeko
            dispentsazioak_ensaioan = Dispentsazioa.objects.filter(Q(ensaioa__protokoloZenbakia=ensaioa_protokolo_zenb))

            #Lehenik, paziente konkretu bat aukeratu duen edo ez ikusi behar da
            if 'paziente' in request.POST:
                paziente_id = request.POST['paziente']

                if len(paziente_id)>0:
                    #paziente konkretu bat bat espezifikatu baldin bada
                    paziente_id = request.POST['paziente']
                else:
                    #ez bada paziente konkreturik espezifikatu
                    paziente_id = -1
                    


            #Bilaketak egiteko flag hauek erabiliko ditugu, jakiteko erbailtzaileak zein aukera hautatu dituen bilaketarako
            if(request.POST['dataNoiztik']!=''):
                flagNoiztik = True

            if(request.POST['dataNoizArte']!=''):
                flagNoizarte = True

            #Paziente konkretu bat espezifikatu baldin bada
            if paziente_id != -1:

                if (flagNoiztik and flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik']) and Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte']) and Q(paziente__ident=pazientea_id)).distinct()

                if (not flagNoiztik and flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte']) and Q(paziente__ident=pazientea_id)).distinct()

                if (flagNoiztik and not flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik']) and Q(paziente__ident=pazientea_id)).distinct()

                if (not flagNoiztik and not flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(paziente__ident=pazientea_id)).distinct()

            
            else:
                if (flagNoiztik and flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik']) and Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte'])).distinct()

                if (not flagNoiztik and flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte'])).distinct()

                if (flagNoiztik and not flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan) and Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik'])).distinct()

                if (not flagNoiztik and not flagNoizarte):
                    bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa=dispentsazioak_ensaioan)).distinct()

  
        else:

            bilaketa_emaitzak = []
            print dispentsazio_form.errors

    
    else:

        dispentsazio_form = DispentsazioFormularioa(ensaioa_protokolo_zenb=ensaioa_protokolo_zenb)
        bilaketa_emaitzak = []

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(Q(erabiltzailea=request.user))[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request,
            'farmaciapp/itxitako_dispentsazioak_aztertu.html',
            {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'farmazia':farmazia, 'mota':erabiltzaile_mota, 'pazienteidreal':pazienteidreal, 'noiztik': noiztik, 'noizarte': noizarte, 'paziente_id': paziente_id, 'pazientea': pazienteaEnsaioan, 'ensaioa': ensaioa_protokolo_zenb, 'bilaketa_emaitzak': bilaketa_emaitzak, 'dispentsazio_form': dispentsazio_form, 'ensaioa_titulua':ensaioa_protokolo_zenb} )


@login_required
def itxitako_dispentsazioaren_info(request, ensaioa_protokolo_zenb, dispentsazioa_ident):

    #Hemen itxita dagoen dispentsazioaren informazioa ikusi ahalko da
    context_dict = {}
    context_dict['dispentsazioa'] = dispentsazioa_ident
    context_dict['ensaioa'] = ensaioa_protokolo_zenb
    context_dict['bukaeraData'] = None
    context_dict['pazientea'] = None
    context_dict['mota'] = ErabiltzaileProfila.objects.filter(Q(erabiltzailea=request.user))[0].zerbitzua
    context_dict['admin'] = 'admin'
    context_dict['farmazia'] = 'Farmazia'
    context_dict['dispentsatzailea'] = None
    context_dict['medikamentuen_informazioa'] = None

    #Dispentsazio horren errezetaren informazioa lortu beharko litzateke
    context_dict['gainontzekoEremuak'] = None

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    context_dict['pendienteak'] = errezeta_pendienteak.count

    context_dict['errezetaIzena'] = None

    context_dict['protokoloZenbakia'] = ensaioa_protokolo_zenb


    
      
    try:
        paz_dis = PazienteDispentsazio.objects.filter(dispentsazioa__ident=dispentsazioa_ident)
        paziente_id = paz_dis[0].paziente

        #Dispentsatu diren medikamentuak eskuratuko ditugu
        paziente_dispentsazioak = PazienteDispentsazio.objects.filter(dispentsazioa__ident=dispentsazioa_ident, paziente=paziente_id)
        context_dict['medikamentuen_informazioa'] = paziente_dispentsazioak
    
        context_dict['dispentsazioa'] = dispentsazioa_ident
        context_dict['ensaioa'] = ensaioa_protokolo_zenb
        context_dict['bukaeraData'] = Dispentsazioa.objects.get(ident=dispentsazioa_ident).bukaeraData
        context_dict['pazientea'] = paziente_id
        context_dict['dispentsatzailea'] = Dispentsazioa.objects.get(ident=dispentsazioa_ident).dispentsatzailea
       
        dispentsazioa = Dispentsazioa.objects.get(ident=dispentsazioa_ident)
        errezeta = EnsaioErrezeta.objects.get(ident=dispentsazioa.ensaioerrezeta)
        context_dict['gainontzekoEremuak'] = errezeta.gainontzekoEremuak

        context_dict['errezetaIzena'] = errezeta.errezetaIzena
        
       

    except PazienteDispentsazio.DoesNotExist:
        pass

   
    return render(request, 'farmaciapp/dispentsazioa_info.html', context_dict)




@login_required
def medikamentuak_kontsultatu_botoia(request):

    #Honek eramango gaitu medikamentuen kontsulta kudeatuko duen orrialdera

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request, 'farmaciapp/medikamentu_menua.html', {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia})

@login_required
def medikamentuak_bilatu(request):

    #Aldagai laguntzaileak
    ensaioa_id = ''
    ensaioa = ''


    #Ensaioa espezifikatu den formularioan begiratzen da
    if 'ensaioa' in request.POST:
        ensaioa_id = request.POST['ensaioa']

        try:
            ensaioa = Ensaioa.objects.get(titulua=ensaioa_id)
        except:
            ensaioa_id = -1
            ensaioa = None

    if request.method == 'POST':
       
        medikamentu_bilaketa_form = MedikamentuBilaketaFormularioa(data=request.POST)
        medikamentu_bilaketa_form2 = MedikamentuBilaketaFormularioa2(data=request.POST)

        #Bidali den informazioa zuzena baldin bada
        if ((medikamentu_bilaketa_form.is_valid() or request.POST['ident'] != '') and medikamentu_bilaketa_form2.is_valid()):
           
            #Bilaketa ordua dagokion formatuan jartzen da bilaketarako
            bidalketaOrdua = parser.parse(request.POST['bidalketaOrdua']).time()
            bidalketaOrdua = bidalketaOrdua.strftime('%H:%M')
            if(ensaioa!=None):

                bilaketa_emaitzak = Medikamentua.objects.filter(Q(bidalketaOrdua__icontains=bidalketaOrdua) & Q(medikamentua_ensaioan__ensaioa=ensaioa) & Q(ident__icontains=request.POST['ident']) & Q(kit__icontains=request.POST['kit']) & Q(lote__icontains=request.POST['lote']) & Q(kaduzitatea__icontains=request.POST['kaduzitatea']) & Q(bidalketaZenbakia__icontains=request.POST['bidalketaZenbakia']) & Q(bidalketaData__icontains=request.POST['bidalketaData']))
                    

            else:
                if request.POST['bidalketaOrdua'] == '':
                    bilaketa_emaitzak = Medikamentua.objects.filter(Q(ident__icontains=request.POST['ident']) & Q(kit__icontains=request.POST['kit']) & Q(lote__icontains=request.POST['lote']) & Q(kaduzitatea__icontains=request.POST['kaduzitatea']) & Q(bidalketaZenbakia__icontains=request.POST['bidalketaZenbakia']) & Q(bidalketaData__icontains=request.POST['bidalketaData']))
                else:
                    bilaketa_emaitzak = Medikamentua.objects.filter(Q(bidalketaOrdua__icontains=bidalketaOrdua) & Q(ident__icontains=request.POST['ident']) & Q(kit__icontains=request.POST['kit']) & Q(lote__icontains=request.POST['lote']) & Q(kaduzitatea__icontains=request.POST['kaduzitatea']) & Q(bidalketaZenbakia__icontains=request.POST['bidalketaZenbakia']) & Q(bidalketaData__icontains=request.POST['bidalketaData']))
        else:
            bilaketa_emaitzak = []

    else:
        medikamentu_bilaketa_form = MedikamentuBilaketaFormularioa()
        medikamentu_bilaketa_form2 = MedikamentuBilaketaFormularioa2()
        bilaketa_emaitzak = []
        
    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    #Honek eramango gaitu medikamentuen bilaketa emaitza erakutsiko duen orrialdera
    return render(request,
            'farmaciapp/medikamentuak_bilatu.html',
            {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'ensaioa_id': ensaioa_id, 'ensaioa': ensaioa, 'bilaketa_emaitzak': bilaketa_emaitzak, 'medikamentu_bilaketa_form': medikamentu_bilaketa_form, 'medikamentu_bilaketa_form2': medikamentu_bilaketa_form2} )
    


@login_required
def medikamentua_info(request, medikamentua_identKodetua):

    #Medikamentuari dagokion informazioa agertuko da
    
    context_dict = {}
    context_dict['ident'] = None
    context_dict['kit'] = None
    context_dict['lote'] = None
    context_dict['kaduzitatea'] = None
    context_dict['bidalketaZenbakia'] = None
    context_dict['bidalketaData'] = None
    context_dict['bidalketaOrdua'] = None
    context_dict['unitateak'] = None
    context_dict['ezabatuta'] = False
    context_dict['identKodetua'] = None

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    context_dict['mota'] = erabiltzaile_mota
    context_dict['farmazia'] = farmazia
    context_dict['admin'] = 'admin'
    
      
    try:
        medikamentua = Medikamentua.objects.get(identKodetua=medikamentua_identKodetua)
        context_dict['ident'] = medikamentua.ident
        context_dict['kit'] = medikamentua.kit
        context_dict['lote'] = medikamentua.lote
        context_dict['bidalketaZenbakia'] = medikamentua.bidalketaZenbakia
        context_dict['bidalketaData'] = medikamentua.bidalketaData
        context_dict['kaduzitatea'] = medikamentua.kaduzitatea
        context_dict['bidalketaOrdua'] = medikamentua.bidalketaOrdua
        context_dict['unitateak'] = medikamentua.unitateak
        context_dict['identKodetua'] = medikamentua.identKodetua

        

    except Medikamentua.DoesNotExist:
        pass

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    context_dict['pendienteak'] = errezeta_pendienteak.count

   
    return render(request, 'farmaciapp/medikamentua_info.html', context_dict)



@login_required
def errezeta_pendienteak_kontsultatu(request):

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    return render(request, 'farmaciapp/errezeta_pendienteak.html', {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'errezeta_pendienteak': errezeta_pendienteak, 'farmazia':farmazia, 'mota': erabiltzaile_mota})




@login_required
def errezeta_info(request, errezeta_ident):
    #Hemen erakutsiko da errezetari dagokion informazioa

    context_dict = {}

    context_dict['errezeta_ident'] = errezeta_ident

    context_dict['ensaioa'] = None
    context_dict['pazientea_ident'] = None
    context_dict['preskripzioData'] = None
    context_dict['hurrengoPreskripzioData'] = None
    context_dict['paziente_pisua'] = None
    context_dict['gainontzekoEremuak'] = None
    context_dict['ensaioaren_medikamentuak'] = None
    context_dict['errezetaIzena'] = None

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    context_dict['pendienteak'] = errezeta_pendienteak.count

    

    try:
        errezeta = EnsaioErrezeta.objects.get(ident=errezeta_ident)
        context_dict['ensaioa'] = errezeta.ensaioa
        context_dict['pazientea_ident'] = errezeta.pazientea
        context_dict['preskripzioData'] = errezeta.preskripzioData
        context_dict['hurrengoPreskripzioData'] = errezeta.hurrengoPreskripzioData

        pazientea = Pazientea.objects.get(ident=errezeta.pazientea.ident)
        context_dict['paziente_pisua'] = pazientea.pisua
        context_dict['pazientea'] = pazientea

        #Jakiteko zein erabiltzailek sortu duen errezeta
        context_dict['errezetaren_sortzailea'] = errezeta.sortzailea

        #Aukeratzeko listan aterako diren pazienteen aukeraketa filtratzeko erabiliko da
        ensaioa_protokolo_zenb = errezeta.ensaioa.protokoloZenbakia
        context_dict['errezeta_form'] = ErrezetaModifikatuFormularioa(ensaioa_protokolo_zenb=ensaioa_protokolo_zenb,initial={'ensaioa':errezeta.ensaioa.titulua, 'pazientea':errezeta.pazientea, 'pazientearen_pisua':pazientea.pisua, 'preskripzioData':errezeta.preskripzioData, 'hurrengoPreskripzioData':errezeta.hurrengoPreskripzioData, 'gainontzekoEremuak':errezeta.gainontzekoEremuak})

        #Ensaio horren medikamentuak bilatuko ditugu, gero aukeratzeko zeintzuk nahi diren dispentsatu
        ensaioarenMedikamentuak = MedikamentuEnsaio.objects.filter(ensaioa=errezeta.ensaioa.titulua)
        context_dict['ensaioaren_medikamentuak'] = ensaioarenMedikamentuak

        context_dict['gainontzekoEremuak'] = errezeta.gainontzekoEremuak

        context_dict['errezetaIzena'] = errezeta.errezetaIzena

    except EnsaioErrezeta.DoesNotExist:
        pass

    
    #Jakiteko zein motako erabiltzailea den
    context_dict['mota'] = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    context_dict['farmazia'] = 'Farmazia'
    context_dict['admin'] = 'admin'


    return render(request, 'farmaciapp/errezeta_info.html', context_dict)


@login_required
def errezeta_onartu(request, errezeta_ident):
    
    #Aldagai laguntzaileen definizioa
    mezua = ''
    ensaioa = ''
    pazientea_ident = ''
    preskripzioData = ''
    hurrengoPreskripzioData = ''
    pazientea = ''
    paziente_pisua = ''
    errezetaren_sortzailea = ''
    gainontzekoEremuak = ''
    ensaioaren_medikamentuak = ''

    #Aldagai honek adieraziko du gaizki joan den edo ez dispentsazioa
    #Beharbada medikamenturen baten faltan edo
    gaizkiJoanDa = False
    eguneraketa = False

    errezeta_form = None

    #CheckBox-ean aukeratuta dauden elementuak kargatuko ditu
    aukeratutako_medikamentuak = []

    #Errezeta onartu den edo ez jakiteko aldagaia
    onartuta = False


    #Ensaioaren protokolo zenbakia lortzen da
    errezeta_protokolo_zenb = EnsaioErrezeta.objects.get(ident=errezeta_ident)
    #errezetako pazienteen zerrenda kudeatzeko erabiliko da
    ensaioa_protokolo_zenb = errezeta_protokolo_zenb.ensaioa.protokoloZenbakia


    if request.method == 'POST':

        #Checkbox-ean markatutako medikamentuak jasotzen dira
        dispentsatu_beharreko_medikamentu_lista = request.POST.getlist('medikamentua')
        
        #Lista hutsa ez bada eta medikamentu bat aukeratu baldin bada
        if dispentsatu_beharreko_medikamentu_lista:

            #Errezetaren egoera 'Pendiente'-tik 'Dispentsatuta'-ra pasatu behar da
            
            ensaio_errezeta = EnsaioErrezeta.objects.get(ident=errezeta_ident)
        
            ensaioa = Ensaioa.objects.get(protokoloZenbakia=request.POST['ensaioa'])
        
            bukaeraData = parser.parse(request.POST['preskripzioData']).date()
            bukaeraData = bukaeraData.strftime('%Y-%m-%d')

            dispentsazioa = Dispentsazioa(ensaioerrezeta=errezeta_ident, bukaeraData=bukaeraData, ensaioa=ensaioa, dispentsatzailea=request.user)
            dispentsazioa.save()

            #Errezeta dispentsatuta bezala jartzen da
            ensaio_errezeta.pendiente = 'Dispentsatuta'
            ensaio_errezeta.gainontzekoEremuak = request.POST['gainontzekoEremuak']
            ensaio_errezeta.save()

            #Ensaioaren eta pazientearen arteko erlazioa ondo eginda dagoela konprobatzen da
            try:
                paziente_ensaio = PazienteEnsaio.objects.get(idensaioan=request.POST['pazientea'], ensaioa=ensaioa)

            #Ez baldin badago erregistratuta jada, erregistratu egin behar da
            except PazienteEnsaio.DoesNotExist:
                paziente_ensaio = PazienteEnsaio(idensaioan=request.POST['pazientea'], ensaioa=ensaioa)
                paziente_ensaio.save()

            
            dispentsatu_beharreko_medikamentu_lista = request.POST.getlist('medikamentua')
            mezua = dispentsatu_beharreko_medikamentu_lista


            #Orain, medikamentuak dispentsatzera jo behar da
            for dispentsatzeko_medikamentua in dispentsatu_beharreko_medikamentu_lista:
                
                #Orain aukeratutako medikamentu bakoitzaren unitateak hartzen dira
                medikamentuaren_unitateak = int(request.POST[dispentsatzeko_medikamentua])

                #Medikamentuaren objektua lortzen da
                medikamentua = Medikamentua.objects.get(ident=dispentsatzeko_medikamentua)


                #Dispentsazioa erregistratzen da
                pazientea = paziente_ensaio.pazientea
                paziente_dispentsazio = PazienteDispentsazio(ident=dispentsazioa.ident, dispentsazioa=dispentsazioa, paziente=pazientea, medikamentua=medikamentua, dosia=medikamentuaren_unitateak)
                paziente_dispentsazio.save()

                #stock-ean dagoen medikamentuari unitate horiek kentzen zaizkio
                medikamentua.unitateak = medikamentua.unitateak - medikamentuaren_unitateak
                medikamentua.save()

                #Bakarrik onartuko da dispentsazioa medikamenturen bat dispentsatu bazaio
                onartuta = True


        if not onartuta:
            mezua = "Medikamentu bat dispentsatu behar zaio gutxienez"
            gaizkiJoanDa = True
           
            try:

                #Interfazeko formularioan agertu behar den eremuen informazioa eskuratzen da
                errezeta = EnsaioErrezeta.objects.get(ident=errezeta_ident)
                ensaioa = errezeta.ensaioa
                pazientea_ident = errezeta.pazientea
                preskripzioData = errezeta.preskripzioData
                hurrengoPreskripzioData = errezeta.hurrengoPreskripzioData
                
                pazientea = Pazientea.objects.get(ident=errezeta.pazientea.ident)
                paziente_pisua = pazientea.pisua
                pazientea = pazientea

                #Jakiteko zein erabiltzailek sortu duen errezeta
                errezetaren_sortzailea = errezeta.sortzailea
                
                errezeta_form = ErrezetaModifikatuFormularioa(ensaioa_protokolo_zenb=ensaioa_protokolo_zenb, initial={'ensaioa':errezeta.ensaioa.titulua, 'pazientea':errezeta.pazientea, 'pazientearen_pisua':pazientea.pisua, 'preskripzioData':errezeta.preskripzioData, 'hurrengoPreskripzioData':errezeta.hurrengoPreskripzioData, 'gainontzekoEremuak':errezeta.gainontzekoEremuak})

                #Ensaio horren medikamentuak bilatuko ditugu, gero aukeratzeko zeintzuk nahi diren dispentsatu
                ensaioarenMedikamentuak = MedikamentuEnsaio.objects.filter(ensaioa=errezeta.ensaioa.titulua)
                ensaioaren_medikamentuak = ensaioarenMedikamentuak

                gainontzekoEremuak = errezeta.gainontzekoEremuak

            except EnsaioErrezeta.DoesNotExist:
                pass



    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request, 'farmaciapp/errezeta_info.html', {'pendienteak':errezeta_pendienteak.count, 'gaizkiJoanDa':gaizkiJoanDa, 'eguneraketa':eguneraketa, 'errezeta_form':errezeta_form, 'mezua':mezua, 'onartuta':onartuta, 'admin':admin, 'errezeta_pendienteak': errezeta_pendienteak, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'gainontzekoEremuak':gainontzekoEremuak, 'ensaioa':ensaioa, 'pazientea_ident':pazientea_ident, 'preskripzioData':preskripzioData, 'hurrengoPreskripzioData':hurrengoPreskripzioData, 'pazientea':pazientea, 'paziente_pisua':paziente_pisua, 'errezetaren_sortzailea':errezetaren_sortzailea, 'ensaioaren_medikamentuak':ensaioaren_medikamentuak})


@login_required
def errezeta_modifikatu(request, errezeta_ident):
    #Hemen aurretik zeuzkan datuan jarriko ditugu eta aukera emango zaio erabiltzaileari aldatzeko
    eguneraketa = False
    sortzailea = ''

    #Errezetako pazienteen zerrenda kudeatzeko erabiliko da
    ensaioa_protokolo_zenb_objektua = Ensaioa.objects.get(titulua=request.POST['ensaioa'])
    ensaioa_protokolo_zenb = ensaioa_protokolo_zenb_objektua.protokoloZenbakia

    if request.method == 'POST':
        sortzailea = request.POST['errezetaren_sortzailea']

        errezeta_form = ErrezetaModifikatuFormularioa(data=request.POST, ensaioa_protokolo_zenb=ensaioa_protokolo_zenb)
        if errezeta_form.is_valid():

            ensaioa = Ensaioa.objects.get(titulua=request.POST['ensaioa'])
            pazientea = Pazientea.objects.get(ident=request.POST['pazientea'])

            
            try:
                #Balio berriekin moldatu nahi den errezeta existitzen den edo ez konprobatuko da
                ensaioerrezeta = EnsaioErrezeta.objects.get(ensaioa=ensaioa.titulua, pazientea=pazientea, preskripzioData=request.POST['preskripzioData'], hurrengoPreskripzioData=request.POST['hurrengoPreskripzioData'])
                eguneraketa = False
            except:
                #Aurreko datuekin geneukan errezeta hartu eta balioak aldatuko dizkiogu
                
                errezeta = EnsaioErrezeta.objects.get(ident=errezeta_ident)

                hurrengoPreskripzioData = None

                #Balio berriak esleitzen dira
                errezeta.ensaioa = ensaioa
                errezeta.pazientea = pazientea
                preskripzioData = parser.parse(request.POST['preskripzioData']).date()
                preskripzioData = preskripzioData.strftime('%Y-%m-%d')

                #Hurrengo preskripzio data ez denez derrigorra, begiratu behar da ea definitu den formularioan parseatzeko eta errorerik ez emateko
                if request.POST['hurrengoPreskripzioData'] != '':
                    hurrengoPreskripzioData = parser.parse(request.POST['hurrengoPreskripzioData']).date()
                    hurrengoPreskripzioData = hurrengoPreskripzioData.strftime('%Y-%m-%d')
  

                errezeta.hurrengoPreskripzioData = hurrengoPreskripzioData

                errezeta.preskripzioData = preskripzioData
                
                errezeta.save()

                #Ondo eguneratu dela adierazten da
                sortuta = True
                eguneraketa = True

        else:
            print errezeta_form.errors

    else:
        errezeta_form = ErrezetaModifikatuFormularioa(ensaioa_protokoloa_zenb=ensaioa_protokoloa_zenb)

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    ensaioa = request.POST['ensaioa']
    pazientea = request.POST['pazientea']
    pazientePisua = request.POST['pazientearen_pisua']
    preskripzioData = request.POST['preskripzioData']
    hurrengoPreskripzioData = request.POST['hurrengoPreskripzioData']

    errezetaIzena = EnsaioErrezeta.objects.get(ident=errezeta_ident).errezetaIzena

    ensaioarenMedikamentuak = MedikamentuEnsaio.objects.filter(ensaioa=ensaioa)

    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request,
            'farmaciapp/errezeta_info.html',
            {'errezetaIzena':errezetaIzena, 'ensaioaren_medikamentuak':ensaioarenMedikamentuak, 'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'errezetaren_sortzailea':sortzailea, 'eguneraketa':eguneraketa, 'errezeta_ident':errezeta_ident, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'errezeta_form':errezeta_form, 'ensaioa':ensaioa, 'pazientea_ident':pazientea, 'preskripzioData':preskripzioData, 'hurrengoPreskripzioData':hurrengoPreskripzioData, 'paziente_pisua':pazientePisua})





@login_required
def medikamentuaren_ensaioak_ikusi(request, medikamentua_identKodetua):
    
    #Medikamentua zein ensaiorekin dagoen erlazionatuta ikusiko da
    ensaio_lista = MedikamentuEnsaio.objects.filter(Q(medikamentua__identKodetua=medikamentua_identKodetua)).values('ensaioa').distinct()
    
    ensaioak = Ensaioa.objects.filter(Q(titulua=ensaio_lista))

    #Lista bat sortzen da, lista horretan gordetzeko medikamentuaren ensaioak
    lista = []
    i=1
    for ensaioaren_titulua in ensaio_lista:
   
         ensaioa = Ensaioa.objects.get(titulua=ensaioaren_titulua.get('ensaioa', None))
         lista.insert(i,ensaioa.protokoloZenbakia)
         i = len(lista) 

    ensaioak = lista

    
    medikamentua = Medikamentua.objects.get(identKodetua=medikamentua_identKodetua).ident

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    #Honek erakutsiko du medikamentu horren ensaioak agertzen diren orrialdea
    return render(request, 'farmaciapp/medikamentuaren_ensaioak.html', {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'medikamentua':medikamentua, 'ensaio_lista': ensaioak})






@login_required
def aukeratutako_ensaioak_ezabatu(request):
    
    #CheckBox-ean aukeratuta dauden elementuak ezabatuko ditu
    ezabatu_beharreko_ensaio_lista = []
    ensaio_bilaketa_form = EnsaioBilaketaFormularioa()
    ensaio_bilaketa_form2 = EnsaioBilaketaFormularioa2()

    if request.method == 'POST':
        ezabatu_beharreko_ensaio_lista = request.POST.getlist('ensaioa')
        for ezabatzeko_ensaioa_titulua in ezabatu_beharreko_ensaio_lista:
            #Ensaio horren dispentsazioak ezabatu behar dira
            ezabatzeko_dispentsazioak = Dispentsazioa.objects.filter(Q(ensaioa__titulua=ezabatzeko_ensaioa_titulua))
            for disp in ezabatzeko_dispentsazioak:
                PazienteDispentsazio.objects.filter(Q(dispentsazioa=disp)).delete()
                disp.delete()

            EnsaioErrezeta.objects.filter(Q(ensaioa__titulua=ezabatzeko_ensaioa_titulua)).delete()
            PazienteEnsaio.objects.filter(Q(ensaioa__titulua=ezabatzeko_ensaioa_titulua)).delete()
            MedikamentuEnsaio.objects.filter(Q(ensaioa__titulua=ezabatzeko_ensaioa_titulua)).delete()
            Ensaioa.objects.get(titulua=ezabatzeko_ensaioa_titulua).delete()



    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request, 'farmaciapp/ensaioak_bilatu.html', {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'ensaio_bilaketa_form':ensaio_bilaketa_form, 'ensaio_bilaketa_form2':ensaio_bilaketa_form2, 'ensaio_lista': ezabatu_beharreko_ensaio_lista})




@login_required
def paziente_berria_erregistratu_botoia(request):
    
    #Hemen paziente berriaren informazioa gehituko da, errezeta bat egin ahal izateko

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #formularioa hasieratzen da
    paziente_form = PazienteBerriFormularioa() 
    
    errezeta = 'errezeta'
    ensaioa = ''

    if request.method == 'POST':
        ensaioa = request.POST['ensaioa']

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    #Hori erakutsiko den orrialdera eramango gaitu
    return render(request, 'farmaciapp/paziente_berria_sortu.html', {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'titulua':ensaioa, 'errezeta':errezeta, 'paziente_form':paziente_form, 'mota':erabiltzaile_mota, 'farmazia':farmazia})

@login_required
def paziente_berria_erregistratu(request):
    #Paziente berria erregistratzeko logika

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    #pazientea ondo erregistratu den edo ez adieraziko duen aldagaia
    erregistratuta = False

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    mezua = 'Pazientea ez da ondo sortu'
    if request.method == 'POST':
        #paziente berria sortzen da emandako datuekin

        paziente_form = PazienteBerriFormularioa(data=request.POST)
        if paziente_form.is_valid():
            
            paziente_berria = Pazientea(idensaioan=request.POST['idensaioan'], izena=request.POST['izena'], unitateKlinikoa=request.POST['unitateKlinikoa'], pisua=request.POST['pisua'])
            paziente_berria.save()

            ensaioa = Ensaioa.objects.get(protokoloZenbakia=request.POST['ensaioa'])

            pazienteensaio = PazienteEnsaio(pazientea=paziente_berria, ensaioa=ensaioa, idensaioan=request.POST['idensaioan'])
            pazienteensaio.save()
                
            mezua = 'Pazientea ondo sortu da'
            erregistratuta = True
        
        else:
            print paziente_form.errors
            return render(request, 'farmaciapp/paziente_berria_sortu.html', {'pendienteak':errezeta_pendienteak, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'admin':admin, 'titulua':request.POST['ensaioa'],'erregistratuta':erregistratuta,'paziente_form':paziente_form, 'mezua':mezua})

    else:
        paziente_form = PazienteBerriFormularioa()
        return render(request, 'farmaciapp/paziente_berria_sortu.html', {'pendienteak':errezeta_pendienteak, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'admin':admin,'titulua':request.POST['ensaioa'],'erregistratuta':erregistratuta,'paziente_form':paziente_form, 'mezua':mezua})


    #Errezetarako pazienteen zerrenda egiteko erabiliko da
    ensaioa_protokolo_zenb = request.POST['ensaioa']

    errezeta_form = ErrezetaBerriEnsaiotikFormularioa(ensaioa_protokolo_zenb=ensaioa_protokolo_zenb)
    return render(request, 'farmaciapp/paziente_berria_sortu.html', {'pendienteak':errezeta_pendienteak.count, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'admin':admin,'titulua':request.POST['ensaioa'], 'errezeta_form':errezeta_form, 'mezua':mezua,'erregistratuta':erregistratuta})




@login_required
def erabiltzaile_menua(request):

    #Aplikazioan erregistratuta dauden erabiltzaileen menura eramango gaitu

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    admin = 'admin'

    #Aplikazioan dauden erabiltzaile guztiak bilatuko dira
    bilaketa_emaitzak = ErabiltzaileProfila.objects.all()

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request, 'farmaciapp/erabiltzaile_kudeaketa_menua.html', {'pendienteak':errezeta_pendienteak.count, 'bilaketa_emaitzak':bilaketa_emaitzak, 'mota':erabiltzaile_mota, 'admin':admin})


@login_required
def erabiltzailea_info(request, erabiltzailea):
    
    erabiltzaile_form = ErabiltzaileFormularioa(initial={'username':erabiltzailea})

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    admin = 'admin'

    #Ikusi nahi den erabiltzailearen mota
    ikusteko_erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea__username=erabiltzailea)[0].zerbitzua


    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request, 'farmaciapp/erabiltzaile_info.html', {'pendienteak':errezeta_pendienteak.count, 'ikusteko_erabiltzaile_mota':ikusteko_erabiltzaile_mota, 'erabiltzailea':erabiltzailea, 'erabiltzaile_form':erabiltzaile_form, 'admin':admin, 'mota':erabiltzaile_mota})


@login_required
def erabiltzailea_eguneratu(request, erabiltzailea):
    #Aldagai hau erabiliko da adierazteko ea eguneraketa ondo joan den edo ez
    eguneratuta = False


    if request.method == 'POST':
        erabiltzaile_form = ErabiltzaileFormularioa(data=request.POST)

        #erabiltzaile izen bat izan behar duela konprobatzen da
        if len(request.POST['username'])>0:

            erabiltzailea_profila = ErabiltzaileProfila.objects.get(erabiltzailea__username=erabiltzailea)
            erabiltzailea_info = User.objects.get(username=erabiltzailea)

            #pasahitzaren luzeera 0 karaktere baino gehiagokoa baldin bada
            if len(request.POST['password'])>0:
                erabiltzailea_info.set_password(request.POST['password'])
                #pasahitza aldatuko diogu

            if len(request.POST['username'])>0:
                #Lehenik konprobatzen da ea existitzen den erabiltzaile hori
                #Eta existitzen bada, ea erabiltzaile honen username zaharra den
                if request.POST['username']!=erabiltzailea:
                    try:
                        erabiltzailea_konprobatu = User.objects.get(username=request.POST['username'])
                        mezua = 'Erabiltzaile hori existitzen da jada!'
                    except:

                        erabiltzailea_info.username = request.POST['username']
                        #erabiltzailea aldatuko diogu

            erabiltzailea_info.email = request.POST['email']
            erabiltzailea_info.save()

            erabiltzailea_profila.username = erabiltzailea_info

            #Ikusten dugu ea zerbitzuaren balio berria admin, Farmazia edo Medikua den
            #Horietako bat baldin bada, balioa aldatuko diogu
            #Bestela, mantendu egingo diogu
            motaBerria = request.POST['zerbitzua']
            if motaBerria == 'admin' or motaBerria == 'Farmazia' or motaBerria == 'Medicina':
                #Aldatu egingo diogu balioa
                erabiltzailea_profila.zerbitzua = motaBerria
           


            erabiltzailea_profila.save()

            erabiltzailea_info.save()
            eguneratuta = True


        else:
            print erabiltzaile_form.errors

    else:
        erabiltzaile_form = ErabiltzaileFormularioa()

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    admin = 'admin'

    #Aplikazioan dauden erabiltzaile guztiak bilatuko dira
    bilaketa_emaitzak = ErabiltzaileProfila.objects.all()

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))



    return render(request, 'farmaciapp/erabiltzaile_info.html', {'pendienteak':errezeta_pendienteak.count, 'eguneratuta':eguneratuta, 'bilaketa_emaitzak':bilaketa_emaitzak, 'erabiltzailea':erabiltzailea, 'erabiltzaile_form':erabiltzaile_form, 'admin':admin, 'mota':erabiltzaile_mota})

@login_required
def medikamentuaren_unitateak_ezabatu(request, medikamentua_identKodetua):
    #Medikamentuaren unitateak ezabatzen dira Stock-etik

    #Zenbat unitate geldituko diren unitateak kendu eta gero kalkulatzen da
    medikamentua = Medikamentua.objects.get(identKodetua=medikamentua_identKodetua)
    momentuko_stocka = int(medikamentua.unitateak)
    amaierako_stocka = momentuko_stocka - int(request.POST['medikamentuKantitatea'])

    historiko_berria = int(medikamentua.unitateak_historikoa) - int(request.POST['medikamentuKantitatea'])
    medikamentua.unitateak_historikoa = historiko_berria

    medikamentua.unitateak = amaierako_stocka
    medikamentua.save()


    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Aldagai honek adieraziko du medikamentua eguneratua izan dela
    eguneratuta = True

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))



    return render(request, 'farmaciapp/medikamentua_info.html', {'pendienteak':errezeta_pendienteak.count, 'eguneratuta':eguneratuta, 'admin':admin, 'mota':erabiltzaile_mota})


@login_required
def erabiltzailea_ezabatu(request, erabiltzailea):
    
    #Erabiltzailearen profila eta informazioa ezabatuko dira

    #Lehenik, erabiltzailea aurkitzen da
    erabiltzailea_profila = ErabiltzaileProfila.objects.get(erabiltzailea__username=erabiltzailea)
    erabiltzailea_profila.erabiltzailea.delete()
    erabiltzailea_profila.delete()

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    admin = 'admin'

    #Aplikazioan dauden erabiltzaile guztiak bilatuko dira
    bilaketa_emaitzak = ErabiltzaileProfila.objects.all()

    #Erabiltzailea ezabatu den edo ez jakiteko flag bat
    ezabatuta = True

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request, 'farmaciapp/erabiltzaile_kudeaketa_menua.html', {'pendienteak':errezeta_pendienteak.count, 'ezabatuta':ezabatuta, 'bilaketa_emaitzak':bilaketa_emaitzak, 'erabiltzailea':erabiltzailea, 'admin':admin, 'mota':erabiltzaile_mota})


@login_required
def erabiltzailea_gehitu(request):

    #Erabiltzaile berri bat gehitzeko pantaila erakutsiko da

    erabiltzaile_form = ErabiltzaileFormularioa()
    erabiltzaile_profil_form = ErabiltzaileProfilFormularioa()

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    admin = 'admin'

    erregistratuta = False

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request,
            'farmaciapp/erregistratu.html',
            {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'erabiltzaile_form': erabiltzaile_form, 'erabiltzaile_profil_form': erabiltzaile_profil_form, 'erregistratuta': erregistratuta} )



@login_required
def erabiltzaileak_bilatu(request):

    #Erabiltzaileak bilatzera joko da

    if request.method == 'POST':
        
        #Guztiak aukera baldin badago aukeraketan, ez da erabiltzailearen motaren araberako filtrorik aplikatuko, eta mota guztietako erabiltzaileak bilatzen saiatuko da
        if request.POST['zerbitzua'] == 'Guztiak':
            #Ez da zerbitzuen araberako bilaketarik egingo
            bilaketa_emaitzak = ErabiltzaileProfila.objects.filter(Q(erabiltzailea__username__icontains=request.POST['username']) & Q(erabiltzailea__email__icontains=request.POST['email']) & Q(izena__icontains=request.POST['izena']) & Q(abizena1__icontains=request.POST['abizena1']) & Q(abizena2__icontains=request.POST['abizena2']) & Q(azpizerbitzua__icontains=request.POST['azpizerbitzua']))

        else:

            bilaketa_emaitzak = ErabiltzaileProfila.objects.filter(Q(erabiltzailea__username__icontains=request.POST['username']) & Q(erabiltzailea__email__icontains=request.POST['email']) & Q(izena__icontains=request.POST['izena']) & Q(abizena1__icontains=request.POST['abizena1']) & Q(abizena2__icontains=request.POST['abizena2']) & Q(azpizerbitzua__icontains=request.POST['azpizerbitzua']) & Q(zerbitzua__icontains=request.POST['zerbitzua']))
    else:
        
        bilaketa_emaitzak = []


    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    admin = 'admin'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))


    return render(request,
            'farmaciapp/erabiltzaile_kudeaketa_menua.html',
            {'pendienteak':errezeta_pendienteak.count, 'admin':admin, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'bilaketa_emaitzak':bilaketa_emaitzak} )



@login_required
def pdf_eskuratu(request, ensaioa_protokolo_zenb, dispentsazioa_ident):
    #PDF-a eskuratzeko kodea

    #Dispentsazioaren/Errezeta informazio osoa eskuratzen da
    paz_dis = PazienteDispentsazio.objects.filter(dispentsazioa__ident=dispentsazioa_ident)
    paziente_id = paz_dis[0].paziente

    #Dispentsatu diren medikamentuak eskuratuko ditugu
    medikamentuak = PazienteDispentsazio.objects.filter(dispentsazioa__ident=dispentsazioa_ident, paziente=paziente_id).values('medikamentua')
    bukaeraData = Dispentsazioa.objects.get(ident=dispentsazioa_ident).bukaeraData
    pazientea = paziente_id
    dispentsatzailea = Dispentsazioa.objects.get(ident=dispentsazioa_ident).dispentsatzailea
     
    #Errezetaren gainontzeko informazioa lortzen da  
    errezeta = EnsaioErrezeta.objects.get(ident=Dispentsazioa.objects.get(ident=dispentsazioa_ident).ensaioerrezeta)
    gainontzekoEremuak = errezeta.gainontzekoEremuak

    #Ensaioaren informazioa aterako da
    ensaioa = Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb)

    ikertzailea = ensaioa.ikertzailea
    promotorea = ensaioa.promotorea
    titulua = ensaioa.titulua


    #HttpResponse objektua sortzen da.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+dispentsazioa_ident+'.pdf"'

    c = canvas.Canvas(response)

    c.setFont('Helvetica-Bold', 18) #Formatua, letra mota eta tamaina

    c.drawString(50,770,'Dispensacion: ' + errezeta.errezetaIzena)

    #Altuera 0-tik behetik gora hasten da 

    #Zabalera 0-tik ezkerretik eskuinera

    c.line(50,760,580,760) #Lerro horizontala

    c.setFont('Helvetica', 12) #Formatua, letra mota eta tamaina


    c.drawString(50,730, 'Titulo del ensayo: ' + str(titulua))
    c.drawString(50,700, 'Numero de protocolo del ensayo: ' + str(ensaioa_protokolo_zenb))
    c.drawString(50,670, 'Nombre de paciente: ' + str(paziente_id.izena))
    c.drawString(50,640, 'Numero de paciente: ' + str(paziente_id.ident))

    c.setFont('Helvetica-Bold', 18) #Formatua, letra mota eta tamaina

    c.drawString(180, 610, 'MEDICAMENTO')

    c.setFont('Helvetica', 12) #Formatua, letra mota eta tamaina

    #Medikamentuak zerrendatuko dira
    altuera = 580
    for med in medikamentuak:
        #Dagokion medikamentuaren dosia kalkulatuko da:
        dosia = PazienteDispentsazio.objects.get(dispentsazioa=dispentsazioa_ident, medikamentua=med.get('medikamentua')).dosia
        c.drawString(120, altuera, '- ' + med.get('medikamentua') + '       Unidades: ' + str(dosia))
        altuera = altuera - 30


    c.drawString(50,altuera, 'Medico investigador: ' + str(ikertzailea))
    altuera = altuera - 30
    c.drawString(50,altuera, 'Promotor: ' + str(promotorea))
    altuera = altuera - 30
    c.drawString(50,altuera, 'Fecha de Dispensacion: ' + str(bukaeraData))
    altuera = altuera - 30
    c.drawString(50,altuera, 'Encargado de la dispensacion: ' + dispentsatzailea)
    altuera = altuera - 30
    c.drawString(50,altuera, 'Servicio: ' + Ensaioa.objects.get(protokoloZenbakia=ensaioa_protokolo_zenb).zerbitzua)


    altuera = altuera - 30
    c.drawString(50,altuera, gainontzekoEremuak)
    altuera = altuera - 30

    c.drawString(50,altuera, 'Firmado: ' + str(request.user))
    altuera = altuera - 30


    c.setFont('Helvetica-Bold', 18) #Formatua, letra mota eta tamaina

    c.line(30,altuera,580,altuera)
    altuerakuadro1 = altuera
    altuera = altuera - 30


    c.drawString(150, altuera, 'MEDICAMENTOS DISPENSADOS')

    c.setFont('Helvetica', 12) #Formatua, letra mota eta tamaina

    altuera = altuera - 30



    for med in medikamentuak:
        #Dagokion medikamentuaren dosia kalkulatuko da:
        dosia = PazienteDispentsazio.objects.get(dispentsazioa=dispentsazioa_ident, medikamentua=med.get('medikamentua')).dosia
        c.drawString(120, altuera, '- ' + med.get('medikamentua') + '       Unidades: ' + str(dosia))
        altuera = altuera - 30

    c.drawString(50,altuera, 'Fecha: ' + time.strftime("%Y-%m-%d"))
    altuera = altuera - 30
    c.drawString(50,altuera, 'Farmaceutico/a: ' + str(request.user))
    altuera = altuera - 30

    c.line(30,altuera,580,altuera)
    c.line(30,altuerakuadro1,30,altuera)
    c.line(580,altuerakuadro1,580,altuera)

    c.showPage()
    c.save() #PDF-a gordetzeko

    
    return response