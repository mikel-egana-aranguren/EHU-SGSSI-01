# Laboratorio: Introduccion al cifrado, esteganografia y algoritmos resumen

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).







- Herramientas disponibles: `openssl`, `sha256sum`, `md5sum`, `git`.
- Opcional para esteganografia: `steghide`.

Comprobacion rapida:

```bash
openssl version
sha256sum --version
git --version
```

Si `steghide` no esta instalado:

```bash
sudo apt update
sudo apt install steghide -y
```



## Esteganografía práctica

En este bloque ocultaremos un mensaje dentro de una imagen contenedora.

### 2.1 Preparacion de ficheros

```bash
mkdir -p labo_cifrado_intro/estego
cd labo_cifrado_intro/estego
echo "SGSSI-26-27: mensaje oculto de prueba" > secreto.txt
```

Descarga o copia una imagen JPEG de prueba como `portada.jpg`.

### 2.2 Insercion de mensaje con contrasena

```bash
steghide embed -cf portada.jpg -ef secreto.txt -sf portada_stego.jpg
```

El comando solicitara una contrasena.

### 2.3 Extraccion del mensaje oculto

```bash
steghide extract -sf portada_stego.jpg
cat secreto.txt
```

Pregunta 3:

- Que ocurre si introduces una contrasena incorrecta?
- Por que combinar cifrado + esteganografia mejora la robustez?

### 2.4 Tamano e integridad del contenedor

```bash
ls -lh portada.jpg portada_stego.jpg
sha256sum portada.jpg portada_stego.jpg
```

Pregunta 4:

- Compara tamano y hash de ambos ficheros.
- Razona por que una transformacion de formato (ejemplo: JPEG -> PNG -> JPEG) puede destruir el mensaje oculto.

---

## 3) Integridad con funciones hash

### 3.1 Calculo de resumenes

En `labo_cifrado_intro`:

```bash
cd ..
echo "Este fichero verifica integridad" > integridad.txt
md5sum integridad.txt
sha256sum integridad.txt
sha3sum -a 256 integridad.txt 2>/dev/null || echo "sha3sum no disponible"
```

### 3.2 Efecto avalancha

Modifica un solo caracter:

```bash
echo "Este fichero verifica integridad." > integridad.txt
md5sum integridad.txt
sha256sum integridad.txt
```

Pregunta 5:

- Copia los hashes antes y despues.
- Explica el efecto avalancha en 2-3 lineas.

### 3.3 Verificacion de integridad tipo distribucion de software

```bash
echo "abc123  integridad.txt" > checksum_incorrecto.txt
sha256sum -c checksum_incorrecto.txt || true
sha256sum integridad.txt > checksum_correcto.txt
sha256sum -c checksum_correcto.txt
```

Pregunta 6:

- Que riesgo existe si una web publica un fichero y su hash en un canal no autenticado?

---

## 4) Contrasenas y sal

### 4.1 Problema sin sal

```bash
echo -n "ContrasenaSegura" | sha256sum
echo -n "ContrasenaSegura" | sha256sum
```

Observa que el resultado es identico.

### 4.2 Uso de sal con OpenSSL

```bash
openssl passwd -6 -salt SAL001 ContrasenaSegura
openssl passwd -6 -salt SAL002 ContrasenaSegura
```

Pregunta 7:

- Explica por que la misma contrasena genera hashes distintos al cambiar la sal.
- Relaciona este resultado con ataques de tablas precalculadas.

### 4.3 Formato de almacenamiento en Linux

Muestra un ejemplo sintetico del formato de `/etc/shadow`:

`usuario:$6$SAL$HASH:...`

Pregunta 8:

- Que representa el `6`?
- Que parte corresponde a la sal?

---

## 5) Colisiones y riesgos criptograficos

### 5.1 MD5 en contexto actual

Pregunta 9:

- Investiga y resume brevemente por que MD5 esta roto criptograficamente.
- Indica en que casos podria seguir apareciendo (contextos heredados, control no critico de duplicados, etc.).

### 5.2 Caso de ataque por colision

Consulta un caso historico de colisiones practicas (por ejemplo, SHA-1 SHAttered).

Pregunta 10:

- Describe el impacto potencial sobre:
	- Integridad de documentos
	- Certificados o identidad digital

---

## Actividad opcional (ampliacion)

Relacion entre hashes y Git:

```bash
mkdir -p git_hash_demo
cd git_hash_demo
git init
echo "version 1" > ejemplo.txt
git add ejemplo.txt
git commit -m "primer commit"
git log --oneline -1
```

Pregunta opcional:

- Que identifica el hash del commit?
- Por que Git detecta cambios de contenido de forma eficiente?


