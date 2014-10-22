meteopy
================

# Sitio de estaciones meteorologicas.

## How to.



## Autores

[Julian Caceres](https://github.com/juliancpy) - 
[Teddy Limousin](https://github.com/)

## Pasos.
* Se presume la previa instalacion de python. 

		$ Python version: 2.7

* Se procede a la instalacion de [virtualenv](https://pypi.python.org/pypi/virtualenv), la cual nos ayudara con la instalacion de Django.
* Luego de la instalacion de virtualenv sin importar la manera que lo hayas hecho, creamos un nuevo entorno virtual. 

        $ mkdir carpeta_nuestro_proyecto
        $ cd carpeta_nuestro_proyecto
        $ virtualenv env	

* si no tenemos asignado virtualenv en el $PATH  del sistema. (hacerlo de la siguiente manera)

		$ python virtualenv.py --distribute env


* Ahora ya contamos con nuestro entorno virtual. solo necesitamos activarlo y comenzar la instalación de todo lo necesario para ejecutar nuestro proyecto de django.

        $ source ./env/bin/activate

* Si deseas descativar solo basta ejecutar el comando:

		$deactivate

* A continuación procedemos a la instalacion de Django.

		$ pip install django

* Deberia instalar la ultima version de Django, el cual estaria en tu virtualenv. Para confirmarlo:

		$which django-admin.py

* Todo listo para trabajar con un proyecto de Django, en nuestro caso los archivos para el mismo se encuentran disponibles en el repositorio github.		
		
## Realizar clone desde repositorio.

Como ya contamos con los archivos de nuestro proyecto en el repositorio [github](https://github.com/juliancpy/meteopy) simplemente realizamos una copia en nuestra maquina.

* Lo realizamos de la siguiente manera.

		$ git clone git@github:YOUR_NICK_NAME/meteopy.git [Para mas detalles](https://code.djangoproject.com/wiki/CollaborateOnGithub)

Ahora que contamos con las fuentes relacionadas al proyecto tendremos que instalar las librerias especificas relacionadas al proyecto.

* Relacionadas a filtros en rango de fechas para el admin.

		$ pip install django-daterange-filter 

* Libreria utilizada a modo de prueba para el sistema de graficos. 		

		$ pip install django_chartit

## Base de datos.

* Uno de los ultimos pasos a realizar es simplemente crear la base de datos en nuestro servidor mysql. 

		$ create database meteopy
Una vez hecho esto tendremos que verificar si las credenciales de acceso a la base de datos corresponden. 
Esto lo podemos ver en el archivo settings del proyecto. 

* Si precisamos de datos para la prueba del sistema podriamos simplemente migrar las que se encuentran disponibles en el repositorio.

		$ mysql -uUSER -pPASSWD meteopy < meteopy.sql

## Prueba.

* Si todo esta correcto bastara con ejecutar el siguiente comando y probar.
 
		$ python manage.py runserver.

* [Reportes Bug](http://dev.ingejc.com/projects/meteopy)
* [Feature requests](http://dev.ingejc.com/projects/meteopy)

## Copyright and license

Copyright (C) 2013-2014 meteopy

