import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import tkinter as tk
import tkinter.messagebox as MessageBox
import Figuras
import numpy as np

import sys


class GDistribuciones:
    """
    Clase auxiliar para contener los datos necesarios para graficar las
    distribuciones de probabilidad muestreadas con los grupos
    de partículas.
    """
    def __init__(self, maquina, nrens = 3, ncols = 4):
        self.nrens = nrens
        self.ncols = ncols
        self.fig, self.axes = plt.subplots(nrens, ncols)

        self.num_edos_posibles = pow(2, maquina.num_neuronas)
        self.num_edos_ocultos_posibles = pow(2, maquina.num_ocultas)

        # Ejes para graficar la distribución de partículas de fantasía
        self.ax_pf = plt.subplot2grid((nrens,ncols), (0, 0), colspan=ncols)
        self.ax_pf.set_xlim(0, self.num_edos_posibles)

        # Subgráficas para las distribuciones para cada dato de entrenamiento
        part_axes = []
        for i in range(1, 3):
            for j in range(0, 4):
                part_axes.append(plt.subplot2grid((nrens,ncols), (i, j)))
        self.part_axes = part_axes


class Maquina:
    """
    Clase que representa a la máquina de Boltzmann, con los métodos necesarios
    para realizar evaluaciones y entrenarla.
    """
    colores_neuronas = {'oculta_activa':('SpringGreen4','dark green'),
                        'oculta_inactiva':('slate gray','black'),
                        'visible_activa':('firebrick1', 'red4'),
                        'visible_inactiva':('slate gray','black')}
    colores_aristas = {'visible_visible':'firebrick',
                       'visible_oculta':'DeepSkyBlue2',
                       'oculta_oculta':'forest green'}

    def __init__(self, canvas, centro):
        nh = 8             # número de neuronas ocultas
        nv_x = 3
        nv_y = 3
        nv = nv_x * nv_y    # número de neuronas visibles
        n = nh + nv         # número total de neuronas
        nps = 100           # número de partículas

        self.num_ocultas = nh
        self.num_visibles = n - nh
        self.num_neuronas = n
        self.num_particulas = nps
        # Datos de entrenamiento
        X = np.array([
            [1,0,0,0,1,0,0,0,1],
            [0,0,1,0,1,0,1,0,0],
            [1,1,1,0,0,0,0,0,0],
            [0,0,0,1,1,1,0,0,0],
            [0,0,0,0,0,0,1,1,1],
            [1,0,0,1,0,0,1,0,0],
            [0,1,0,0,1,0,0,1,0],
            [0,0,1,0,0,1,0,0,1]
        ])
        self.datos_de_entrenamiento = X

        # Valores iniciales para los pesos
        # recordando que es una matriz simétrica con ceros en la diagonal
        W = np.random.random((n, n))
        W = (W.T + W)/2 - np.diag(W.diagonal())
        self.pesos = W
        print(W)

        # Partículas de fantasía
        PF = np.random.randint(2, size=(nps, n))

        # Partículas (para muestrear p(v))
        P = np.random.randint(2, size=(len(X), nps, n))
        for i, v in enumerate(X):
            particulas = P[i]
            particulas[:,0:nv] = v      # El valor de las neuronas visibles está fijo
        self.particulas = P
        self.particulas_fantasia = PF

        #
        # Parámetros para graficar las distribuciones de las partículas
        #
        self.datos_distribuciones = GDistribuciones(self)

        # Elementos para dibujar la máquina de Boltzmann
        p = Figuras.Poligono(nh)        # Neuronas ocultas
        pcentro = centro.copy()

        g = Figuras.Grid(nv_x, nv_y)    # Neuronas visibles
        centro[1] += p.radio() + 50 + g.altura()
        gcentro = centro.copy()

        # Aristas en el orden en que deben ser dibujadas
        # (triángulo inferior de la matriz de pesos)
        coordenadas = np.vstack((gcentro + g.coordenadas(), pcentro + p.coordenadas()))
        aristas = [[]]
        for i in range(1, n):
            renglon = []
            for j in range(0, i):
                ini = coordenadas[i]
                fin = coordenadas[j]
                renglon.append(canvas.create_line(ini[0], ini[1], fin[0], fin[1]))
            aristas.append(renglon)
        p.dibuja_vertices(canvas, pcentro, fill="SteelBlue1")
        g.dibuja_vertices(canvas, centro, fill="orchid1")

        # Círculos con los valores de activación de cada neurona
        self.vertices = g.circulos() + p.circulos()
        self.aristas = aristas


    def dibuja_particula(self, particula, canvas):
        """
        Cambia los colores del dibujo de la máquina de Boltzmann
        dependiendo de los valores de activación de la partícula indicada
        :param particula: partícula cuyos estados serán dibujados
        :param canvas: canvas de tkinter donde se encuentra el dibujo
        """
        for i, circ in enumerate(self.vertices):
            if i < self.num_visibles:
                if(particula[i] < 0.5):
                    canvas.itemconfig(circ, fill=Maquina.colores_neuronas['visible_inactiva'][0],
                                      outline=Maquina.colores_neuronas['visible_inactiva'][1],
                                      width=1.5)
                else:
                    canvas.itemconfig(circ, fill=Maquina.colores_neuronas['visible_activa'][0],
                                      outline=Maquina.colores_neuronas['visible_activa'][1],
                                      width=1.5)
            else:
                if(particula[i] < 0.5):
                    canvas.itemconfig(circ, fill=Maquina.colores_neuronas['oculta_inactiva'][0],
                                      outline=Maquina.colores_neuronas['oculta_inactiva'][1],
                                      width=1.5)
                else:
                    canvas.itemconfig(circ, fill=Maquina.colores_neuronas['oculta_activa'][0],
                                      outline=Maquina.colores_neuronas['oculta_activa'][1],
                                      width=1.5)
        W = self.pesos
        max = np.amax(W)
        MAX_W = 5.0
        aristas = self.aristas
        for i in range(1, self.num_visibles):
            for j in range(0, i):
                canvas.itemconfig(aristas[i][j], fill=Maquina.colores_aristas['visible_visible'], width=MAX_W * W[i,j]/max)
        for i in range(self.num_visibles, self.num_neuronas):
            for j in range(0, self.num_visibles):
                canvas.itemconfig(aristas[i][j], fill=Maquina.colores_aristas['visible_oculta'], width=MAX_W * W[i,j]/max)
        for i in range(self.num_visibles, self.num_neuronas):
            for j in range(self.num_visibles, i):
                canvas.itemconfig(aristas[i][j], fill=Maquina.colores_aristas['oculta_oculta'], width=MAX_W * W[i,j]/max)

    def grafica_distribuciones_fantasia(self):
        """
        Grafica el histograma de las partículas de fantasía en cada estado posible.
        """
        datos = self.datos_distribuciones
        num_edos_posibles = datos.num_edos_posibles
        #num_edos_posibles = 50

        # Distribución de las partículas de fantasía
        ax_pf = datos.ax_pf
        ax_pf.clear()
        ax_pf.set_xlim(0, num_edos_posibles)
        P = self.particulas_fantasia
        edos_int = P.dot(1 << np.arange(P.shape[1] - 1, -1, -1))
        ax_pf.hist(edos_int, num_edos_posibles)
        return datos.fig

    def grafica_distribuciones_particulas(self):
        """
        Grafica los histogramas de las partículas utilizadas para muestrear las
        distribuciones de probabilidad condicional para cada ejemplar de entrenamiento.
        P(ocultas|visibles)
        """
        datos = self.datos_distribuciones
        num_edos_ocultos_posibles = datos.num_edos_ocultos_posibles

        # Distribución de las partículas para cada valor de entrenamiento
        part_axes = datos.part_axes
        x = np.arange(num_edos_ocultos_posibles)
        y = np.zeros(x.shape)
        for i, P in enumerate(self.particulas):
            part_axes[i].clear()
            part_axes[i].set_xlim(0, num_edos_ocultos_posibles)
            a = P[:,self.num_visibles:]
            edos_int = a.dot(1 << np.arange(a.shape[1] - 1, -1, -1))
            for estado in edos_int:
                y[estado] += 1
            part_axes[i].bar(x, y)
        return datos.fig
    
    def probabilidad_neurona_oculta(self, h, W, v):
        """
        Calcula la probabilidad de activacion de una neurona oculta.
        """
        z = np.dot(W[h], v)
        return 1.0 / (1.0 + np.exp(-z))

    def probabilidad_neurona_visible(self, v, W, h):
        """
        Calcula la probabilidad de activacion de una neurona visible.
        """
        z = np.dot(W[v], h)
        return 1.0 / (1.0 + np.exp(-z))

    def simula_fantasia(self, ciclos, canvas=None, num_particula=0):
        """
        Para cada paso, elige las neuronas en cada partícula en orden aleatorio y actualiza su valor
        :param ciclos: número de veces que actualizará todos los valores de las neuronas de cada partícula.
        :return:
        """
        for ciclo in range(ciclos):
            for particula in self.particulas_fantasia:
                for i in range(self.num_neuronas):
                    if i < self.num_visibles:  # neuronas visibles
                        h = particula[self.num_visibles:]
                        prob = self.probabilidad_neurona_visible(i, self.pesos[:self.num_visibles, self.num_visibles:], h)
                        particula[i] = np.random.rand() < prob
                    else:  # neuronas ocultas
                        v = particula[:self.num_visibles]
                        prob = self.probabilidad_neurona_oculta(i - self.num_visibles, self.pesos[self.num_visibles:, :self.num_visibles], v)
                        particula[i] = np.random.rand() < prob

        if(canvas != None):
            print("Siguiendo: ", num_particula)
            self.dibuja_particula(self.particulas_fantasia[num_particula], canvas)

    def simula_particulas(self, ciclos, canvas=None, num_dato=0, num_particula=0):
        """
        Para cada paso, elige las neuronas ocultas en cada partícula en orden aleatorio y actualiza su valor
        :param ciclos: número de veces que actualizará todos los valores de las neuronas de cada partícula.
        :return:
        """
        for ciclo in range(ciclos):
            particulas = self.particulas[num_dato]
            for particula in particulas:
                for i in range(self.num_visibles, self.num_neuronas):  # solo neuronas ocultas
                    v = particula[:self.num_visibles]
                    prob = self.probabilidad_neurona_oculta(i - self.num_visibles, self.pesos[self.num_visibles:, :self.num_visibles], v)
                    particula[i] = np.random.rand() < prob

        if (canvas != None):
            print("Siguiendo: ", num_dato, ", ", num_particula)
            self.dibuja_particula(self.particulas[num_dato][num_particula], canvas)

    def actualiza_pesos(self):
        """
        Asigna nuevos valores a los pesos utilizando los valores esperados
        de los productos de los valores de activación de las neuronas que conectan.
        """
        # Paso positivo - calculo de la expectativa empirica
        positive_phase = np.zeros_like(self.pesos)
        for x in self.datos_de_entrenamiento:
            v0 = x
            h0_prob = self.probabilidad_neurona_oculta(np.arange(self.num_ocultas), self.pesos[self.num_visibles:, :self.num_visibles], v0)
            h0 = (np.random.rand(self.num_ocultas) < h0_prob).astype(np.float32)
            positive_phase[:self.num_visibles, self.num_visibles:] += np.outer(v0, h0)
            positive_phase[self.num_visibles:, :self.num_visibles] += np.outer(h0, v0)

        # Paso negativo - calculo de la expectativa del modelo (usando particulas de fantasia)
        negative_phase = np.zeros_like(self.pesos)
        for particula in self.particulas_fantasia:
            v = particula[:self.num_visibles]
            h = particula[self.num_visibles:]
            negative_phase[:self.num_visibles, self.num_visibles:] += np.outer(v, h)
            negative_phase[self.num_visibles:, :self.num_visibles] += np.outer(h, v)

        # Actualizacion de los pesos
        self.pesos += (positive_phase - negative_phase) / self.num_particulas

        # Normalizacion de los pesos
        #max = np.amax(self.pesos)
        #self.pesos = self.pesos / max
        #print(self.pesos)

        print("Pesos actualizados")




