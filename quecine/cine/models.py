from django.db import models

# Create your models here.


class Cine(models.Model):
    cod = models.AutoField(primary_key=True)
    cine = models.CharField(max_length=200)


class Pelicula(models.Model):
    cod = models.AutoField(primary_key=True)
    pelicula = models.CharField(max_length=300)


class CinePeli(models.Model):
    pelicula = models.ForeignKey(Pelicula)
    cine = models.ForeignKey(Cine)
    horarios = models.CharField(max_length=300)
