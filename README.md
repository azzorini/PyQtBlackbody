# PyQtBlackbody

Pequeña interfaz gráfica en Python para entender mejor la radiación de un cuerpo negro.

## Dependencias

Para poder ejecutar esta aplicación es necesario tener instalado Python y las siguientes dependencias:

1. `PyQt5`: Para poder mostrar y manejar la interfaz gráfica.
2. `matplotlib`: Para poder mostrar el espectro del cuerpo negro.
3. `scipy`: Proporciona varias constantes físicas que se usan a lo largo del programa.
4. `numpy`: Para realizar los cálculos del espectro que se ha de mostrar.

## ¿Qué tiene el programa?

El programa muestra el espectro de un cuerpo negro para una cierta temperatura. Dispone de un slider que permite ajustar la temperatura que queremos ver.

Además nos permite elegir entre una lista de estrellas para ajustar su temperatura superficial. Esta lista se lee del archivo "*stars.txt*" que se ha de encontar junto con el ejecutable. Este archivo consta simplemente de una serie de l
