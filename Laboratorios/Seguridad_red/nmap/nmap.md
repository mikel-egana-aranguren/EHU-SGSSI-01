# Laboratorio: NMap

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar lsi si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.
- Cuenta Google Cloud (ver laboratorio [Servidor remoto Google Cloud](../../Servidor_remoto_Google_Cloud/Servidor_remoto_Google_Cloud.md)).

## NMap

[Nmap](https://nmap.org/) es un programa de código abierto que sirve para rastrear puertos y máquinas en una red (probablemente sea la herramienta de hacking que aparece en más películas: [https://nmap.org/movies/](https://nmap.org/movies/)). Con Nmap se pueden descubrir fácilmente muchas características de las máquinas que están visibles en la red: qué máquinas están encendidas, qué puertos tiene abiertos una máquina concreta, qué servicios está ejecutando y qué versiones de los mismos, qué sistema operativo y qué versión usa, etc.

Instala NMap:

```bash
sudo apt install nmap
```

Describe los comandos necesarios para descubrir lo siguiente:

> ¿Qué puertos están abiertos en `scanme.nmap.org` y en tu servidor de Google Cloud, qué servicios y qué versión de esos servicios?

> ¿Qué máquinas están activas en la red desde tu máquina hasta tu servidor remoto? (Pista: `traceroute`).

> ¿Qué puertos tiene abiertos una de las máquinas activas de la red?

> ¿Qué versiones de los servicios está usando una de las máquinas activas de la red?

> ¿Qué sistema operativo tiene una de las máquinas activas de la red?

> ¿Qué sistema operativo tiene tu servidor en Google Cloud (según NMap)?

> ¿Qué sistema operativo tiene `scanme.nmap.org`?

> Una vez determinado el sistema operativo, ¿qué vulnerabilidades tiene? (Pista: [https://cve.mitre.org](https://cve.mitre.org/)).

> ¿Cómo se puede usar NMap para detectar si una máquina tiene un firewall?
