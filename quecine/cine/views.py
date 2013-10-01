# -*- coding: utf-8 *-*

from django.shortcuts import render_to_response
from django.template import RequestContext
from .utils import CINEPLANET
from .utils import getBeautifulSoup, URL_PELICULAS, URL_SEDES, URL_CARTELERA
from .models import Pelicula, Cine, Sede #, CinePeli
import json


def home(request):
    data = dict()
    data['pelicula'] = Pelicula.objects.all()
    data['cine'] = Cine.objects.all()
    return render_to_response(
        'home/index.html', data,
        context_instance=RequestContext(request))


def sincronizar(request):
    Pelicula.objects.all().delete()
    Cine.objects.all().delete()
    #getPeliculas("http://www.cinemark-peru.com/cartelera", 'cinemark')

    sede = Sede.objects.get_or_create(sede=URL_SEDES[CINEPLANET])
    getCines(URL_SEDES[CINEPLANET], CINEPLANET, sede)
    getPeliculas(URL_PELICULAS[CINEPLANET], CINEPLANET, sede)
    getHorarios(URL_CARTELERA[CINEPLANET], CINEPLANET, sede)

    data = dict()
    data['pelicula'] = Pelicula.objects.all()
    data['cine'] = Cine.objects.all()
    return render_to_response(
        'home/data.html', data,
        context_instance=RequestContext(request))


def jsonpeliculas(request):
    peliculas = Pelicula.objects.all()
    return render_to_response(
        'home/json.html', {'peliculas': json.dumps(peliculas)},
        context_instance=RequestContext(request))

####### Utlidades


def getPeliculas(url, cine):
    soup = getBeautifulSoup(url)
    if cine == CINEPLANET:
        # Obtengo Peliculas
        print soup.find_all('td')
        for td in soup.find_all('td', class_="titulo_pelicula"):
            peli = Pelicula(pelicula=td.string.encode('utf-8', 'ignore'))
            peli.save()
    elif cine == 'cinemark':
        for a in soup.find_all('a', class_="black"):
            title = a.string.encode('utf-8', 'ignore')
            if title not in ['Olvidaste tu contraseña?', 'Regístrate', 'Inicio']:
                peli = Pelicula(pelicula=title.upper())
                peli.save()


def getCines(url, cine, sede):
    soup = getBeautifulSoup(url)

    if cine == 'cineplanet':
        for option in soup.find_all('option'):
            Cine.objects.update_or_create(
                cine=option.string.encode('utf-8', 'ignore'),
                sede=sede)
    elif cine == 'cinemark':
        for h2 in soup.find_all('h2', class_='title2'):
            print h2.string.encode('utf-8', 'ignore')


def getHorarios(url, cine):
    soup = getBeautifulSoup(url)

    if cine == 'cineplanet':
        for option in soup.find_all('option'):
            print '######################'
            print option.string.encode('utf-8', 'ignore')
            print '######################'
            peli = option.attrs['value']
            soup = getBeautifulSoup(url + "?complejo=%s" % peli)
            n = 1
            cartelera = dict()

            for a in soup.find_all('a', class_="titulo_pelicula5"):
                var = a.string.encode('utf-8', 'ignore').strip()
                if n % 2 == 0:
                    lista.append(var)
                    cartelera[len(cartelera)+1] = lista
                else:
                    lista = list()
                    lista.append(var)
                n = n + 1
            print cartelera
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
