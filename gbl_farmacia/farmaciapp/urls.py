from django.conf.urls import patterns, url
from farmaciapp import views

#Web-aplikazioko orrialdeen url-ak definitzen dira hemen
urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^erregistratu/$', views.erregistratu, name='erregistratu'),
        url(r'^login/$', views.erabiltzailea_login, name='login'),
        url(r'^logout/$', views.erabiltzailea_logout, name='logout'),
        url(r'^aukera_menua/$', views.aukera_menua, name='aukera_menua'),
        url(r'^aukera_menua/ensaio_kontsulta/$', views.ensaioak_kontsultatu_botoia, name='ensaio_kontsulta'),
        url(r'^aukera_menua/medikamentu_kontsulta/$', views.medikamentuak_kontsultatu_botoia, name='medikamentu_kontsulta'),
        url(r'^aukera_menua/medikamentu_kontsulta/medikamentu_bilaketa/$', views.medikamentuak_bilatu, name='medikamentu_bilaketa'),
        url(r'^aukera_menua/medikamentu_kontsulta/medikamentu_bilaketa/medikamentua/(?P<medikamentua_ident>\w+)/$', views.medikamentua_info, name='medikamentuaren_informazioa'),
        url(r'^aukera_menua/medikamentu_kontsulta/medikamentu_bilaketa/medikamentua/(?P<medikamentua_ident>\w+)/ensaioak/$', views.medikamentuaren_ensaioak_ikusi, name='medikamentuaren_ensaioak'),
        #url(r'^aukera_menua/errezeta/$', views.errezeta_sortu_botoia, name='errezeta'),
        url(r'^aukera_menua/ensaio_kontsulta/ensaio_bilaketa/$', views.ensaioak_bilatu, name='ensaio_bilaketa'),
        url(r'^aukera_menua/ensaio_kontsulta/ensaio_sorkuntza/$', views.ensaioa_sortu, name='ensaio_sorkuntza'),
        url(r'^aukera_menua/errezeta_pendienteak_kontsultatu/$', views.errezeta_pendienteak_kontsultatu, name='errezeta_pendienteen_kontsulta'),
        url(r'^aukera_menua/errezeta_sorkuntza/$', views.errezeta_sortu, name='errezeta_sorkuntza'),
        url(r'^aukera_menua/errezeta_pendienteak_kontsultatu/errezeta/(?P<errezeta_ident>\w+)/$', views.errezeta_info, name='errezetaren_informazioa'),
        url(r'^aukera_menua/errezeta_pendienteak_kontsultatu/errezeta/(?P<errezeta_ident>\w+)/errezeta_onartu/$', views.errezeta_onartu, name='errezetaren_onarpena'),
        url(r'^aukera_menua/ensaio_kontsulta/ensaio_bilaketa/ensaioa/(?P<ensaioa_titulua>\w+)/$', views.ensaioa_info, name='ensarioaren_informazioa'),
        url(r'^aukera_menua/errezeta_pendienteak_kontsultatu/errezeta/(?P<errezeta_ident>\w+)/modifikatu/$', views.errezeta_modifikatu, name='errezetaren_modifikazioa'),
        url(r'^aukera_menua/ensaio_kontsulta/ensaioen_historikoa/$', views.ensaioen_historikoa_ikusi_botoia, name='ensaioen_historikoaren_kontsulta'),
        #url(r'^aukera_menua/ensaio_kontsulta/ensaio_sorkuntza/ensaio_sorkuntza_formularioa/$', views.ensaioa_sortu2, name='ensaio_sorkuntza_formularioa')
        
        url(r'^aukera_menua/ensaio_kontsulta/ensaio_bilaketa/ensaioa/(?P<ensaioa_titulua>\w+)/dispentsazioak/$', views.dispentsazioak_aztertu, name='dispentsazioen_azterketa'),
        url(r'^aukera_menua/ensaio_kontsulta/ensaio_bilaketa/ensaioa/(?P<ensaioa_titulua>\w+)/dispentsazioak/(?P<dispentsazioa_ident>\w+)/$', views.dispentsazioa_info, name='dispentsazioaren_informazioa_ikusi'),
        url(r'^aukera_menua/ensaio_kontsulta/ensaio_bilaketa/ensaioa/(?P<ensaioa_titulua>\w+)/errezeta_berria_botoia/$', views.errezeta_sortu_ensaiotik_botoia, name='errezeta_sorkuntza_ensaiotik_botoia'),        
        url(r'^aukera_menua/ensaio_kontsulta/ensaio_bilaketa/ensaioa/(?P<ensaioa_titulua>\w+)/errezeta_berria/$', views.errezeta_sortu_ensaiotik, name='errezeta_sorkuntza_ensaiotik'),        
        url(r'^aukera_menua/ensaio_kontsulta/ensaio_bilaketa/ensaioa/(?P<ensaioa_titulua>\w+)/medikamentuak/$', views.medikamentuak_gehitu_ensaioari_botoia, name='medikamentu_gehiketa_ensaioan'),
        url(r'^aukera_menua/ensaio_kontsulta/ensaio_bilaketa/ezabatu/$', views.aukeratutako_ensaioak_ezabatu, name='aukeratutako_ensaioen_ezabaketa'),
)