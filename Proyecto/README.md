<div align="center">

# 🎸🤖 **Proyecto Final : Predictor musical ​** 🐦‍🔥🎶

----
## **Integrantes del equipo:**

### <br> <img src="https://media.tenor.com/m6cM9lV-doYAAAAi/batman-batman-beyond.gif" width="30"> **Carlos Emilio Castañon Maldonado** & **Dana Dana Berenice Hernández Norberto** <img src="https://i.pinimg.com/originals/c2/00/92/c2009226c462e1fe82a19ca7cd206d1c.gif" width="30"> <br> 

[![](https://i.pinimg.com/originals/3e/fe/1c/3efe1cb845954233246f60d5d8395dd0.gif)](https://www.youtube.com/watch?v=O2IuJPh6h_A)

</div>

## **Proyecto originalmente hecho en este Repositorio:**
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/CarlosCastanon2099/Predictor-Musical)


## **Objetivo del proyecto:**
El objetivo de este proyecto es implementar una red neuronal que nos permita ingresar un archivo de audio y predecir cual es su genero. Para ello utilizamos la base de datos GTZAN Dataset compuesta por los siguientes archivos:
* CSV: Contiene dos csv con observaciones de canciones, clasificadas por genero musical.
* genres_original: En esta base tenemos diferentes archivos de audio de 10 generos diferentes con 100 canciones con una duración de 30 segundos cada una.
* images_original: Contiene espectogramas en un formato de imagen, de cada canción de las bases mencionadas anteriormente.

Los generos con los que vamos a trabajar son los siguientes en su formato de audio:

blues - classical - country - disco - hiphop - jazz - metal - pop - reggae - rock

-------------

## **Requerimientos**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/)

Para la presente implementacion se contemplaron las bibliotecas adicionales de pytorch, scikit-learn, librosa, numpy, pandas, matplotlib y seaborn en caso de no tenerlas instaladas, ejecutar:

[Pytorch](https://pytorch.org/)

```C
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

[Scikit-learn](https://scikit-learn.org/stable/install.html)

```C
> pip install -U scikit-learn
```

[librosa](https://librosa.org/)

```C
> pip install librosa
```

[Numpy](https://numpy.org/install/)

```C
> pip install numpy
```

[Pandas](https://pandas.pydata.org/getting_started.html)

```C
> pip install pandas
```

[Matplotlib](https://matplotlib.org/)

```C
> pip install matplotlib
```

[Seaborn](https://seaborn.pydata.org/installing.html)

```C
> pip install seaborn
```

Es importante recordar tambien que debemos asegurarnos de que tenemos instalado [Jupyter](https://jupyter.org/install).

```C
> pip install jupyterlab
```

```C
> pip install notebook
```

### **Nota**
En caso de querer hacer lo mostrado en el video del ejemplo de uso, necesitaremos tambien las bibliotecas de pytube y de moviepy.

[Pytube](https://pytube.io/en/latest/user/install.html)

```C
> pip install pytube
```

[Moviepy](https://zulko.github.io/moviepy/install.html)

```C
> pip install moviepy
```


------

## **Uso**

Para correr el notebook que implementa la arquitectura, entrenamiento y uso de la Red Neuronal LSTM, , se debe abrir el Jupyter Notebook en algun editor (como Jupyter nativo, VS Code, etc.).

[proyecto.ipynb](./proyecto.ipynb)

Una vez dentro del Notebook podremos correr distintas simulaciones a las presentadas cambiando cosas como los hiperparametros de entrenamiento de la red para ver su desempeño en otras condiciones:

```python
hidden_size = 128
num_layers = 3
num_classes = 10
dropout_prob = 0.8
learning_rate = 0.0009
num_epochs = 100
batch_size = 256
```

O en su defecto, el uso de nuestro modelo entrenado para poder predecir el genero musical de alguna cancion de nuestra eleccion.

Un ejemplo de uso para solo probar la red entrenada seria el siguiente:

https://github.com/CarlosCastanon2099/Predictor-Musical/assets/108638686/6179b978-7fcf-4e46-8942-c14832efe6c7





