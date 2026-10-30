# Laboratorio: Ataques Web

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar usuario `lsi` si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.

## Burp suite

Burp suite es una herramienta de pen-testing para realizar ataques web. Vamos a usarla para realizar ataques web a los sitios vulnerables que ofrece PortSwigger en sus laboratorios (https://portswigger.net/web-security/all-labs).

Para instalar BurpSuite, ir a (https://portswigger.net/burp/communitydownload), bajar instalador y ejecutarlo. Elegir "community edition". Lanzar Burp Suite con buscador de aplicaciones.  

Ir a (http://localhost:8080/) y descargar certificado ("CA certificate"). Para añadir el certificado en Firefox, ir a Ajustes; Privacidad & Seguridad; Seguridad de la conexión y del software; Administrador de certificados; Import (Marcar las dos casillas de confiar). 

En Firefox tambien hay que instalar FoxyProxy. Ir a https://addons.mozilla.org/es-ES/firefox/addon/foxyproxy-standard/ y pulsar en el boton añadir. Una vez activado en Firefox, pulsar en FoxyProxy; 
Opciones; Proxy; Añadir:

- Titulo: BURP
- Hostname: 127.0.0.1 
- Puerto: 8080
- Tipo: HTTP

## Injección SQL en Portswigger labs


