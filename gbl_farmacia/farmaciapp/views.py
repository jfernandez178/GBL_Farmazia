from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from farmaciapp.forms import ErabiltzaileFormularioa, ErabiltzaileProfilFormularioa, EnsaioBerriFormularioa, EnsaioBilaketaFormularioa, EnsaioBilaketaFormularioa2, MedikamentuBilaketaFormularioa, MedikamentuBilaketaFormularioa2, Medikamentua, ErrezetaBerriFormularioa, DispentsazioFormularioa, ErrezetaBerriEnsaiotikFormularioa, MedikamentuBerriFormularioa, ErrezetaModifikatuFormularioa
from farmaciapp.models import Ensaioa, ErabiltzaileProfila, PazienteEnsaio, Pazientea, EnsaioErrezeta, MedikamentuEnsaio, Dispentsazioa, PazienteDispentsazio
from django.db.models import Q
import datetime
from dateutil import parser
#Orrialde nagusia
def index(request):
    #Hitzarmen batek adosten du parametro hori request deitu behar dela (HTTPRequest motakoa)

    if request.user.is_authenticated():
        return HttpResponseRedirect('/farmaciapp/aukera_menua/')
    else:
        # Hiztegi bat pasatzen da ereduari pasatzeko mezu bezala
        context_dict = {'boldmessage': "Farmaciapp Orrialde Nagusian zaude!"}

        # Jasotako emaitza pasatzen zaio, bezeroari erakusteko
        return render(request, 'farmaciapp/index.html', context_dict)
   

