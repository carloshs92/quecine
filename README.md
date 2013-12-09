Que Cine
=======
Este aplicativo mapea las paginas web de cines (por el momento solo cineplanet y algo de cinemark)
para luego almacenar los cines, horarios y peliculas en una base ed datos local

INSTALACION de aplicativo

*Configurar el settings.py acorde a su base de datos y luego ejecutar lo sgte:

1) virtualenv venv --distribute
2) source venv/bin/activate
3) pip install -r requirements.txt

Listo! El aplicativo deberia estar funcionando

La carpeta app contiene el aplicativo firefox os
La carpeta que cine contiene el aplicativo django que mapea los cines

Para sincronizar la data mapeada de la web ejecutar 127.0.0.1:8000/sincronizar 
