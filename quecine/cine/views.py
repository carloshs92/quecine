# -*- coding: utf-8 *-*

from django.shortcuts import render_to_response
from django.template import RequestContext
from .utils import CINEPLANET
from .utils import getBeautifulSoup, URL_PELICULAS, URL_SEDES, URL_CARTELERA
from .models import Pelicula, Cine, Sede, CinePeli
from django.http import (HttpResponse)
import re
from rest_framework import viewsets
from .serializers import (CineSerializer, PeliculaSerializer,
HorarioSerializer, SedeSerializer)
from django.core import serializers


def home(request):
    data = dict()
    data['pelicula'] = Pelicula.objects.all()
    data['cine'] = Cine.objects.all()
    return render_to_response(
        'home/index.html', data,
        context_instance=RequestContext(request))


def jsonhorarios(request):
    data = serializers.serialize("json", CinePeli.objects.all())
    return HttpResponse(data,
             content_type="text/html;charset=utf-8")


def sincronizar(request):
    Pelicula.objects.all().delete()
    Cine.objects.all().delete()
    #getPeliculas("http://www.cinemark-peru.com/cartelera", 'cinemark')
    if not Sede.objects.filter(cod=CINEPLANET).exists():
        sede = Sede(cod=CINEPLANET)
        sede.save()
    sede = Sede.objects.get(cod=CINEPLANET)
    getCines(URL_SEDES[CINEPLANET][1], CINEPLANET, sede)
    getPeliculas(URL_PELICULAS[CINEPLANET][1], CINEPLANET)
    getHorarios(URL_CARTELERA[CINEPLANET][1], CINEPLANET)

    data = dict()
    data['pelicula'] = Pelicula.objects.all()
    data['cine'] = Cine.objects.all()
    return render_to_response(
        'home/data.html', data,
        context_instance=RequestContext(request))


class SedeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer


class CineViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Cine.objects.all()
    serializer_class = CineSerializer


class PeliculaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed.
    """
    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer


class HorarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed.
    """
    queryset = CinePeli.objects.all()
    serializer_class = HorarioSerializer


####### Utlidades


def getPeliculas(url, cine):
    soup = getBeautifulSoup(url)
    if cine == CINEPLANET:
        # Obtengo Peliculas
        for td in soup.find_all('td', class_="titulo_pelicula"):
            raw = td.string.encode('utf-8', 'ignore').strip()
            clean = re.sub(u'(\(?(3D|SUB|DOB|DIG|\\\)\)?)+', '', raw)
            clean = clean.strip()
            if not Pelicula.objects.filter(pelicula__icontains=clean).exists():
                print 'Pelicula Ingresada: ' + clean
                peli = Pelicula(pelicula=clean.lower())
                peli.save()
    elif cine == 'cinemark':
        for a in soup.find_all('a', class_="black"):
            title = a.string.encode('utf-8', 'ignore')
            if title not in ['Olvidaste tu contraseña?', 'Regístrate', 'Inicio']:
                peli = Pelicula(pelicula=title.upper())
                peli.save()


def getCines(url, cine, sede):
    soup = getBeautifulSoup(url)
    if cine == CINEPLANET:
        for option in soup.find_all('option'):
            cine_raw = option.string.encode('utf-8', 'ignore').strip()
            if not Cine.objects.filter(cine__icontains=cine_raw).exists():
                c = Cine(
                    cod=option.attrs['value'],
                    cine=cine_raw,
                    sede=sede)
                c.save()
    elif cine == 'cinemark':
        for h2 in soup.find_all('h2', class_='title2'):
            print h2.string.encode('utf-8', 'ignore')


def getHorarios(url, cine):
    soup = getBeautifulSoup(url)

    if cine == CINEPLANET:
        for option in soup.find_all('option'):
            cinepeli = None
            #print '######################'
            #print option.string.encode('utf-8', 'ignore')
            #print '######################'
            peli = option.attrs['value']
            soup = getBeautifulSoup(url + "?complejo=%s" % peli)
            cine = Cine.objects.get(pk=peli)
            n = 1
            #cartelera = dict()
            cinepeli = None
            for a in soup.find_all('a', class_="titulo_pelicula5"):
                var = a.string.encode('utf-8', 'ignore').strip()
                if n % 2 == 0:
                    horarios = re.sub(u'(\(?(3D|SUB|DOB|DIG)\)?)+', '', var)
                    cinepeli.horarios = horarios
                    cinepeli.save()
                else:
                    cinepeli = CinePeli()
                    regex = re.compile(u'((3D|SUB|DOB|DIG))+')
                    tipo = list()
                    tipo_raw = regex.findall(var)
                    if tipo_raw != 0:
                        for i in range(len(tipo_raw)):
                            tipo.append(tipo_raw[i][0])
                            cinepeli.tipo = ", ".join(str(x) for x in tipo)
                    peli = re.sub(u'(\(?(3D|SUB|DOB|DIG|\\\)\)?)+', '', var)
                    peli = peli.strip()
                    cinepeli.cine = cine
                    #verficando que la pelicula existe
                    if Pelicula.objects.filter(pelicula__icontains=peli).exists():
                        print 'peli buena: ' + peli
                        cinepeli.pelicula = Pelicula.objects.get(pelicula__icontains=peli)
                    else:
                        print 'peli mala: ' + peli
                        cinepeli.pelicula = Pelicula.objects.get(pelicula__icontains=peli[:7])
                n = n + 1
            #print cartelera
    elif cine == 'cinemark':
        for loc in soup.find_all('div', class_="item-block-details"):
            soup = getBeautifulSoup('http://www.cinemark-peru.com%s' % loc.a.attrs['href'])
            print '######################'
            print loc.h2.string.encode('utf-8', 'ignore')
            print '######################'
            for div in soup.find_all('div', class_="movie-prog2"):
                print div.h5.next_element.encode('utf-8', 'ignore')
                print div.h5.span.string
                print div.li.string


