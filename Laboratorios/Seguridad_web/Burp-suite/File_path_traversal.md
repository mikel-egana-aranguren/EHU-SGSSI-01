# Laboratorio: File path traversal

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar usuario `lsi` si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.
- Burp suite, Firefox + FoxyProxy, cuenta personal en PortSwigger (Ver laboratorio `SQL injection`). 

## File path traversal with superfluous URL-encode

El path traversal, también conocido como directory traversal, es un tipo de vulnerabilidad que permite a un atacante leer archivos en el servidor que ejecuta una aplicación, como por ejemplo código y datos de la aplicación, credenciales de sistemas backend, o archivos sensibles del sistema operativo. Esto se hace explotando los paths que maneja la aplicación atacada.


burp 

firefox con foxy proxy

logearse en portswigger


 La aplicación elimina las secuencias de path traversal del nombre de archivo proporcionado por el usuario antes de utilizarlo.

Para resolver el laboratorio, hay que leer el archivo `/etc/passwd`.

https://portswigger.net/web-security/file-path-traversal/lab-sequences-stripped-non-recursively

Acceder al labo

IMG

Con `Ctrl+u`, podemos ver el codiog fuente de la pagina:

IMG

Hay veremos que esta el codigo HTML para las imagenes, por ejemplo:

```html
<div>
                            <img src="/image?filename=27.jpg">
                            <h3>The Trolley-ON</h3>
                            <img src="/resources/images/rating1.png">
                            $16.16
                            <a class="button" href="/product?productId=1">View details</a>
                        </div>
                        ```

De vuelta la web, si abrimos una imagen en otra pestaña

Hay que activar las imagens en Burp Proxy HTTP history filter settings

IMG

IMG



https://....web-security-academy.net/image?filename=27.jpg


Buscar la peticion en Burp y enviarla al repeater

Podemos probar a poner `/etc/passwd` en la peticion del filename, no deja:

IMG

lo mismo con ../../../etc/passwd

Explicar ENCODING DECODING

..%252f..%252f..%252fetc/passwd



DIAGRAMA resumen

