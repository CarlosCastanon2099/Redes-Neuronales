import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import warnings

from IPython.core.pylabtools import figsize
import matplotlib.gridspec as gridspec

def muestraImagen(vector3D, labelsVector, indice):
    COLOR = cm.magma
    figsize(3, 3)
    plt.title(labelsVector[indice])
    # El -1 invierte el orden en y
    plt.pcolormesh(vector3D[indice][::-1], cmap=COLOR)


def muestraActividad(red, iEntrada):
    """Grafica los valores de activación de cada neurona
    para la entrada en la posición iEntrada.
    """
    COLOR = cm.magma

    # Verificación del índice de entrada
    if iEntrada >= red.A0.shape[0]:
        raise IndexError(f"Ejemplar de entrenamiento inexistente {iEntrada}")

    fig = plt.figure(figsize=(5, 7))
    gs = gridspec.GridSpec(4, 1, height_ratios=[1, 1, 4, 4])  # Ajusta las proporciones aquí

    ax_2 = plt.subplot(gs[0, 0])  # Activación de la capa de salida: predicción
    ax_1 = plt.subplot(gs[1, 0])  # Activación de la capa oculta
    ax_0 = plt.subplot(gs[2:4, 0])  # Imagen de entrada

    norm = matplotlib.colors.Normalize(vmin=0, vmax=1)

    # Ajustes para a0, a1, y a2
    a0 = red.A0[iEntrada, 1:].reshape((28, 28))[::-1]
    a1 = red.A1[iEntrada, :].reshape(1, -1)
    a2 = red.A2[iEntrada, :].reshape(1, -1)

    # Imagen de entrada
    ax_0.pcolormesh(a0, cmap=COLOR, norm=norm)
    ax_0.set_xlim(0, 28)
    ax_0.set_ylim(0, 28)
    ax_0.set_title("Imagen de entrada")

    # Activación de la capa oculta
    ax_1.pcolormesh(a1, cmap=COLOR, norm=norm)
    ax_1.set_yticks(np.array([0, 1]))
    ax_1.set_xlim(0, a1.shape[1])
    ax_1.set_xticks(np.arange(a1.shape[1]) + 0.5)
    ax_1.set_xticklabels(np.arange(a1.shape[1]), minor=False, ha="center")
    ax_1.set_title("Activación de la capa oculta")

    # Activación de la capa de salida: predicción
    ax_2.pcolormesh(a2, cmap=COLOR, norm=norm)
    ax_2.set_xticks(np.arange(a2.shape[1]) + 0.5)
    ax_2.set_xticklabels(np.arange(a2.shape[1]), minor=False, ha="center")
    ax_2.set_title("Activación de la capa de salida: predicción")

    # Barra de color
    ax1 = fig.add_axes([1.0, 0, 0.025, 1.0])  # left, bottom, width, height
    cb1 = matplotlib.colorbar.ColorbarBase(ax1, cmap=COLOR, norm=norm, orientation="vertical")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.tight_layout()