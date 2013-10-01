# -*- coding: utf-8 *-*
try:
    from bs4 import BeautifulSoup as Soup
except:
    from BeautifulSoup import BeautifulSoup as Soup
import urllib2


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
    return Soup(html_text)

############ DATOS ESTATICOS

CINEPLANET = 01
CINEMARK = 02

SEDES = (
        (CINEPLANET, 'cineplanet'),
        (CINEMARK, 'cinemark')
    )

URL_PELICULAS = (
        (CINEPLANET, 'http://www.cineplanet.com.pe/cartelera.php'),
        (CINEMARK, 'Cinemark')
    )

URL_SEDES = (
        (CINEPLANET, 'http://www.cineplanet.com.pe/nuestroscines.php'),
        (CINEMARK, 'Cinemark')
    )

URL_CARTELERA = (
        (CINEPLANET, 'http://www.cineplanet.com.pe/nuestroscines.php'),
        (CINEMARK, 'Cinemark')
    )