class Toolbar(tk.Frame):
    """
    Barra de herramientas con los controles para mandar ejecutar cada paso del algoritmo de entrenamiento
    y ejecución de la máquina utilizando ensembles de partículas.
    """
    def __init__(self, parent, maquina, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Partículas de fantasía
        tk.Label(self, text="Partícula a seguir: [0," + str(maquina.num_particulas - 1) + "]").grid(row=0, column=0)
        tk.Spinbox(self, from_=0, to=maquina.num_particulas, textvariable=parent.particula_fantasia_a_seguir).grid(row=0, column=1)
        tk.Label(self, text="Ciclos:").grid(row=1, column=0)
        tk.Spinbox(self, from_=0, to=maquina.num_particulas, textvariable=parent.ciclos_fantasia).grid(row=1, column=1)
        tk.Button(master=self, text='Simular fantasía', command=parent.simula_fantasia).grid(row=1, column=2, sticky='WE')

        # Partículas para datos de entrenamiento
        max = len(maquina.datos_de_entrenamiento) - 1
        tk.Label(self, text="Dato a seguir: [0," + str(max) + "]").grid(row=3, column=0)
        tk.Spinbox(self, width=10, from_=0, to=max, textvariable=parent.dato_a_seguir).grid(row=3, column=1)
        tk.Label(self, text="Partícula a seguir: [0," + str(maquina.num_particulas - 1) + "]").grid(row=4, column=0)
        tk.Spinbox(self, from_=0, to=maquina.num_particulas, textvariable=parent.particula_a_seguir).grid(row=4, column=1)
        tk.Label(self, text="Ciclos:").grid(row=5, column=0)
        tk.Spinbox(self, from_=0, to=maquina.num_particulas, textvariable=parent.ciclos).grid(row=5, column=1)
        tk.Button(master=self, text='Simular partículas', command=parent.simula_particulas).grid(row=5, column=2, sticky='WE')

        # Actualización de los pesos de la red
        tk.Label(self, text="Muestras:").grid(row=6, column=0)
        muestras = tk.Spinbox(self, from_=0, to=100000)
        muestras.grid(row=6, column=1)
        button_actualiza_pesos = tk.Button(master=self, text='Actualiza pesos', command=maquina.actualiza_pesos)
        button_actualiza_pesos.grid(row=6, column=2, sticky='WE')

        # Visualización de las gráficas
        button_grafica = tk.Button(master=self, text='Graficar conjuntas', command=parent.grafica_distribuciones_fantasia)
        button_grafica.grid(row=7, column=1, sticky='WE')
        button_grafica_cond = tk.Button(master=self, text='Graficar condicionales', command=parent.grafica_distribuciones_particulas)
        button_grafica_cond.grid(row=7, column=2, sticky='WE')



class BoltzmannGui(tk.Frame):
    """
    Interfaz gráfica para mostrar el proceso de entrenamiento de una máquina de Boltzmann
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Dibujo del estado de la máquina para una partícula
        w = tk.Canvas(parent, width=500, height=850)
        w.pack(side=tk.RIGHT)
        m = Maquina(w, np.array([250, 250])) # El arreglo indica el centro del dibujo
        self.maquina = m
        self.maq_canvas = w

        # Controles para indicar los parámetros para la simulación
        self.particula_fantasia_a_seguir = var = tk.IntVar(self)
        var.set(0)
        self.ciclos_fantasia = var = tk.IntVar(self)
        var.set(100)

        self.dato_a_seguir = var = tk.IntVar(self)
        var.set(0)
        self.particula_a_seguir = var = tk.IntVar(self)
        var.set(0)
        self.ciclos = var = tk.IntVar(self)
        var.set(50)
        self.toolbar = Toolbar(self, m)
        self.toolbar.pack(side="top", fill="x")

        # Canvas para las gráficas de las distribuciones de probabilidad
        mpl_canvas = FigureCanvasTkAgg(m.datos_distribuciones.fig, master=self)
        mpl_canvas.draw()
        mpl_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.mpl_canvas = mpl_canvas

        m.dibuja_particula(m.particulas_fantasia[0], w)

    def simula_fantasia(self):
        self.maquina.simula_fantasia(self.ciclos_fantasia.get(), self.maq_canvas, self.particula_fantasia_a_seguir.get())

    def simula_particulas(self):
        self.maquina.simula_particulas(self.ciclos.get(), self.maq_canvas, self.dato_a_seguir.get(), self.particula_a_seguir.get())

    def grafica_distribuciones_fantasia(self):
        """
        Responde a la acción del botón "Grafica distribuciones"
        """
        fig = self.maquina.grafica_distribuciones_fantasia()
        fig.canvas.draw()
        self.mpl_canvas.draw()

    def grafica_distribuciones_particulas(self):
        """
        Responde a la acción del botón "Grafica distribuciones"
        """
        fig = self.maquina.grafica_distribuciones_particulas()
        fig.canvas.draw()
        self.mpl_canvas.draw()


if '__main__' == __name__:
    #http://effbot.org/tkinterbook/canvas.htm
    master = tk.Tk()
    master.wm_title("Máquina de Boltzmann")
    BoltzmannGui(master).pack(side="top", fill="both", expand=True)
    master.protocol("WM_DELETE_WINDOW", sys.exit)
    master.mainloop()
