# README #

El objeto de estas notas es explicar para que es este repositorio y
y cómo construir el proyecto.


### Propósito de este repositorio ###

* Este repositorio está pensado para albergar nuestra primera herramienta
* para Trading. Es una transcripción del programa que ya funciona en Matlab
* pero reimplementado y hecho mucho más eficiente y escalable
* Version 0.1
* PD. Este documento está desarrollado con Markdown! No se conforme
* [Aprenda Markdown!!](ht tps://bitbucket.org/tutorials/markdowndemo)

### Instalación DESARROLLO ###

* Lo único que se necesita es un entorno Python 3.5
* Con lo que está en requirements.txt
* En este fichero está también la instalación para PEP-8 (estilo de codificación)
  Si está trabajando con ATOM como editor de Python no olvide instalar el paquete
  para avisar de los warnings de PEP-8 llamado linter-pep8
```
pip install -r requirements.txt
```
### Ejecución de los tests unitarios ###
Para ejecutar los test se pueden ejecutar de la siguiente manera si es a nivel de clase

```
python -m unittest tests.test_datacollection.NetworkTestCase
```

O si es a nivel de paquete:  
```
python -m unittest tests
```
Hay también desglose, por supuesto a nivel de módulo o, en cambio, a nivel de método.
El orden de especificación sería:
paquete , módulo, clase, método


### Instalación PRODUCCIÓN ###

(no aplica)
