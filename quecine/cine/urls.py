# -*- coding: utf-8 *-*
from django.conf.urls import patterns, url, include
from rest_framework import routers
from .views import CineViewSet, PeliculaViewSet, HorarioViewSet, SedeViewSet


router = routers.DefaultRouter()
router.register(r'sedes', SedeViewSet)
router.register(r'cines', CineViewSet)
router.register(r'peliculas', PeliculaViewSet)
router.register(r'horarios', HorarioViewSet)


urlpatterns = patterns('',
   url(r'^$', 'cine.views.home', name='home'),
   url(r'^jsonhorarios/$', 'cine.views.jsonhorarios', name='jsonhorarios'),
   url(r'^', include(router.urls)),
   url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   url(r'^sincronizar/$', 'cine.views.sincronizar', name='home'),
)
