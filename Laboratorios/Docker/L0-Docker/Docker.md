# Laboratorio 00 - Docker

Este laboratorio no entra en el examen practico, pero es necesario para entregar el proyecto.

## Objetivos

1. Entender a nivel basico las ventajas tecnicas del uso de Docker.
2. Obtener un conocimiento basico de los elementos mas importantes de Docker y su funcionamiento: imagenes, containers, repositorios, volumenes, etc.
3. Hacer un despliegue simple de varios servicios mediante docker-compose.

## Recursos necesarios

- Ubuntu (Usuario/password: lsi/lsi).
- Archivos Docker disponibles en eGela.
- Proyecto basico docker-compose disponible en GitHub.

## Indice

1. Introduccion.
2. Instalacion y configuracion.
3. Gestionar imagenes.
4. Ejecutar containers.
5. Construir imagenes.
6. Ejecutar servicios.

## 1. Introduccion

Docker es una infraestructura de "virtualizacion" para GNU/Linux basada en containers. Es una herramienta muy popular que se usa para hacer despliegues de servicios fieles al entorno original, evitando asi el famoso "En mi local funciona" (pero en el de tu cliente no).

El elemento principal de Docker es la imagen: un archivo comprimido inmutable que contiene todo lo que necesita el servicio para funcionar (sistema, binarios, librerias, archivos, etc.). A partir de una imagen se pueden crear containers, que son ejecuciones aisladas, efimeras y mutables del servicio.

Docker tambien ofrece la posibilidad de crear repositorios de imagenes: el repositorio oficial contiene imagenes oficiales que se pueden reusar para construir servicios especificos.

## 2. Instalacion y configuracion

Para instalar Docker:

```bash
apt install docker.io
```

Docker necesita privilegios de root. Para evitar el uso de sudo:

- Crear grupo docker:

```bash
sudo groupadd docker
```

- Anadir usuario actual al grupo docker:

```bash
sudo usermod -aG docker $USER
```

- Reiniciar el sistema, volver a entrar, y ejecutar:

```bash
docker run hello-world
```

## 3. Gestionar imagenes

Docker tiene un repositorio local que contiene las imagenes que vamos a usar en nuestro ordenador.

- Puedes ver las imagenes disponibles en tu repositorio local mediante:

```bash
docker images
```

El repositorio remoto mas comun se encuentra en Docker Hub, que es el repositorio configurado por defecto al instalar Docker.

- Explora las imagenes que se pueden encontrar en Docker Hub.

Vamos a descargar una imagen del repositorio remoto al repositorio local:

- Busca la imagen hello-world en Docker Hub.
- Descarga la imagen al repositorio local:

```bash
docker pull hello-world
```

Pregunta:

- Con que comando se suben imagenes a Docker Hub desde nuestro repositorio local?

## 4. Ejecutar containers

En Docker, los containers se ejecutan a partir de una imagen.

- Ejecuta un container a partir de la imagen hello-world:

```bash
docker run hello-world
```

Pregunta:

- Que output nos da la ejecucion del container?

- Ejecuta:

```bash
docker run -it ubuntu bash
```

Preguntas:

- De donde sale la imagen ubuntu?
- Que diferencia hay entre docker run y docker run -it?
- Por que ha cambiado el prompt de la terminal?
- Si hacemos un listado mediante ls, a que maquina pertenecen los directorios?
- Que output nos da el comando docker ps -a?

Para parar los containers, necesitamos su nombre o id:

```bash
docker kill nombre_o_id
docker ps -a
```

Aunque los containers no estan funcionando, hay que eliminarlos:

```bash
docker rm nombre_o_id
docker ps -a
docker images
```

Preguntas:

- Que diferencia hay entre parar y borrar un container?
- Como afecta a la imagen de la que ha surgido el container?
- Como se borra una imagen?

Vuelve a ejecutar un container desde la imagen ubuntu:

```bash
docker run -it ubuntu bash
```

En otra terminal:

```bash
docker exec nombre_container ls
```

Pregunta:

- Que diferencia hay entre run y exec?

## 5. Construir imagenes

Para construir una imagen Docker necesitamos un Dockerfile. Un Dockerfile es un archivo de texto plano que le dice a Docker como tiene que construir la imagen.

Por ejemplo:

- FROM: la imagen base a usar.
- ADD: anade archivos locales a la imagen.
- RUN: ejecuta comandos.
- CMD: el comando que se ejecutara al arrancar el container a partir de la imagen descrita en el Dockerfile.

Pregunta:

- Cuando ejecutemos un container a partir de esta imagen, que output vamos a obtener? Por que?

Vamos a construir una imagen a partir del Dockerfile que se encuentra en eGela:

- Baja el Dockerfile de eGela, junto al archivo msg que contiene un mensaje.
- Ejecuta en el mismo directorio (el nombre puede ser cualquiera):

