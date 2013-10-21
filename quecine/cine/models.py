from django.db import models
from .utils import SEDES


class Sede(models.Model):
    cod = models.AutoField(primary_key=True)
    sede = models.CharField(max_length=4, choices=SEDES)
    logo = models.CharField(max_length=200, null=True, blank=True)


class Cine(models.Model):
    cod = models.AutoField(primary_key=True)
    cine = models.CharField(max_length=200)
    lat = models.CharField(max_length=50, null=True, blank=True)
    lon = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    sede = models.ForeignKey(Sede, related_name='cine_sede')


class Pelicula(models.Model):
    cod = models.AutoField(primary_key=True)
    pelicula = models.CharField(max_length=300)
    trailer = models.CharField(max_length=400, null=True, blank=True)


class CinePeli(models.Model):
    pelicula = models.ForeignKey(Pelicula, related_name='cinepeli_pelicula')
    cine = models.ForeignKey(Cine, related_name='cinepeli_cine')
    tipo = models.CharField(max_length=10)
    horarios = models.CharField(max_length=300)




