# -*- coding: utf-8 *-*
from django.conf.urls import patterns, url

urlpatterns = patterns('',
   url(r'^$', 'cine.views.home', name='home'),
   url(r'^sincronizar/$', 'cine.views.sincronizar', name='home'),
)