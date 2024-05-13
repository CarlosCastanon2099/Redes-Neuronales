#!/usr/bin/python3.6
"""
Dibuja gráficas completamente conexas con la forma indicada en un tk.Canvas.
"""

import math
import numpy as np
import tkinter as tk

# Para instalar tk:
# sudo apt install python3-tk


def _create_circle(self, x, y, r, **kwargs):
    """
    Dibuja un círculo dado su centro y radio.
    :param self: canvas
    :param x: x
    :param y: y
    :param r: radio
    :param kwargs:
    :return:
    """
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle


class Poligono:
    """ Clase para definir las esquinas del polígono con el número indicado de lados. """
    def __init__(self, lados, radio_vertice=5):
        coordenadas = []
        angulo = 2 * math.pi / lados
        radio = 0.5 * math.pi * lados * radio_vertice
        par = (lados % 2 == 0)
        radianes = - math.pi / 2
        if par:
            radianes -= angulo / 2
        coordenadas.append(radianes)
        for i in range(1, lados):
            coordenadas.append(radianes + angulo * i)
        coordenadas = [(radio * math.cos(ang), radio * math.sin(ang)) for ang in coordenadas]
        self._radio_vertice = radio_vertice
        self._radio = radio
        self._coordenadas = np.array(coordenadas)

    def radio_vertice(self):
        """ Devuelve el radio con que dibujará el círculo de cada vértice. """
        return self._radio_vertice

    def radio(self):
        """ Devuelve el radio del círculo que engloba al polígono. """
        return self._radio

    def coordenadas(self):
        """ Devueve las coordenadas de este polígono. """
        return self._coordenadas

    def dibuja_vertices(self, canvas, centro, **kwargs):
        """
        Dibuja los vértices alrededor del centro indicado.
        :param centro:
        :return:
        """
        circulos = []
        for c in self.coordenadas():
            circulos.append(canvas.create_circle(centro[0] + c[0],
                                            centro[1] + c[1], self.radio_vertice(), **kwargs))
        self._circulos = circulos

    def circulos(self):
        """
        :return: Devuelve los círculos que representan a los vértices.
        """
        return  self._circulos


class Grid:
    """
    Clase para determinar las coordenadas de los vértices en un grid.
    """
    def __init__(self, nx, ny, radio_vertice=5):
        """
        Constructor
        :param nx: número de vértices en x
        :param ny: número de vértices en y
        :param radio_vertice: radio del círculo que será dibujado en cada vértice
        """
        coordenadas = []
        separacion = radio_vertice * 5
        for x in range(-nx + 1, nx + 1, 2):
            for y in range(-ny + 1, ny + 1, 2):
                coordenadas.append((x * separacion, y * separacion))
        self._coordenadas = np.array(coordenadas)
        self._radio_vertice = radio_vertice
        self._altura = (separacion + radio_vertice * 2) * (ny - 1)

    def radio_vertice(self):
        """ Devuelve el radio con que dibujará el círculo de cada vértice. """
        return self._radio_vertice

    def altura(self):
        """
        :return: el altura del grid en pixeles
        """
        return self._altura

    def coordenadas(self):
        """ Devueve las coordenadas de este polígono. """
        return self._coordenadas

    def dibuja_vertices(self, canvas, centro, **kwargs):
        """
        Dibuja los vértices alrededor del centro indicado.
        :param centro:
        :return:
        """
        circulos = []
        for c in self.coordenadas():
            circulos.append(canvas.create_circle(centro[0] + c[0],
                                            centro[1] + c[1], self.radio_vertice(), **kwargs))
        self._circulos = circulos

    def circulos(self):
        """
        :return: Devuelve los círculos que representan a los vértices.
        """
        return  self._circulos


def dibuja_conexiones(canvas, coordenadas, **kwargs):
    num = len(coordenadas)
    conexiones = []
    for i in range(num):
        for j in range(i):
            conexiones.append(canvas.create_line(coordenadas[i][0], coordenadas[i][1],
                                                 coordenadas[j][0], coordenadas[j][1],
                                                 **kwargs))


if '__main__' == __name__:
    import sys
    num_lados = 7
    if (len(sys.argv) > 1):
        try:
            num_lados = int(sys.argv[1])
        except ValueError:
            print("Uso: Poligono <num_lados>")
            exit(1)
    print(dir())
    p = Poligono(num_lados)
    print("Poligono:\n", p.coordenadas())

    g = Grid(3,3)
    print("Grid:\n", g.coordenadas())

    master = tk.Tk()
    w = tk.Canvas(master, width=200 + 2 * p.radio(), height=350 + 2 * p.radio() + g.altura())
    w.pack()

    centro = np.array([100 + p.radio(), 100 + p.radio()])
    dibuja_conexiones(w, centro + p.coordenadas(), fill="DarkOrchid1")
    p.dibuja_vertices(w, centro, fill="purple1", outline="LightSteelBlue1")

    centro[1] += p.radio() + 50 + g.altura()
    dibuja_conexiones(w, centro + g.coordenadas(), fill="SteelBlue4", width="2.0")
    g.dibuja_vertices(w, centro, fill="SteelBlue1", outline="thistle1")
    tk.mainloop()
