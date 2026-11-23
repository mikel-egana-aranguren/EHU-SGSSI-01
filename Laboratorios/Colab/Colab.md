# Laboratorio: Google Colab

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar usuario `lsi` si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.
- Cuenta Google utilizada para servidor Google Cloud.

## Google Colab

### Introducción

[Google Colab](https://colab.research.google.com) es un entorno de desarrollo basado en [Jupyter Notebooks](https://jupyter.org) que permite ejecutar código Python en la nube sin instalar software adicional.

En este laboratorio aprenderemos a:

- Crear y ejecutar notebooks en Google Colab.
- Utilizar celdas de código y texto Markdown.
- Cargar y analizar datos.
- Entrenar un modelo sencillo de Machine Learning.
- Evaluar su rendimiento.
- Identificar algunos riesgos de seguridad relacionados con modelos de Machine Learning.

Trabajaremos con herramientas y conjuntos de datos públicos. No subas información personal, datos sensibles ni credenciales a Google Colab.

### Crear un notebook en Colab

Accede a [Colab](https://colab.research.google.com) con la misma cuenta de Google con la que creaste el servidor de Google Cloud. Crea un nuevo notebook (File; New Notebook) y renómbralo a `ml-sec.ipynb`.

Ejecuta la siguiente celda:

```python
print("Hi Colab World")
```

Añade una celda de texto.

> ¿Qué diferencia existe entre una celda de código y una celda de texto?

> ¿Qué ocurre si ejecutas varias veces la misma celda?

### Conocer el entorno de ejecución

Ejecuta:

```python
import platform

print(platform.platform())
print(platform.python_version())
```

Comprueba la memoria disponible:

```python
!free -h
```

Comprueba el contenido del directorio actual:

```python
!ls
```

> ¿Dónde se ejecuta realmente el código?

> ¿Qué diferencia existe entre tu ordenador local y el entorno de ejecución de Colab?

### Trabajar con datos

Importa las librerías necesarias:

```python
import pandas as pd
```

Carga un conjunto de datos público:

```python
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

df = pd.read_csv(url)

df.head()
```

Obtén información general:

```python
df.info()
```

Obtén estadísticas descriptivas:

```python
df.describe()
```

> ¿Cuántas filas y columnas contiene el conjunto de datos?

> ¿Qué representa cada columna?

### Visualizar los datos

Instala y utiliza bibliotecas de visualización:

```python
import seaborn as sns
import matplotlib.pyplot as plt
```

Visualiza las relaciones entre variables:

```python
sns.pairplot(df, hue="species")
plt.show()
```

> ¿Se distinguen visualmente las diferentes especies?

> ¿Qué variables parecen más útiles para clasificarlas?

### Entrenar un modelo de Machine Learning

Importa las herramientas necesarias:

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
```

Separa datos y etiquetas:

```python
X = df.drop("species", axis=1)
y = df["species"]
```

Divide entrenamiento y prueba:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)
```

Crea y entrena el modelo:

```python
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
```

Realiza predicciones:

```python
predictions = model.predict(X_test)
```

Calcula la precisión:

```python
accuracy_score(y_test, predictions)
```

> ¿Qué significa la precisión obtenida?

> ¿Es suficiente una precisión elevada para confiar plenamente en el modelo?

### Interpretar el modelo

Visualiza el árbol de decisión:

```python
from sklearn.tree import plot_tree

plt.figure(figsize=(12,8))

plot_tree(
    model,
    feature_names=X.columns,
    class_names=model.classes_,
    filled=True
)

plt.show()
```

> ¿Qué variables aparecen cerca de la raíz del árbol?

> ¿Por qué puede ser útil entender cómo toma decisiones un modelo?

### Guardar el notebook en GitHub

Selecciona: File; Save a copy in GitHub

O descarga el notebook: File; Download; Download .ipynb

Sube el notebook a tu repositorio de GitHub.

> ¿Qué ventajas tiene almacenar el notebook bajo control de versiones?

### Seguridad en Machine Learning

Los modelos de Machine Learning también presentan riesgos de seguridad. En esta sección analizaremos algunos ejemplos.

#### Envenenamiento de datos (Data Poisoning)

Un atacante modifica parte de los datos de entrenamiento para alterar el comportamiento del modelo.

Ejecuta:

```python
df_poisoned = df.copy()

df_poisoned.loc[0:10, "species"] = "setosa"
```

Observa las primeras filas:

```python
df_poisoned.head(15)
```

> ¿Qué efecto puede tener modificar etiquetas de entrenamiento?

> ¿Por qué es importante verificar el origen y calidad de los datos?

#### Modelos con sesgos

Calcula cuántas muestras existen de cada clase:

```python
df["species"].value_counts()
```

> ¿Qué problemas podrían aparecer si una clase estuviera muy poco representada?

> ¿Cómo afectaría esto a la calidad de las predicciones?


