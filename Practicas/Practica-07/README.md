<div align="center">

# 🐱 **Practica 07** 🐶



# **Redes Convolucionales**


</div>


<div align="center">

[![](https://data-flair.training/blogs/wp-content/uploads/sites/2/2020/05/Cats-Dogs-Classification-deep-learning.gif)](https://www.youtube.com/watch?v=FhFyAIZL4_g)

</div>

---

### **Practica hecha por:**

```Haskell
\src> Carlos Emilio Castañon Maldonado
```

---

## **Requerimientos**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/)

Para la presente implementacion se contemplaron las bibliotecas adicionales de pytorch, ipywidgets, numpy y matplotlib, en caso de no tenerlas instaladas, ejecutar:

[Pytorch](https://pytorch.org/)

```C
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

[ipywidgets](https://ipywidgets.readthedocs.io/en/stable/)

```C
> pip install ipywidgets
```

[Numpy](https://numpy.org/install/)

```C
> pip install numpy
```

[Matplotlib](https://matplotlib.org/)

```C
> pip install matplotlib
```


Es importante recordar tambien que debemos asegurarnos de que tenemos instalado [Jupyter](https://jupyter.org/install).

```C
> pip install jupyterlab
```

```C
> pip install notebook
```


---


## **Uso**

Para correr el programa que implementa una Red Neuronal Convolucional para la prediccion de imagenes correspondientes a;

<div align="center">

**'🛩️ avión 🛩️', '🚗 automóvil 🚗', '🕊️ pájaro 🕊️', '🐱 gato 🐱', '🦌 ciervo 🦌', '🐶 perro 🐶', '🐸 rana 🐸', '🐎 caballo 🐎', '🛥️ barco 🛥️', '🚛 camión 🚛'**

</div>

Usando el data-set [Cifar 10](https://www.cs.toronto.edu/~kriz/cifar.html),
se debe abrir el Jupyter Notebook en algun editor (como Jupyter nativo, VS Code, etc.).

[Práctica-07](./CIFAR10-Pytorch.ipynb)

<div align="center">

![ImgRedNTrain](https://github.com/CarlosCastanon2099/Redes-Neuronales/assets/108638686/7b85ff3b-f91b-45bb-9e36-b0cf530fe741)

```C
Precision en conjunto de entrenamiento: 99.0880%
Precision en conjunto de validacion: 70.2300%
```

![ImgRedNConv](https://github.com/CarlosCastanon2099/Redes-Neuronales/assets/108638686/381f002b-c291-4fa2-bfba-85ed38d14fcc)

![ImgRedNConv2](https://github.com/CarlosCastanon2099/Redes-Neuronales/assets/108638686/a62e830b-bcd9-4392-ba87-0d730b6024f4)


</div>

