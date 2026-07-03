# Laboratorio: Git

## Requisitos previos

- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP).
- Herramientas necesarias: `git`.

## Git

Git es un sistema distribuido de control de versiones desarrollado por el creador de Linux, Linus Torvalds, muy extendido, y que usaremos en diferentes partes de la asignatura. Sus elementos básicos son:

- Repositorio: el almacen de contenido (Normalmente archivos de código). Es una carpeta con un carpeta oculta llamada `.git`. 
- Fork: una copia independiente de un repositorio completo.
- Remoto (Remote): el repositorio puede ser local (En nuestro ordenador físico) o remoto (Por ejemplo en GitHub). Ambas instancias se pueden sincronizar mediante `pull`/`push`. 
- Commit: un repositorio es una "Grabación" de la historia de una carpeta (elementos añadidos, borrados, o modificados). Un commit es un momento dado en esa historia. 
- Rama: una historia específica. Un repositorio puede tener varias ramas, cada una de ellas representando una historia diferente (Un "Universo paralelo"). Las ramas se sincronizan fusionando unas sobre otras mediante `merge`. 

## Acceso a GitHub

Para trabajar con Git en esta asignatura, tenéis que crear una cuenta gratuita en [GitHub](https://github.com/) con el email de la universidad. 

Hay dos maneras de acceder a los repositorios en Github: mediante HTTP(S) o SSH. SSH es mucho más segura, ya que no hay que usar usuario/contraseña, y además es la que GitHub usa por defecto para poder hacer `push`. Para configurar el acceso de SSH, seguir las [instrucciones](https://docs.github.com/en/authentication/connecting-to-github-with-ssh). Esa misma clave SSH os va a servir en otros laboratorios, por ejemplo para acceder al servidor remoto de Google Cloud, así que guardadla bien.  

## Repositorio

Crear un repositorio **público** en GitHub siguiendo el patrón "sgssi-26-27-nombre-estudiante" (El nombre debe estar normalizado, por ejemplo "Mikel Egaña Aranguren" pasaría a "mikel-egana-aranguren", es decir "sgssi-26-27-mikel-egana-aranguren"). Este repositorio se usará para algunos ejercicios de laboratorio y el examen. 

Clonar el repositorio recién creado mediante `git clone git@github.com:...` (Usando SSH). Cambiar la terminal al directorio del repositorio recién clonado. 

Realizar cambios. Añadirlos al Staging area:

```bash
$ git add ...
```

Crear un commit (Añadir los cambios  al repositorio local):

```bash
$ git commit ...
```

Subir los cambios al remoto:

```bash
$ git push
```

Cambiar a una rama ya existente:

```bash
$ git checkout rama
```

Cambiar a rama nueva (Crear rama):

```bash
$ git checkout -b rama_nueva
```

Fusionar ramas (En rama target, es decir la rama que va a recibir los cambios):

```bash
$ git merge rama
``` 

## Obtener y modificar los apuntes de clase

Clonar el repo por primera vez mediante SSH:

```bash
$ git clone git@github.com:mikel-egana-aranguren/EHU-SGSSI-01.git
```
(El contenido esta dentro de cada carpeta, en PDF o HTML).

Para actualizar el contenido (Cambia con frecuencia):

```bash
$ cd EHU-SGSSI-01
$ git pull
```

Dado que los apuntes pueden tener errores, los alumnos pueden corregirlos y si la corrección es adecuada obtener 0,5 puntos sobre la nota de ese parcial. 

Para corregir un error:
- En la Web de GitHub, obtener un fork a partir del [repositorio de apuntes](https://github.com/mikel-egana-aranguren/EHU-SGSSI-01).
- Clonar el fork (No el original).
- Hacer la corrección en la rama **develop** y subirlo al fork. 
- Crear un [pull request](https://github.com/mikel-egana-aranguren/EHU-SGSSI-01/pulls?q=is%3Apr+is%3Aclosed).

## Más información

"La he liado parda" describe una situación bastante común:
- [La he liado parda](https://www.youtube.com/watch?v=QNTZbJSQVis).
- [La he liado parda - versión Git](https://vimeo.com/82408340).

Software carpentry - [Version Control with Git](https://swcarpentry.github.io/git-novice/).

[Git](https://git-scm.com/).

[GitFlow](https://nvie.com/posts/a-successful-git-branching-model/).


