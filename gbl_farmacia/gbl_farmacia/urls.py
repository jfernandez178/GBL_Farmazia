from django.conf.urls import patterns, include, url
from django.contrib import admin

#Hemen gure gbl_farmacia proiektua lotuko dugu gure aplikazio desberidnekin (kasu honetan, farmaciapp-ekin)
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gbl_farmacia.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^farmaciapp/', include('farmaciapp.urls')),

)
