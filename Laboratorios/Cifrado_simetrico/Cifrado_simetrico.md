# Laboratorio: Cifrado simétrico

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Herramientas necesarias: OpenSSL (`sudo apt install openssl`).
- Repositorio GitHub de asignatura: puedes subir los programa desarrollados en el laboratorio.

## Ataque fuerza bruta al cifrado César

Crea un programa, en el lenguaje que quieras, que realice un ataque de fuerza bruta contra el siguiente mensaje: "Uunejvxb dw vdwmx wdnex jzdr, nw wdnbcaxb lxajixwnb". Es decir, el programa tiene que inferir la clave y usarla para descifrar el mensaje (PISTA: detección de idioma en Python). 

## Ataque fuerza bruta al cifrado simple por sustitución

Crea un programa, en el lenguaje que quieras, que realice un ataque de fuerza bruta contra el siguiente mensaje:

RIJ AZKKZHC PIKCE XT ACKCUXJHX SZX, E NZ PEJXKE, PXGIK XFDKXNEQE RIPI RIPQEHCK ET OENRCNPI AXNAX ZJ RKCHXKCI AX CJAXDXJAXJRCE AX RTENX, E ACOXKXJRCE AXT RITEQIKERCIJCNPI OKXJHXDIDZTCNHE AX TE ACKXRRCIJ EJEKSZCNHE.

AZKKZHC OZX ZJ OERHIK AX DKCPXK IKAXJ XJ XT DEDXT AX TE RTENX IQKXKE XJ REHETZJVE XJ GZTCI AX 1936. DXKI AZKKZHC, RIPI IRZKKX RIJ TEN DXKNIJETCAEAXN XJ TE MCNHIKCE, JI REVI AXT RCXTI. DXKNIJCOCREQE TE HKEACRCIJ KXvITZRCIJEKCE AX TE RTENX IQKXKE. NZ XJIKPX DIDZTEKCAEA XJHKX TE RTENX HKEQEGEAIKE, KXOTXGEAE XJ XT XJHCXKKI PZTHCHZACJEKCI XJ QEKRXTIJE XT 22 AX JIvCXPQKX AX 1936, PZXNHKE XNE CAXJHCOCRERCIJ. NZ PZXKHX OZX NCJ AZAE ZJ UITDX IQGXHCvI ET DKIRXNI KXvITZRCIJEKCI XJ PEKRME. NCJ AZKKZHC SZXAI PEN TCQKX XT REPCJI DEKE SZX XT XNHETCJCNPI, RIJ TE RIPDTCRCAEA AXT UIQCXKJI AXT OKXJHX DIDZTEK V AX TE ACKXRRCIJ EJEKSZCNHE, HXKPCJEKE XJ PEVI AX 1937 TE HEKXE AX TCSZCAEK TE KXvITZRCIJ, AXNPIKETCLEJAI E TE RTENX IQKXKE V OERCTCHEJAI RIJ XTTI XT DINHXKCIK HKCZJOI OKEJSZCNHE.

El mensaje está en castellano y deberás usar el análisis de frecuencias mediante la siguiente tabla:

![Frecuencias](Fecuencias.png)

(PISTA: el programa puede ser interactivo).

## Cifrado de flujo mediante XOR

Implementa un programa que cifre y descifre mensajes mediante un cifrado de flujo sencillo. El programa debe:

- Leer un mensaje y una clave de la misma longitud, representados como cadenas de bytes.
- Aplicar la operación XOR byte a byte entre el mensaje y la clave para obtener el criptograma.
- Usar la misma operación XOR para recuperar el mensaje original a partir del criptograma.
- Mostrar el mensaje original, la clave y el criptograma en hexadecimal.
- Comprobar que el descifrado del criptograma produce exactamente el mensaje original.

Utiliza los siguientes datos de prueba:

- Mensaje: `ATAQUE AL AMANECER`
- Clave: `CLAVE12345678901`

## Cifrado y descifrado con OpenSSL

Utiliza la herramienta `openssl enc` desde un terminal de Ubuntu para cifrar y descifrar un archivo con AES, Triple DES y DES. No tienes que implementar ningún programa.

Prepara un mensaje y una contraseña en archivos separados:

```bash
printf '%s\n' 'La criptografia protege la confidencialidad de la informacion.' > mensaje.txt
printf '%s\n' 'Laboratorio2026' > clave.txt
```

Cifra y descifra el mensaje con AES-256-CBC:

```bash
openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -salt \
	-in mensaje.txt -out mensaje.aes -pass file:clave.txt
openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
	-in mensaje.aes -out mensaje.aes.descifrado -pass file:clave.txt
cmp mensaje.txt mensaje.aes.descifrado
```

Repite la práctica con Triple DES y DES:

```bash
openssl enc -des-ede3-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -salt -in mensaje.txt -out mensaje.3des \
	-pass file:clave.txt
openssl enc -d -des-ede3-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -in mensaje.3des -out mensaje.3des.descifrado \
	-pass file:clave.txt
cmp mensaje.txt mensaje.3des.descifrado

openssl enc -des-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -salt -in mensaje.txt -out mensaje.des \
	-pass file:clave.txt
openssl enc -d -des-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -in mensaje.des -out mensaje.des.descifrado \
	-pass file:clave.txt
cmp mensaje.txt mensaje.des.descifrado
```

Compara el tamaño de los criptogramas y verifica su integridad mediante sus sumas SHA-256:

```bash
sha256sum mensaje.txt mensaje.aes mensaje.3des mensaje.des
sha256sum mensaje.aes.descifrado mensaje.3des.descifrado mensaje.des.descifrado
```

¿Que quiere decir CBC en `-des-ede3-cbc`?¿Hay otras opciones?







