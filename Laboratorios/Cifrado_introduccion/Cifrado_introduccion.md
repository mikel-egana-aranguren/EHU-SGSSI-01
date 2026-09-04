# Laboratorio: Introduccion al cifrado, esteganografia y algoritmos resumen

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Herramientas necesarias: `openssl`, `sha512sum`, `git`, `steghide`.

## Esteganografía práctica

En este bloque ocultaremos un mensaje dentro de una imagen contenedora.

Si `steghide` no esta instalado:

```bash
sudo apt update
sudo apt install steghide -y
```

Preparar mensaje:

```bash
echo "SGSSI-26-27 Software is like sex: it's better when it's free" > msg_linus
```

Insertar mensaje con contraseña en imagen `linus.jpg`:

```bash
steghide embed -cf linus.jpg -ef msg_linus -sf linus_steg.jpg
```

Extraccion del mensaje oculto (Primero renombrar archivo original mensaje a `msg_linus_old`):

```bash
steghide extract -sf linus_steg.jpg
less msg_linus
```

Tamaño del contenedor:

```bash
ls -lh linus.jpg linus_steg.jpg
```

## Integridad con funciones hash

Cálculo de resúmenes:

```bash
echo "Este fichero verifica integridad" > integridad.txt
md5sum integridad.txt
sha256sum integridad.txt
```

Modifica un solo caracter y vuelve a calcular los resúmenes. ¿Cómo han cambiado?

## Integridad y esteganografia

Compara los hashes de los mensajes usados en la esteganografía: 

```bash
sha256sum msg_linus
sha256sum msg_linus_old
```

¿Coinciden? 

Compara los hashes de los ficheros contenedor:

```bash
sha256sum linus.jpg
sha256sum linus_steg.jpg
```

¿Coinciden? 

Hay un mensaje importante de Buenaventura Durruti para vosotros en una de las imagenes del directorio `durruti`. El mensaje ha sido introducido mediante el programa steghide, con contraseña "durruti". La imagen que contiene el mensaje se corresponde con el Hash (SHA256) `7d573924d70a604cb56122aed9bded3f40d3083d8adc353a97c0b816c0e573bb`. ¿Qué archivo es? ¿Qué dice la frase? ¿Como automatizarías la búsqueda si tuvieses muchos archivos en carpetas y subcarpetas?

## Contraseñas y sal

Ejecuta:

```bash
echo -n "ContrasenaSegura" | sha256sum
echo -n "ContrasenaSegura" | sha256sum
```

Observa que el resultado es idéntico.

Uso de sal con OpenSSL:

```bash
openssl passwd -6 -salt SAL001 ContrasenaSegura
openssl passwd -6 -salt SAL002 ContrasenaSegura
```

¿Cambian los Hashes?

En la carpeta `password_hash_demo` tienes una pequeña aplicación web con tres versiones de la misma funcionalidad:

- `plain`: almacena la contraseña en texto plano.
- `hashed`: almacena un hash SHA-256 de la contraseña.
- `salted`: almacena un salt aleatorio y un hash PBKDF2-HMAC-SHA256.

Para ejecutarla:

```bash
cd password_hash_demo
docker compose up --build
```

Después abre:

- http://localhost:5001/ -> versión insegura (texto plano)
- http://localhost:5002/ -> versión con hash
- http://localhost:5003/ -> versión con sal

Registra el mismo usuario y la misma contraseña en las tres versiones y compara la base de datos o la información mostrada por cada servicio. Fíjate en que:

- En texto plano se ve la contraseña original;
- Con hash, la misma contraseña produce el mismo valor hash para todos los usuarios;
- Con sal, cada usuario tiene un salt distinto, por lo que iguales contraseñas no generan el mismo valor almacenado.

Despliega el proyecto en tu servidor Google Cloud y comprueba que funciona correctamente, y que puedes cambiar la sal a "457897821372183721".

## Hashes y Git

Clona, si no lo has hecho ya, el repositorio de la asignatura (Usando SSH):

```bash
git clone git@github.com:mikel-egana-aranguren/EHU-SGSSI-01.git
cd cd EHU-SGSSI-01/
git log
```

¿Qué identifica el hash del commit?¿Por qué Git detecta cambios de contenido de forma eficiente?


