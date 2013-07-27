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


def getCines(url, cine):
    soup = getBeautifulSoup(url)

    if cine == 'cineplanet':
        for option in soup.find_all('option'):
            print option.string.encode('utf-8', 'ignore')


# Defino URL
url = "http://www.cineplanet.com.pe/cartelera.php"

getPeliculas(url, 'cineplanet')

url = "http://www.cineplanet.com.pe/nuestroscines.php"

getCines(url, 'cineplanet')
