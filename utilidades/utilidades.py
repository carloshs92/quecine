# -*- coding: utf-8 *-*
import urllib2
from bs4 import BeautifulSoup


def getBeautifulSoup(url):
    # Agrego agente
    headers = {'User-Agent': 'Mozilla 5.10'}
    # Creo el Request
    request = urllib2.Request(url, None, headers)
    # Consigo la data
    response = urllib2.urlopen(request)
    # Obtengo el HTML
    html_text = response.read()
    # Cierro la conexion
    response.close()
    # Creo el Soup
    return BeautifulSoup(html_text)


def getPeliculas(url, cine):
    soup = getBeautifulSoup(url)
    if cine == 'cineplanet':
        # Obtengo Peliculas
        for td in soup.find_all('td', class_="titulo_pelicula"):
            print td.string.encode('utf-8', 'ignore')
    elif cine == 'cinemark':
        for a in soup.find_all('a', class_="black"):
            peli = a.string.encode('utf-8', 'ignore')
            if peli not in ['Olvidaste tu contraseña?','Regístrate','Inicio']:
                print peli


def getCines(url, cine):
    soup = getBeautifulSoup(url)

    if cine == 'cineplanet':
        for option in soup.find_all('option'):
            print option.string.encode('utf-8', 'ignore')
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


def testingCineplanet():
    print "\n\n\n\n#-------CINEPLANET---------#\n\n"

    url = "http://www.cineplanet.com.pe/cartelera.php"

    print "\n#-------PELICULAS---------#\n"
    getPeliculas(url, 'cineplanet')

    url = "http://www.cineplanet.com.pe/nuestroscines.php"

    print "\n#-------CINES---------#\n"
    getCines(url, 'cineplanet')

    print "\n#-------HORARIOS---------#\n"
    getHorarios(url, 'cineplanet')


def testingCinemark():
    print "\n\n\n\n#-------CINEMARK---------#\n\n"
    url = 'http://www.cinemark-peru.com/cartelera'

    print "\n#-------PELICULAS---------#\n"
    getPeliculas(url, 'cinemark')

    url = 'http://www.cinemark-peru.com/cines'

    print "\n#-------CINES---------#\n"
    getCines(url, 'cinemark')

    print "\n#-------HORARIOS---------#\n"
    getHorarios(url, 'cinemark')