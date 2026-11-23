# Laboratorio: Backups

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar usuario `lsi` si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.

Copias de seguridad en GNU/Linux
    • Cread en el escritorio una carpeta llamada Seguridad y en su interior 5 ficheros de texto llamados a, b, c, d y e. Cada fichero puede tener el contenido que queráis (ej. $ echo "A" > A).
Vamos a usar la herramienta rsync, que viene incluída por defecto en la mayoría de distribuciones de Linux, para realizar las copias de seguridad. Para ello, comenzaremos realizando una copia de seguridad completa de nuestra carpeta Seguridad, y a partir de ahí realizaremos copias de seguridad incrementales. 
    • Cread una carpeta llamada Backups en el directorio /var/tmp.
    • Ejecutad el siguiente comando (Sustituid “usuario” por el usuario que corresponda): 
	$ rsync -av /home/usuario/Seguridad /var/tmp/Backups 
¿Qué hace exactamente ese comando? ¿Qué implican las opciones “a” y “v” que hemos usado? ($ info rsync)
    • Ejecutad otra vez el comando, pero esta vez con un slash “/” al final del primer argumento:
	$ rsync -av /home/usuario/Seguridad/ /var/tmp/Backups
¿Qué diferencia hay con el comando sin slash?
    • Modificad el contenido de los ficheros a y b de la carpeta Seguridad y cread un nuevo fichero llamado f.
    • Cread dentro de la carpeta Backups una carpeta cuyo nombre sea la fecha actual en formato dd-mm-aaaa.
    • Cread dentro de la carpeta Backups una carpeta cuyo nombre sea SeguridadLinkDest.
    • Situaros mediante la terminal en la carpeta Seguridad.
    • Ejecutad el siguiente comando, sustituyendo “fechaactual” por la fecha correspondiente en el formato indicado:
	$ rsync -av --link-dest=/var/tmp/Backups/SeguridadLinkDest . 		/var/tmp/Backups/fechaactual 
¿Qué hace exactamente ese comando? ¿Qué aparece en el directorio con la fecha actual? ¿Qué significan los parametros “/var/tmp/Backups/SeguridadLinkDest”,”.”, y “/var/tmp/Backups/fechaactual” que se usan en el comando?
    • En el directorio Seguridad borrad el fichero c, añadid cambios a los ficheros a y e, y cread un fichero g ($ echo "G" > G).
    • Vamos a simular el paso del tiempo. Cread dentro de la carpeta Backups una carpeta cuyo nombre sea la fecha de mañana en formato dd-mm-aaaa.
    • Situaros mediante la terminal en el directorio Seguridad y ejecutad el siguiente comando, sustituyendo “fechamañana” por la fecha correspondiente en el formato indicado:
	$ rsync -av --link-dest=/var/tmp/Backups/fechaactual . 	/var/tmp/Backups/fechamañana
¿Qué se encuentra en el directorio con la fecha de mañana? ¿Qué ha ocurrido y por qué?
    • Modificad el contenido del fichero g.
¿Qué comando sería necesario para realizar en la carpeta Backups/fechapasadomañana una copia de seguridad sólo con el fichero modificado desde la anterior copia de seguridad (La que tiene fecha de mañana)?
    • Borrad todo el contenido del directorio Seguridad.
¿Qué comandos son necesarios para restaurar el contenido completo a partir de la penúltima de las copias de seguridad (La que tiene fecha de mañana)?
Ejecutad el siguiente comando en varios directorios de la carpeta Backups:
$ ls -ali /var/tmp/Backups/fechamañana
Hay dos números importantes a tener en cuenta: (1) Antes de los permisos, un número con muchos dígitos, por ejemplo 1150561; (2) Después de los permisos, un número pequeño, siempre 1 o mayor (1, 2, o 3 en este caso) ¿Qué significan? ¿Qué utilidad pueden tener a la hora de hacer copias de seguridad?
Automatización de tareas
    • Cread un script Cron que realice una copia de seguridad incremental de la carpeta Seguridad cada día a las 12 del mediodía. Cada copia se deberá realizar en una carpeta distinta, cuyo nombre será la fecha del día que se hizo la respectiva copia. 
Al trabajar con Cron, si el comando que tiene que ejecutar Cron es muy largo o la tarea está compuesta por varios comandos a la vez, es muy común crear un Shell Script que es el que es ejecutado por Cron. 
Copias de seguridad remotas
Realizar las copias de seguridad en la misma máquina en la que está la información que deseamos preservar no es una buena idea. Lo mejor es realizar las copias en una máquina remota: vamos a usar la máquina remota de Google Cloud para hacer las copias de seguridad en ella mediante el protocolo SSH.
Recrea los ejercicios del laboratorio 1 sobre rsync, pero haz las copias de seguridad en el servidor remoto Google Cloud mediante SSH. 
¿En qué cambia el comando rsync sobre SSH? 
¿Cómo es la versión del comando cp sobre SSH?
