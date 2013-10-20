# -*- coding: utf-8 *-*
from django.conf.urls import patterns, url

urlpatterns = patterns('',
   url(r'^$', 'cine.views.home', name='home'),
   url(r'^get-peliculas/$', 'cine.views.jsonpeliculas', name='peliculas'),
   url(r'^get-cines/$', 'cine.views.jsoncines', name='cines'),
   url(r'^get-horarios/$', 'cine.views.jsonhorarios', name='horarios'),
   url(r'^sincronizar/$', 'cine.views.sincronizar', name='home'),
)
