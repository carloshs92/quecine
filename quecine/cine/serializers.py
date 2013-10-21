# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Cine, CinePeli, Pelicula, Sede


class SedeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sede
        fields = ('cod', 'sede', 'logo')


class CineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cine
        fields = ('cod', 'cine', 'lat', 'lon', 'direccion', 'sede')


class PeliculaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pelicula
        fields = ('cod', 'pelicula', 'trailer')


class HorarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CinePeli
        fields = ('pelicula', 'cine', 'tipo', 'horarios')