# -*- coding: utf-8 *-*

from django.shortcuts import render_to_response
from django.template import RequestContext
from .utils import getBeautifulSoup
from .models import Pelicula, Cine, CinePeli
# Create your views here.


def home(request):
    data = dict()
    data['pelicula'] = Pelicula.objects.all()
    data['cine'] = Cine.objects.all()
    return render_to_response(
        'home/index.html', data,
        context_instance=RequestContext(request))


def sincronizar(request):
    #getPeliculas("http://www.cineplanet.com.pe/cartelera.php", 'cineplanet')
    #getCines("http://www.cineplanet.com.pe/nuestroscines.php", 'cineplanet')
    getHorarios("http://www.cineplanet.com.pe/nuestroscines.php", 'cineplanet')
    data = dict()
    data['pelicula'] = Pelicula.objects.all()
    data['cine'] = Cine.objects.all()
    return render_to_response(
        'home/data.html', data,
        context_instance=RequestContext(request))


def getPeliculas(url, cine):
    soup = getBeautifulSoup(url)
    if cine == 'cineplanet':
        # Obtengo Peliculas
        for td in soup.find_all('td', class_="titulo_pelicula"):
            peli = Pelicula(pelicula=td.string.encode('utf-8', 'ignore'))
            peli.save()
    elif cine == 'cinemark':
        for a in soup.find_all('a', class_="black"):
            peli = a.string.encode('utf-8', 'ignore')
            if peli not in ['Olvidaste tu contraseña?','Regístrate','Inicio']:
                print peli


def getCines(url, cine):
    soup = getBeautifulSoup(url)

    if cine == 'cineplanet':
        for option in soup.find_all('option'):
            c = Cine(cine=option.string.encode('utf-8', 'ignore'))
            c.save()
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
