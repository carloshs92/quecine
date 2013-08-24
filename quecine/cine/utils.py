# -*- coding: utf-8 *-*
try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup
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
    Soup = BeautifulSoup
    return Soup(html_text)