```bash
docker build -t="nombre" .
```

- Comprueba que la imagen ha sido construida y anadida al repositorio local:

```bash
docker images
```

- Ejecuta un container de la imagen que acabamos de construir:

```bash
docker run nombre
```

Preguntas:

- Que output nos da al ejecutar el container?
- Como cambiarias el mensaje que se obtiene?

Docker nos permite montar directorios que son compartidos por el host y el container, es decir que ambos pueden leer y escribir en esos directorios.

Para probarlo:

- Crea un directorio llamado dir-msg que contenga un archivo msg2 con la cadena "iep":

```bash
mkdir dir-msg && echo "iep" > dir-msg/msg2
```

- Ejecuta un container a partir de la imagen ubuntu, de manera interactiva, montando el directorio dir-msg dentro del container en el directorio /app:

```bash
docker run -it -v "$(pwd)"/dir-msg:/app ubuntu bash
```

- Una vez dentro del container, asegurate de que se ha montado correctamente:

```bash
cat /app/msg2
```

- En otra terminal, cambia el contenido de dir-msg/msg2 y vuelve a ejecutar cat /app/msg2 dentro del container.

Preguntas:

- Ha cambiado el contenido del archivo?
- Por que?

Los containers son, por definicion, efimeros y de una existencia muy corta. Por lo tanto, los volumenes en Docker son muy importantes ya que nos permiten persistir datos que de otra manera se perderian al borrar el container.

A la hora de desarrollar aplicaciones que se van a desplegar mediante Docker es muy comun trabajar de la siguiente manera:

1. Montar directorio de desarrollo con la aplicacion y el directorio con los datos en el container.
2. Desarrollar y hacer pruebas.
3. Cuando obtengamos una version estable de la aplicacion, anadirla al Dockerfile.

## 6. Ejecutar servicios

Mediante docker-compose podemos definir un grupo de servicios que se ejecuten a la vez de manera coordinada, basandose cada servicio en una imagen Docker. Teniendo en cuenta que hoy en dia muchas aplicaciones se basan en combinaciones de servicios (base de datos, servidor web, otros servidores, etc.), esta es una caracteristica muy importante.

Vamos a ver como funciona docker-compose explorando el proyecto que podeis usar como base para la entrega 1.

El proyecto consta de tres servicios que conforman una aplicacion web muy sencilla:

- Un servidor web con una aplicacion PHP (la aplicacion web propiamente dicha) que accede a una base de datos MariaDB.
- La base de datos MariaDB.
- Un servidor web con la aplicacion PHPMyAdmin para gestionar la base de datos MariaDB.

- Clona el repositorio de GitHub que contiene el proyecto (o descargalo):

```bash
git clone https://github.com/mikel-egana-aranguren/docker-lamp.git
```

El archivo docker-lamp/docker-compose.yml contiene la definicion de los servicios. En este caso hay tres servicios (el nombre del servicio y de la imagen Docker en la que se basa pueden ser diferentes):

- web: este servicio se basa en la imagen web construida a partir del Dockerfile, que contiene un servidor web Apache y una aplicacion PHP definida en /app (esta imagen es una extension de la imagen oficial de PHP). Se enlaza al servicio db y redirige el puerto 81 del host al puerto 80 del container (donde se ejecuta Apache).
- db: la imagen mariadb es la imagen oficial que provee la base de datos MariaDB. En este caso el servicio se ejecuta obteniendo los datos del volumen ./mysql (es decir, si volvemos a ejecutar un container, los datos se cargaran de ese directorio y no se perderan, aunque el container haya desaparecido), con la configuracion de la seccion environment y redirigiendo el puerto 8889 del host al puerto 3306 del container.
- phpmyadmin: este servicio se basa en la imagen oficial de PHPMyAdmin, que se conecta al servicio db y se usa para administrar la base de datos, redirigiendo el puerto 8890 del host al puerto 80 del container.

Para desplegar el proyecto:

- Situa la terminal dentro del repositorio docker-lamp.
- Construye la imagen web:

```bash
docker build -t="web" .
```

- Despliega los servicios mediante:

```bash
docker-compose up
```

- Visita la web en http://localhost:81
- Para anadir los datos necesarios, visita http://localhost:8890/ (tal y como lo hemos definido en docker-compose.yml, usuario admin, password test).
- Haz click en database y luego en import, desde donde eliges el archivo docker-lamp/database.sql.
- Vuelve a http://localhost:81, deberia tener mas informacion.

Para parar los servicios, en otra terminal:

```bash
docker-compose down
```

## Esquema de servicios

El flujo de puertos y servicios del laboratorio se resume en el diagrama Sistema-web.png y su fuente Sistema-web.graphml:

- Host:81 -> Apache/App:80
- Host:8889 -> MariaDB:3306
- Host:8890 -> PHPMyAdmin:80