#Erabitzaile bat erregistratzekoe rabiliko den interfazearen logika adierazten du
def erregistratu(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    erregistratuta = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both ErabiltzaileFormularioa and ErabiltzaileProfilFormularioa.
        erabiltzaile_form = ErabiltzaileFormularioa(data=request.POST)
        erabiltzaile_profil_form = ErabiltzaileProfilFormularioa(data=request.POST)

        # If the two forms are valid...
        if erabiltzaile_form.is_valid() and erabiltzaile_profil_form.is_valid():
            # Save the user's form data to the database.
            erabiltzailea = erabiltzaile_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            erabiltzailea.set_password(erabiltzailea.password)
            erabiltzailea.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profila = erabiltzaile_profil_form.save(commit=False)
            profila.erabiltzailea = erabiltzailea

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
            #    profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profila.save()

            # Update our variable to tell the template registration was successful.
            erregistratuta = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print erabiltzaile_form.errors, erabiltzaile_profil_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        erabiltzaile_form = ErabiltzaileFormularioa()
        erabiltzaile_profil_form = ErabiltzaileProfilFormularioa()

    # Render the template depending on the context.
    return render(request,
            'farmaciapp/erregistratu.html',
            {'erabiltzaile_form': erabiltzaile_form, 'erabiltzaile_profil_form': erabiltzaile_profil_form, 'erregistratuta': erregistratuta} )


#Erabiltzaileak login egiteko beharreko bista
def erabiltzailea_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/farmaciapp/aukera_menua/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Zure kontua desgaituta dago...")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Sesio-irekiera desegokia: {0}, {1}".format(username, password)
            return HttpResponse("Erabiltzailea edo pasahitza ez dira egokiak!")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
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


    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(Q(erabiltzailea=request.user))[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    #Aukera menura eramango gaitu
    return render(request, 'farmaciapp/aukera_menua.html', {'farmazia':farmazia, 'mota':erabiltzaile_mota})


@login_required
def ensaioak_kontsultatu_botoia(request):
    #Erbailtzaile mota konprobatu behar da
        #Farmazia zerbitzukoa bada, orrialde mota bat erakutsiko da
        #Ez bada Farmazia zerbitzukoa, beste bat

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(Q(erabiltzailea=request.user))[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    # Honek eramango gaitu ensaioen kontsulta kudeatuko duen orrialdera
    return render(request, 'farmaciapp/ensaio_menua.html', {'farmazia':farmazia, 'mota':erabiltzaile_mota})



@login_required
def ensaioak_bilatu(request):
    
    pazientea_id = ''
    pazientea = ''
    ondo = ''
    ensaio_bilaketa_form2 = []
    pazientea_duten_ensaioak = []
    if 'pazientea' in request.POST:
        pazientea_id = request.POST['pazientea']
        try:
            pazientea = Pazientea.objects.get(ident=pazientea_id)
        except:
            pazientea_id = -1
            pazientea = None

    #Honek eramango gaitu errezetaren sorkuntza kudeatuko duen orrialdera
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both ErabiltzaileFormularioa and ErabiltzaileProfilFormularioa.
        ensaio_bilaketa_form = EnsaioBilaketaFormularioa(data=request.POST)
        ensaio_bilaketa_form2 = EnsaioBilaketaFormularioa2(data=request.POST)

          
        #bilaketa_emaitzak = Ensaioa.objects.filter(Q(ikertzailea__contains=request.POST['ikertzailea']) & Q(monitorea__contains=request.POST['monitorea']) & Q(estudioMota__contains=request.POST['estudioMota']) & Q(promotorea__contains=request.POST['promotorea']) & Q(zerbitzua__contains=request.POST['zerbitzua']) & Q(titulua__contains=request.POST['titulua']) & Q(protokoloZenbakia__contains=request.POST['protokoloZenbakia']) & Q(bukaeraData__contains=request.POST['bukaeraData']) & Q(hasieraData__contains=request.POST['hasieraData']) & Q(egoera__contains=request.POST['egoera']))#, PazienteEnsaio__isnull=False)
        #if(pazientea!=''):
        #    if(pazientea!=None):
        #        #bilaketa filtroan pazientea espezifikatu baldin bada
        #        for emaitza in bilaketa_emaitzak:
        #            #bilatu diren ensaio bakoitza aztertuko da
        #            bilaketa_emaitzak_2 = PazienteEnsaio.objects.filter(Q(pazientea=pazientea) & Q(ensaioa=emaitza))
        #            if not bilaketa_emaitzak_2:
        #                #ensaio hori eta paziente hori daukan erlazioa existitzen ez bada, ezabatu egingo da azken queryset-etik
        #                emaitza.delete()






        # If the two forms are valid...
        if ((ensaio_bilaketa_form.is_valid() or request.POST['titulua'] != '') and ensaio_bilaketa_form2.is_valid()):
           


            if(pazientea!=None):
                ondo = 'pazientea!=none'

                bilaketa_emaitzak = Ensaioa.objects.filter(Q(pazientea_ensaioan__pazientea=pazientea) & Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__icontains=request.POST['hasieraData']) & Q(egoera__icontains=request.POST['egoera']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)
                    #bilaketa_emaitzak_3 = PazienteEnsaio.objects.filter(Q(pazientea=pazientea) & Q(ensaioa=bilaketa_emaitzak_2)).values('ensaioa')#Q(ensaioa__ikertzailea__icontains=request.POST['ikertzailea']) & Q(ensaioa__monitorea__icontains=request.POST['monitorea']) & Q(ensaioa__estudioMota__icontains=request.POST['estudioMota']) & Q(ensaioa__promotorea__icontains=request.POST['promotorea']) & Q(ensaioa__zerbitzua__icontains=request.POST['zerbitzua']) & Q(ensaioa__titulua__icontains=request.POST['titulua']) & Q(ensaioa__protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(ensaioa__hasieraData__icontains=request.POST['hasieraData']) & Q(ensaioa__egoera__icontains=request.POST['egoera'])).values('ensaioa')#Q(ensaioa=emaitza))
                    
                ondo = bilaketa_emaitzak


            #        #bilaketa filtroan pazientea espezifikatu baldin bada
            #        for emaitza in bilaketa_emaitzak:
            #            #bilatu diren ensaio bakoitza aztertuko da
            #            bilaketa_emaitzak_2 = PazienteEnsaio.objects.filter(Q(pazientea=pazientea) & Q(ensaioa__ikertzailea__icontains=request.POST['ikertzailea']) & Q(ensaioa__monitorea__icontains=request.POST['monitorea']) & Q(ensaioa__estudioMota__icontains=request.POST['estudioMota']) & Q(ensaioa__promotorea__icontains=request.POST['promotorea']) & Q(ensaioa__zerbitzua__icontains=request.POST['zerbitzua']) & Q(ensaioa__titulua__icontains=request.POST['titulua']) & Q(ensaioa__protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(ensaioa__hasieraData__icontains=request.POST['hasieraData']) & Q(ensaioa__egoera__icontains=request.POST['egoera']))#Q(ensaioa=emaitza))
            #            ondo = bilaketa_emaitzak_2
            #            if not bilaketa_emaitzak_2:
            #                #ensaio hori eta paziente hori daukan erlazioa existitzen ez bada, ezabatu egingo da azken queryset-etik
            #                emaitza.delete()
            #                ondo = 'ezabatu du zerbait'
            else:
                bilaketa_emaitzak = Ensaioa.objects.filter(Q(ikertzailea__icontains=request.POST['ikertzailea']) & Q(monitorea__icontains=request.POST['monitorea']) & Q(estudioMota__icontains=request.POST['estudioMota']) & Q(promotorea__icontains=request.POST['promotorea']) & Q(zerbitzua__icontains=request.POST['zerbitzua']) & Q(titulua__icontains=request.POST['titulua']) & Q(protokoloZenbakia__icontains=request.POST['protokoloZenbakia']) & Q(hasieraData__icontains=request.POST['hasieraData']) & Q(egoera__icontains=request.POST['egoera']))# & Q(bukaeraData__icontains=request.POST['bukaeraData']))#, PazienteEnsaio__isnull=False)


  
        else:
            bilaketa_emaitzak = []
            ondo = 'ez'

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        ensaio_bilaketa_form = EnsaioBilaketaFormularioa()
        ensaio_bilaketa_form2 = EnsaioBilaketaFormularioa2()
        bilaketa_emaitzak = []
        ondo = 'ez da POST'



    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    # Render the template depending on the context.
    return render(request,
            'farmaciapp/ensaioak_bilatu.html',
            {'mota':erabiltzaile_mota, 'farmazia':farmazia, 'ondo':ondo, 'pazientea_id': pazientea_id, 'pazientea': pazientea, 'bilaketa_emaitzak': bilaketa_emaitzak, 'ensaio_bilaketa_form': ensaio_bilaketa_form, 'ensaio_bilaketa_form2': ensaio_bilaketa_form2, 'pazientea_duten_ensaioak': pazientea_duten_ensaioak} )
    #TODO




#@login_required
#def ensaioa_sortu(request):
#    #Honek eramango gaitu errezetaren sorkuntza kudeatuko duen orrialdera
#    #TODO
#    return render(request, 'farmaciapp/ensaioa_sortu.html', {})

@login_required
def ensaioa_sortu(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    sortuta = False
    ensaioa_titulua = ''
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both ErabiltzaileFormularioa and ErabiltzaileProfilFormularioa.
        ensaio_form = EnsaioBerriFormularioa(data=request.POST)

        # If the two forms are valid...
        if ensaio_form.is_valid():
            # Save the user's form data to the database.
            ensaioa = ensaio_form.save()
            ensaioa_titulua = request.POST['titulua']

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            #profila = erabiltzaile_profil_form.save(commit=False)
            #profila.erabiltzailea = erabiltzailea

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
            #    profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            ensaioa.save()

            # Update our variable to tell the template registration was successful.
            sortuta = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print ensaio_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        ensaio_form = EnsaioBerriFormularioa()

    # Render the template depending on the context.
    #Erbailtzaile mota konprobatu behar da
        #Farmazia zerbitzukoa bada, orrialde mota bat erakutsiko da
        #Ez bada Farmazia zerbitzukoa, beste bat

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    return render(request,
            'farmaciapp/ensaioa_sortu.html',
            {'ensaio_form': ensaio_form, 'sortuta': sortuta, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'ensaioa_titulua':ensaioa_titulua} )



def ensaioa_info(request, ensaioa_titulua):
    context_dict = {}
    context_dict['egoera'] = None
    context_dict['hasieraData'] = None
    context_dict['bukaeraData'] = None
    context_dict['protokoloZenbakia'] = None
    context_dict['titulua'] = None
    context_dict['zerbitzua'] = None
    context_dict['promotorea'] = None
    context_dict['estudioMota'] = None
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
      
    try:
        ensaioa = Ensaioa.objects.get(titulua=ensaioa_titulua)
        context_dict['egoera'] = ensaioa.egoera
        context_dict['hasieraData'] = ensaioa.hasieraData
        context_dict['bukaeraData'] = ensaioa.bukaeraData
        context_dict['protokoloZenbakia'] = ensaioa.protokoloZenbakia
        context_dict['titulua'] = ensaioa.titulua
        context_dict['zerbitzua'] = ensaioa.zerbitzua
        context_dict['promotorea'] = ensaioa.promotorea
        context_dict['estudioMota'] = ensaioa.estudioMota
        context_dict['monitorea'] = ensaioa.monitorea
        context_dict['ikertzailea'] = ensaioa.ikertzailea
        context_dict['komentarioak'] = ensaioa.komentarioak

        #zeintzuk medikamentu dituen agertuko da lehenik
        ensaioa = Ensaioa.objects.get(titulua=ensaioa_titulua)
        medikamentuen_lista = MedikamentuEnsaio.objects.filter(Q(ensaioa=ensaioa))#.values('medikamentua').distinct()
        context_dict['medikamentuak'] = medikamentuen_lista

    except Ensaioa.DoesNotExist:
        pass

   
    return render(request, 'farmaciapp/ensaioa_info_especial.html', context_dict)




@login_required
def dispentsazioak_aztertu(request, ensaioa_titulua):
    #TODO
    #Dispentsazioak bilatzeko formularioa prozesatzen da
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
        # Attempt to grab information from the raw form information.
        # Note that we make use of both ErabiltzaileFormularioa and ErabiltzaileProfilFormularioa.
        dispentsazio_form = DispentsazioFormularioa(data=request.POST)

        # If the form is valid...
        if (dispentsazio_form.is_valid() and 'dataNoiztik' in request.POST):
            paziente_id = None
            pazienteidreal = request.POST['paziente']
            noiztik = request.POST['dataNoiztik']
            noizarte = request.POST['dataNoizArte']
            #konprobatzen da ea pazientea ensaiokoa den edo ez
            #HAU PROBISIONALA DA DESKUBRITU ARTE ZELAN EGIN BEHAR DEN FILTROENA DROP-DOWN LISTE-EAN
            if 'paziente' in request.POST:
                paziente_id = request.POST['paziente']

            try:
                pazienteaEnsaioan = PazienteEnsaio.objects.get(pazientea__ident=request.POST['paziente'], ensaioa__titulua=ensaioa_titulua).pazientea
            except:
                pazienteidreal = paziente_id
                if len(paziente_id)>0:
                    #paziente bat espezifikatu baldin bada, baina ez bada aurkitu
                    flag = 'ez da aurkitu paziente horren dispentsaziorik'
                    #pazienteaEnsaioan = []
                else:
                    #ez bada pazienterik espezifikatu



                    paziente_id = -1
                    pazienteaEnsaioan = PazienteEnsaio.objects.filter(Q(ensaioa__titulua=ensaioa_titulua)).values('pazientea')
                    flag = 'except'
                    #pazienteaEnsaioan = PazienteEnsaio.objects.get(pazientea=request.POST['paziente'], ensaioa__titulua=ensaioa_titulua)
            

            if not pazienteaEnsaioan:
                if paziente_id!=-1:
                    flaga=''
                    #flag = 'if not pazienteaensaioa, if pazienteid!=-1'
            else:
                #Bilaketak egiteko flag hauek erabiliko ditugu, jakiteko erbailtzaileak zein aukera hautatu dituen bilaketarako
                flag = 'else'
                if(request.POST['dataNoiztik']!=''):
                    flagNoiztik = True

                if(request.POST['dataNoizArte']!=''):
                    flagNoizarte = True

                #Ez baldin bada aukeratu pazienterik konkretuki
                if paziente_id == -1:
                    if (flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik']) and Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte']) and Q(paziente=pazienteaEnsaioan))
                        flag = 'if1'
                    if (not flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte']) and Q(paziente=pazienteaEnsaioan))
                        flag = 'if2'
                    if (flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik']) and Q(paziente=pazienteaEnsaioan))
                        flag = 'if3'
                    if (not flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = PazienteDispentsazio.objects.filter(paziente=pazienteaEnsaioan)
                        flag = pazienteaEnsaioan


                #Paziente konkretu bat aukeratu baldin bada
                else:
                    
                    if (flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik']) and Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte']) and Q(pazientea=request.POST['paziente']))
                        flag = 'else1'
                    if (not flagNoiztik and flagNoizarte):
                        bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa__bukaeraData__lte=request.POST['dataNoizArte']) and Q(pazientea=request.POST['paziente']))
                        flag = 'else2'
                    if (flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(dispentsazioa__bukaeraData__gte=request.POST['dataNoiztik']) and Q(pazientea=request.POST['paziente']))
                        flag = 'else3'
                    if (not flagNoiztik and not flagNoizarte):
                        bilaketa_emaitzak = PazienteDispentsazio.objects.filter(Q(paziente=request.POST['paziente']))
                        flag = 'else4'
                



  
        else:
            flag = 'formularioa ez da zuzena'
            bilaketa_emaitzak = []
            print dispentsazio_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        flag = 'ez da post'
        dispentsazio_form = DispentsazioFormularioa()
        bilaketa_emaitzak = []


    # Render the template depending on the context.
    #Honek eramango gaitu medikamentuen bilaketa emaitza erakutsiko duen orrialdera
    return render(request,
            'farmaciapp/dispentsazioak_aztertu.html',
            {'pazienteidreal':pazienteidreal, 'noiztik': noiztik, 'noizarte': noizarte, 'flag': flag, 'paziente_id': paziente_id, 'pazientea': pazienteaEnsaioan, 'ensaioa': ensaioa_titulua, 'bilaketa_emaitzak': bilaketa_emaitzak, 'dispentsazio_form': dispentsazio_form, 'ensaioa_titulua':ensaioa_titulua} )
    #TODO


@login_required
def dispentsazioa_info(request, ensaioa_titulua, dispentsazioa_ident):
    #TODO
    #Hemen dispentsazioaren informazioa ikusi ahalko da
    context_dict = {}
    context_dict['dispentsazioa'] = dispentsazioa_ident
    context_dict['ensaioa'] = ensaioa_titulua
    context_dict['hasieraData'] = None
    context_dict['bukaeraData'] = None
    context_dict['pazientea'] = None
    
      
    try:
        paz_dis = PazienteDispentsazio.objects.get(dispentsazioa__ident=dispentsazioa_ident)
        paziente_id = paz_dis.paziente

        context_dict['dispentsazioa'] = dispentsazioa_ident
        context_dict['ensaioa'] = ensaioa_titulua
        context_dict['hasieraData'] = Dispentsazioa.objects.get(ident=dispentsazioa_ident).hasieraData
        context_dict['bukaeraData'] = Dispentsazioa.objects.get(ident=dispentsazioa_ident).bukaeraData
        context_dict['pazientea'] = paziente_id
        
       

    except PazienteDispentsazio.DoesNotExist:
        pass

   
    return render(request, 'farmaciapp/dispentsazioa_info.html', context_dict)






@login_required
def errezeta_sortu_ensaiotik(request, ensaioa_titulua):
    #TODO
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    sortuta = False
    mezua = ''
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both ErabiltzaileFormularioa and ErabiltzaileProfilFormularioa.
        errezeta_form = ErrezetaBerriEnsaiotikFormularioa(data=request.POST)

        # If the two forms are valid...
        if errezeta_form.is_valid():
            # Save the user's form data to the database.
            #Bilatu behar da ea ensaio horrentzako errezeta hori sortuta dagoen, berdina ez sortzeko
            ensaioa = Ensaioa.objects.get(titulua=ensaioa_titulua)
            pazientea = Pazientea.objects.get(ident=request.POST['pazientea'])
            try:
                ensaioerrezeta = EnsaioErrezeta.objects.get(ensaioa=ensaioa, pazientea=pazientea, preskripzioData=request.POST['preskripzioData'], hurrengoPreskripzioData=request.POST['hurrengoPreskripzioData'])
                mezua = 'Errezeta hori sortuta dago!'
            except:
                errezeta = errezeta_form.save(commit=False)
                errezeta.ensaioa = ensaioa
                errezeta.pendiente = 'Pendiente'
                errezeta.sortzailea = request.user
                #errezeta.save()

              
                # Now we save the UserProfile model instance.
                errezeta.save()

                # Update our variable to tell the template registration was successful.
                sortuta = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print errezeta_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        errezeta_form = ErrezetaBerriEnsaiotikFormularioa()
    # Render the template depending on the context.
    #Erbailtzaile mota konprobatu behar da
        #Farmazia zerbitzukoa bada, orrialde mota bat erakutsiko da
        #Ez bada Farmazia zerbitzukoa, beste bat

    #Jakiteko zein motako erabiltzailea den
    #erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    #farmazia = 'Farmazia'
    return render(request,
            'farmaciapp/errezeta_ensaiotik.html',
            {'sortuta': sortuta, 'mezua':mezua, 'errezeta_form': errezeta_form, 'sortuta': sortuta, 'titulua':ensaioa_titulua})#, 'mota':erabiltzaile_mota, 'farmazia':farmazia} )




@login_required
def errezeta_sortu_ensaiotik_botoia(request, ensaioa_titulua):

    errezeta_form = ErrezetaBerriEnsaiotikFormularioa()
    #Ensaioa sortzeko formularioaren orrialdea erakutsiko da
    return render(request, 'farmaciapp/errezeta_ensaiotik.html', {'errezeta_form':errezeta_form, 'titulua':ensaioa_titulua})


@login_required
def medikamentuak_gehitu_ensaioari_botoia(request, ensaioa_titulua):
    #TODO

    medikamentua_form = MedikamentuBerriFormularioa()
    #Behintzat medikamentuaren titulua espezifikatzen bada, medikamentuaren gehikuntza tratatuko da
    if(request.method == 'POST'):
        if(request.POST['ident']!=''):
            medikamentua_form = MedikamentuBerriFormularioa(data=request.POST)

            # If the form is valid...
            if medikamentua_form.is_valid():
                # Save the user's form data to the database.
                #errezeta_form.ensaioa = ensaioa_titulua
                medikamentua = medikamentua_form.save()
                medikamentua.save()

                #Orain medikamentuEnsaio modeloaren instantzia bat sortu behar da, erlazioa egiteko
                ensaioa = Ensaioa.objects.get(titulua=ensaioa_titulua)
                medikamentuEnsaio = MedikamentuEnsaio(medikamentua=medikamentua, ensaioa=ensaioa)
                medikamentuEnsaio.save()
                # Update our variable to tell the template registration was successful.
                sortuta = True

            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
            else:
                print medikamentua_form.errors
    #Lehen aldia bada, eta ez bada espezifikatu titulorik, formularioa erakutsi beharko da orrialdean
    else:
        medikamentua_form = MedikamentuBerriFormularioa()

    #zeintzuk medikamentu dituen agertuko da lehenik
    ensaioa = Ensaioa.objects.get(titulua=ensaioa_titulua)
    medikamentuen_lista = MedikamentuEnsaio.objects.filter(Q(ensaioa=ensaioa))#.values('medikamentua').distinct()
    
    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    #Ensaioari medikamentuak gehitzeaz arduratuko den orrialdera eramango gaitu
    return render(request, 'farmaciapp/medikamentuak_gehitu_ensaioari.html', {'mota':erabiltzaile_mota, 'farmazia':farmazia, 'medikamentua_form':medikamentua_form, 'medikamentuen_lista': medikamentuen_lista, 'titulua':ensaioa_titulua})













@login_required
def ensaioen_historikoa_ikusi_botoia(request):
    #Honek eramango gaitu ensaioen historikoa erakutsiko duen orrialdera
    return render(request, 'farmaciapp/ensaioen_historikoa.html', {})


@login_required
def medikamentuak_kontsultatu_botoia(request):
    #TODO
    #Honek eramango gaitu medikamentuen kontsulta kudeatuko duen orrialdera

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    return render(request, 'farmaciapp/medikamentu_menua.html', {'mota':erabiltzaile_mota, 'farmazia':farmazia})

@login_required
def medikamentuak_bilatu(request):
    
    ensaioa_id = ''
    ensaioa = ''
    ondo = ''
    if 'ensaioa' in request.POST:
        ensaioa_id = request.POST['ensaioa']

        try:
            ensaioa = Ensaioa.objects.get(titulua=ensaioa_id)
        except:
            ensaioa_id = -1
            ensaioa = None

    #Honek eramango gaitu errezetaren sorkuntza kudeatuko duen orrialdera
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both ErabiltzaileFormularioa and ErabiltzaileProfilFormularioa.
        medikamentu_bilaketa_form = MedikamentuBilaketaFormularioa(data=request.POST)
        medikamentu_bilaketa_form2 = MedikamentuBilaketaFormularioa2(data=request.POST)

        # If the two forms are valid...
        if ((medikamentu_bilaketa_form.is_valid() or request.POST['ident'] != '') and medikamentu_bilaketa_form2.is_valid()):
           


            if(ensaioa!=None):
                ondo = 'ensaioa!=none'

                bilaketa_emaitzak = Medikamentua.objects.filter(Q(medikamentua_ensaioan__ensaioa=ensaioa) & Q(ident__icontains=request.POST['ident']) & Q(kit__icontains=request.POST['kit']) & Q(lote__icontains=request.POST['lote']) & Q(kaduzitatea__icontains=request.POST['kaduzitatea']) & Q(bidalketaZenbakia__icontains=request.POST['bidalketaZenbakia']) & Q(bidalketaData__icontains=request.POST['bidalketaData']))
                    
                ondo = bilaketa_emaitzak

            else:
                bilaketa_emaitzak = Medikamentua.objects.filter(Q(ident__icontains=request.POST['ident']) & Q(kit__icontains=request.POST['kit']) & Q(lote__icontains=request.POST['lote']) & Q(kaduzitatea__icontains=request.POST['kaduzitatea']) & Q(bidalketaZenbakia__icontains=request.POST['bidalketaZenbakia']) & Q(bidalketaData__icontains=request.POST['bidalketaData']))

  
        else:
            bilaketa_emaitzak = []
            ondo = 'ez'

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        medikamentu_bilaketa_form = MedikamentuBilaketaFormularioa()
        medikamentu_bilaketa_form2 = MedikamentuBilaketaFormularioa2()
        bilaketa_emaitzak = []
        ondo = 'ez da POST'


    # Render the template depending on the context.

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'


    #Honek eramango gaitu medikamentuen bilaketa emaitza erakutsiko duen orrialdera
    return render(request,
            'farmaciapp/medikamentuak_bilatu.html',
            {'mota':erabiltzaile_mota, 'farmazia':farmazia, 'ondo':ondo, 'ensaioa_id': ensaioa_id, 'ensaioa': ensaioa, 'bilaketa_emaitzak': bilaketa_emaitzak, 'medikamentu_bilaketa_form': medikamentu_bilaketa_form, 'medikamentu_bilaketa_form2': medikamentu_bilaketa_form2} )
    #TODO


@login_required
def medikamentua_info(request, medikamentua_ident):
    #TODO
    #Medikamentuari dagokion informazioa agertuko da
    
    context_dict = {}
    context_dict['ident'] = None
    context_dict['kit'] = None
    context_dict['lote'] = None
    context_dict['kaduzitatea'] = None
    context_dict['bidalketaZenbakia'] = None
    context_dict['bidalketaData'] = None

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    context_dict['mota'] = erabiltzaile_mota
    context_dict['farmazia'] = farmazia
    
      
    try:
        medikamentua = Medikamentua.objects.get(ident=medikamentua_ident)
        context_dict['ident'] = medikamentua.ident
        context_dict['kit'] = medikamentua.kit
        context_dict['lote'] = medikamentua.lote
        context_dict['bidalketaZenbakia'] = medikamentua.bidalketaZenbakia
        context_dict['bidalketaData'] = medikamentua.bidalketaData
        

    except Medikamentua.DoesNotExist:
        pass


   
    return render(request, 'farmaciapp/medikamentua_info.html', context_dict)








#TODO

#@login_required
#def errezeta_sortu_botoia(request):
#    #Honek eramango gaitu errezetaren sorkuntza kudeatuko duen orrialdera
#    #TODO
#    return render(request, 'farmaciapp/errezeta.html', {})


@login_required
def errezeta_pendienteak_kontsultatu(request):
    #TODO
    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    #Pendiente dauden Errezetak aterako dira
    errezeta_pendienteak = EnsaioErrezeta.objects.filter(Q(pendiente='Pendiente'))

    return render(request, 'farmaciapp/errezeta_pendienteak.html', {'errezeta_pendienteak': errezeta_pendienteak, 'farmazia':farmazia, 'mota': erabiltzaile_mota})


@login_required
def errezeta_sortu(request):
    #TODO
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    sortuta = False
    mezua = ''

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both ErabiltzaileFormularioa and ErabiltzaileProfilFormularioa.
        errezeta_form = ErrezetaBerriFormularioa(data=request.POST)

        # If the two forms are valid...
        if errezeta_form.is_valid():
            # Save the user's form data to the database.
            ensaioa = Ensaioa.objects.get(titulua=request.POST['ensaioa'])
            pazientea = Pazientea.objects.get(ident=request.POST['pazientea'])
            try:
                ensaioerrezeta = EnsaioErrezeta.objects.get(ensaioa=ensaioa,pazientea=pazientea, preskripzioData=request.POST['preskripzioData'], hurrengoPreskripzioData=request.POST['hurrengoPreskripzioData'])
                mezua = 'Errezeta Hori sortuta dago!'
            except:
               
            
                errezeta = errezeta_form.save(commit=False)
                errezeta.sortzailea = request.user


                  
                # Now we save the UserProfile model instance.
                errezeta.save()

                # Update our variable to tell the template registration was successful.
                sortuta = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print errezeta_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        errezeta_form = ErrezetaBerriFormularioa()

    # Render the template depending on the context.
    #Erbailtzaile mota konprobatu behar da
        #Farmazia zerbitzukoa bada, orrialde mota bat erakutsiko da
        #Ez bada Farmazia zerbitzukoa, beste bat

    #Jakiteko zein motako erabiltzailea den
    #erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    #farmazia = 'Farmazia'
    return render(request,
            'farmaciapp/errezeta.html',
            {'mezua': mezua, 'errezeta_form': errezeta_form, 'sortuta': sortuta})#, 'mota':erabiltzaile_mota, 'farmazia':farmazia} )


@login_required
def errezeta_info(request, errezeta_ident):
    #TODO
    #Hemen erakutsiko da errezetari dagokion informazioa

    context_dict = {}

    context_dict['errezeta_ident'] = errezeta_ident

    context_dict['ensaioa'] = None
    context_dict['pazientea_ident'] = None
    context_dict['preskripzioData'] = None
    context_dict['hurrengoPreskripzioData'] = None
    context_dict['paziente_pisua'] = None

    #Dosiaren kalkulua: TODO
    #Jarri beharko litzateke medikamentuentzako eremu bat, farmazeutikoak bete ahal izateko
    #TODO

    try:
        errezeta = EnsaioErrezeta.objects.get(ident=errezeta_ident)
        context_dict['ensaioa'] = errezeta.ensaioa
        context_dict['pazientea_ident'] = errezeta.pazientea
        context_dict['preskripzioData'] = errezeta.preskripzioData
        context_dict['hurrengoPreskripzioData'] = errezeta.hurrengoPreskripzioData
        #Dosiaren kalkulua: TODO

        pazientea = Pazientea.objects.get(ident=errezeta.pazientea.ident)
        context_dict['paziente_pisua'] = pazientea.pisua

        #Jakiteko zein erabiltzailek sortu duen errezeta
        context_dict['errezetaren_sortzailea'] = errezeta.sortzailea
        context_dict['errezeta_form'] = ErrezetaModifikatuFormularioa(initial={'ensaioa':errezeta.ensaioa, 'pazientea':errezeta.pazientea, 'pazientearen_pisua':pazientea.pisua, 'preskripzioData':errezeta.preskripzioData, 'hurrengoPreskripzioData':errezeta.hurrengoPreskripzioData})

    except EnsaioErrezeta.DoesNotExist:
        pass

    #Jakiteko zein erabiltzaile den
    #context_dict['erabiltzailea'] = ErabiltzaileProfila.objects.get(erabiltzailea=request.user)
    
    #Jakiteko zein motako erabiltzailea den
    context_dict['mota'] = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    context_dict['farmazia'] = 'Farmazia'


    return render(request, 'farmaciapp/errezeta_info.html', context_dict)


@login_required
def errezeta_onartu(request, errezeta_ident):
    #TODO
    #Hemen errezeta onartu beharko litzateke Farmazeutikoaren bidez, dispentsaziorako beharrezko informazioa gehituz
    #Hori falta da...
    ensaioa = Ensaioa.objects.get(titulua=request.POST['ensaioa'])
    
    hasieraData = parser.parse(request.POST['preskripzioData']).date()#datetime.datetime.strptime(request.POST['preskripzioData'], '%b %d, %Y')
     
    bukaeraData = parser.parse(request.POST['hurrengoPreskripzioData']).date()#datetime.datetime.strptime(request.POST['hurrengoPreskripzioData'], '%b %d, %Y')
     

    hasieraData = hasieraData.strftime('%Y-%m-%d')
    bukaeraData = bukaeraData.strftime('%Y-%m-%d')

    dispentsazioa = Dispentsazioa(hasieraData=hasieraData, bukaeraData=bukaeraData, ensaioa=ensaioa)
    dispentsazioa.save()

    #TODO: PAZIENTEDISPENTSAZIO ERE EGIN BEHAR DA

    #Errezetaren egoera 'Pendiente'-tik 'Dispentsatuta'-ra pasatu behar da
    ensaio_errezeta = EnsaioErrezeta.objects.get(ident=errezeta_ident)
    ensaio_errezeta.pendiente = 'Dispentsatuta'
    ensaio_errezeta.save()

    #Pazientea ensaioarekin lotuta dagoela ere jarri behar da
    pazientea = Pazientea.objects.get(ident=request.POST['pazientea'])

    #PazienteDispentsazio erlazioa ere erregistratu behar da, baina momentuz ez dut medikamenturik gehituko
    paziente_dispentsazio = PazienteDispentsazio(ident=dispentsazioa.ident, dispentsazioa=dispentsazioa, paziente=pazientea)
    paziente_dispentsazio.save()

    try:
        paziente_ensaio = PazienteEnsaio.objects.get(pazientea=pazientea, ensaioa=ensaioa)

    #Ez baldin badago erregistratuta jada, erregistratu egin behar da
    except PazienteEnsaio.DoesNotExist:
        paziente_ensaio = PazienteEnsaio(pazientea=pazientea, ensaioa=ensaioa)
        paziente_ensaio.save()


    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    return render(request, 'farmaciapp/errezeta_pendienteak.html', {'mota':erabiltzaile_mota, 'farmazia':farmazia})


@login_required
def errezeta_modifikatu(request, errezeta_ident):
    #Hemen aurretik zeuzkan datuan jarriko ditugu eta aukera emango zaio erabiltzaileari aldatzeko
    mezua = ''
    sortzailea = ''
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        sortzailea = request.POST['errezetaren_sortzailea']

        # Attempt to grab information from the raw form information.
        # Note that we make use of both ErabiltzaileFormularioa and ErabiltzaileProfilFormularioa.
        errezeta_form = ErrezetaModifikatuFormularioa(data=request.POST)
        if errezeta_form.is_valid():
            # Save the user's form data to the database.
            ensaioa = Ensaioa.objects.get(titulua=request.POST['ensaioa'])
            pazientea = Pazientea.objects.get(ident=request.POST['pazientea'])
            try:
                #Balio berriekin moldatu nahi den errezeta existitzen den edo ez konprobatuko da
                ensaioerrezeta = EnsaioErrezeta.objects.get(ensaioa=ensaioa,pazientea=pazientea, preskripzioData=request.POST['preskripzioData'], hurrengoPreskripzioData=request.POST['hurrengoPreskripzioData'])
                mezua = 'Errezeta Hori sortuta dago!'
            except:
                #Aurreko datuekin geneukan errezeta hartu eta balioak aldatuko dizkiogu
                errezeta = EnsaioErrezeta.objects.get(ensaioa__titulua=request.POST['ensaioaZ'], pazientea__ident=request.POST['pazientea_identZ'], preskripzioData=request.POST['preskripzioDataZ'], hurrengoPreskripzioData=request.POST['hurrengoPreskripzioDataZ'])
                #errezeta = errezeta_form.save()
                errezeta.ensaioa = ensaioa
                errezeta.pazientea = pazientea
                errezeta.preskripzioData = request.POST['preskripzioData']
                errezeta.hurrengoPreskripzioData = request.POST['hurrengoPreskripzioData']
                  
                # Now we save the UserProfile model instance.
                errezeta.save()

                # Update our variable to tell the template registration was successful.
                sortuta = True
                mezua = 'Errezeta ondo eguneratu da!'

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print errezeta_form.errors

    else:
        errezeta_form = ErrezetaModifikatuFormularioa()

    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'
    ensaioa = request.POST['ensaioa']
    pazientea = request.POST['pazientea']
    pazientePisua = request.POST['pazientearen_pisua']
    preskripzioData = request.POST['preskripzioData']
    hurrengoPreskripzioData = request.POST['hurrengoPreskripzioData']

    return render(request,
            'farmaciapp/errezeta_info.html',
            {'errezetaren_sortzailea':sortzailea, 'mezua':mezua, 'errezeta_ident':errezeta_ident, 'mota':erabiltzaile_mota, 'farmazia':farmazia, 'errezeta_form':errezeta_form, 'ensaioa':ensaioa, 'pazientea_ident':pazientea, 'preskripzioData':preskripzioData, 'hurrengoPreskripzioData':hurrengoPreskripzioData, 'paziente_pisua':pazientePisua})#, 'mota':erabiltzaile_mota, 'farmazia':farmazia} )





@login_required
def medikamentuaren_ensaioak_ikusi(request, medikamentua_ident):
    #TODO
    #Medikamentua zein ensaiorekin dagoen erlazionatuta ikusiko da
    ensaio_lista = MedikamentuEnsaio.objects.filter(Q(medikamentua__ident=medikamentua_ident)).values('ensaioa').distinct()


    #Jakiteko zein motako erabiltzailea den
    erabiltzaile_mota = ErabiltzaileProfila.objects.filter(erabiltzailea=request.user)[0].zerbitzua
    #aldagai hau erabiliko da html-an konprobazioa egiteko
    farmazia = 'Farmazia'

    #Honek erakutsiko du medikamentu horren ensaioak agertzen diren orrialdea
    return render(request, 'farmaciapp/medikamentuaren_ensaioak.html', {'mota':erabiltzaile_mota, 'farmazia':farmazia, 'medikamentua':medikamentua_ident, 'ensaio_lista': ensaio_lista})




@login_required
def aukeratutako_ensaioak_ezabatu(request):
    #TODO
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

    return render(request, 'farmaciapp/ensaioak_bilatu.html', {'mota':erabiltzaile_mota, 'farmazia':farmazia, 'ensaio_bilaketa_form':ensaio_bilaketa_form, 'ensaio_bilaketa_form2':ensaio_bilaketa_form2, 'ensaio_lista': ezabatu_beharreko_ensaio_lista})


#@login_required
#def aukeratutako_errezetak_ezabatu(request):
    #Hau Errezeta sortu duenak egin beharko luke soilik
