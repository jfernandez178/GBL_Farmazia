from django.contrib import admin
from farmaciapp.models import Medikamentua, Pazientea, Dispentsazioa, Ensaioa, ErabiltzaileProfila, PazienteEnsaio, EnsaioErrezeta, PazienteDispentsazio, MedikamentuEnsaio

#Hemen erregistratzen dira gure modeloak, administratzailearen orrian kudeatu ahal izateko
admin.site.register(Medikamentua)
admin.site.register(Pazientea)
admin.site.register(Dispentsazioa)
admin.site.register(Ensaioa)
admin.site.register(ErabiltzaileProfila)
admin.site.register(PazienteEnsaio)
admin.site.register(EnsaioErrezeta)
admin.site.register(PazienteDispentsazio)
admin.site.register(MedikamentuEnsaio)