# Laboratorio: Bitcoin

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar usuario `lsi` si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.
- Docker y Docker Compose instalados y funcionando (Ver [laboratorio Docker](../Docker/Docker.md)).
- `openssl` y `xxd` instalados (`sudo apt install openssl xxd`).

## Introducción

[Bitcoin](https://bitcoin.org/bitcoin.pdf) es una red peer-to-peer y un protocolo que permite transferir valor entre dos partes sin necesidad de un intermediario de confianza (banco, pasarela de pago, etc.). Fue descrito en 2008 por Satoshi Nakamoto en el artículo [Bitcoin: A Peer-to-Peer Electronic Cash System](s70423-290181-707862.pdf), que combina herramientas que ya hemos visto en la asignatura (funciones resumen, cifrado asimétrico, firmas digitales) para resolver el problema del "doble gasto" sin un servidor central.

Los elementos principales del protocolo son:

- **Blockchain**: una cadena de bloques donde cada bloque contiene un conjunto de transacciones. Cada bloque incluye el hash (SHA-256) del bloque anterior, de modo que los bloques quedan encadenados: modificar un bloque antiguo obligaría a recalcular todos los bloques posteriores.
- **Prueba de trabajo (Proof of Work)**: para añadir un bloque nuevo a la cadena, los mineros tienen que encontrar un valor tal que el hash del bloque sea menor que un objetivo (`target`) determinado por la dificultad de la red. Encontrar ese valor requiere mucho cómputo, pero comprobar que es válido es inmediato.
- **Monederos, claves y direcciones**: cada usuario genera un par de claves asimétricas. La clave privada permite firmar transacciones (demostrar propiedad de los fondos) y la dirección pública se deriva de la clave pública aplicando funciones resumen (SHA-256 y RIPEMD-160).
- **Transacciones y UTXO**: en vez de un balance de cuenta, Bitcoin utiliza un modelo de "salidas de transacción no gastadas" (UTXO). Cada transacción consume una o varias salidas de transacciones anteriores (entradas) y genera nuevas salidas, algunas para el destinatario y otra, opcionalmente, como "cambio" de vuelta al emisor.

Montar un nodo completo de Bitcoin conectado a la red real (*mainnet*) requiere descargar y validar toda la blockchain (cientos de GB) y esperar tiempos de bloque reales (~10 minutos). Para este laboratorio usaremos **regtest**, un modo de Bitcoin Core pensado para desarrollo y pruebas locales: funciona de manera totalmente aislada, sin conectarse a ningún otro nodo, y permite minar bloques de forma instantánea bajo demanda. Esto nos permite experimentar con monederos, minado y transacciones sin usar dinero real ni esperar.

## Instalación y configuración

En vez de compilar o instalar Bitcoin Core directamente en el sistema, vamos a ejecutar un nodo `bitcoind` dentro de un contenedor, usando la imagen [`ruimarinho/bitcoin-core`](https://hub.docker.com/r/ruimarinho/bitcoin-core).

Descarga la imagen:

```bash
docker pull ruimarinho/bitcoin-core
```

Ejecuta un contenedor con el nodo en modo `regtest`:

```bash
docker run -d --name bitcoind-regtest ruimarinho/bitcoin-core -regtest=1 -server=1 -fallbackfee=0.0002
```

> ¿Qué hacen los parámetros `-regtest=1` y `-server=1`?

El parámetro `-fallbackfee` fija una comisión por defecto para las transacciones: en una red real la comisión se estima a partir de la actividad reciente de la red, pero en nuestra `regtest` local, recién creada, todavía no hay datos suficientes para hacer esa estimación.

Comprueba que el contenedor está funcionando:

```bash
docker ps
```

El cliente de línea de comandos `bitcoin-cli` ya viene instalado en la imagen. Como el proceso `bitcoind` se ejecuta dentro del contenedor con el usuario `bitcoin`, hay que indicarlo al ejecutar comandos mediante `docker exec`:

```bash
docker exec -u bitcoin bitcoind-regtest bitcoin-cli -regtest getblockchaininfo
```

> En el resultado anterior, ¿Cuántos bloques tiene la cadena? ¿Por qué?

Para no repetir `docker exec -u bitcoin bitcoind-regtest bitcoin-cli` en cada comando, puedes definir un alias en la terminal (sólo dura mientras la terminal esté abierta):

```bash
alias bitcoin-cli="docker exec -u bitcoin bitcoind-regtest bitcoin-cli -regtest"
bitcoin-cli getblockchaininfo
```

## Monederos y direcciones

Crea un monedero (wallet) en el nodo:

```bash
bitcoin-cli createwallet "labw"
```

Genera una dirección nueva dentro del monedero:

```bash
bitcoin-cli getnewaddress
```

Guarda la dirección en una variable para reutilizarla:

```bash
ADDR=$(bitcoin-cli getnewaddress)
echo $ADDR
```

Cada dirección tiene detrás un par de claves. Para verlo:

```bash
bitcoin-cli getaddressinfo $ADDR
```

> ¿Qué campo contiene la clave pública?

> ¿Qué campo contiene el resultado de aplicar funciones resumen a la clave pública?

Vamos a comprobar manualmente que esa dirección realmente se obtiene aplicando un resumen hash a la clave pública. Sustituye `PUBKEY` por el valor del campo `pubkey` obtenido arriba:

```bash
echo -n "PUBKEY" | xxd -r -p | openssl dgst -sha256 -binary | openssl dgst -rmd160
```

> ¿Coincide el resultado con el campo `witness_program` de `getaddressinfo`? ¿Qué pasaría con la dirección si cambiase un solo carácter de la clave pública?

Tus claves privadas nunca deberían salir de tu monedero. Por defecto, un monedero de Bitcoin Core es un monedero "HD" (jerárquico determinista): a partir de una única clave privada maestra se derivan todas las direcciones. Para verla (**Sólo en este entorno de pruebas, nunca en un monedero real**):

```bash
bitcoin-cli listdescriptors true
```

> En el campo `desc`, ¿Qué parte corresponde a la clave privada maestra (empieza por `tprv`)? Si alguien obtiene esa clave, ¿Qué puede hacer con los fondos asociados a todas las direcciones del monedero?

## Mineria y prueba de trabajo

En `regtest` no hay otros mineros con los que competir, así que podemos pedirle directamente al nodo que mine bloques y que la recompensa de cada bloque vaya a una dirección concreta:

```bash
bitcoin-cli generatetoaddress 101 $ADDR
```

> ¿Por qué pedimos 101 bloques en vez de 1 (Pista: `bitcoin-cli getbalance`, y busca información sobre el "periodo de madurez" de las recompensas de minado)?

Comprueba el saldo del monedero:

```bash
bitcoin-cli getbalance
```

Inspecciona el último bloque minado:

```bash
HASH_BLOCK=$(bitcoin-cli getbestblockhash)
bitcoin-cli getblock $HASH_BLOCK
```

> ¿Qué campo contiene el hash del bloque anterior (`previousblockhash`)? ¿Para qué sirve este campo?

> ¿Qué campo contiene el `nonce`? ¿Para qué se usa en la prueba de trabajo?

> ¿Qué campos reflejan la dificultad de minado (`bits`, `difficulty`)? ¿Por qué en `regtest` la dificultad es tan baja?

 Siguiendo el campo `previousblockhash` de bloque en bloque, ¿A qué bloque se llega al final? Puedes automatizar el recorrido con un script, o hacerlo a mano varias veces.

## Transacciones y UTXOs

Genera una segunda dirección, que representará a otro usuario (Por ejemplo un compañero o compañera de clase):

```bash
ADDR_2=$(bitcoin-cli getnewaddress "destiny")
```

Envía una cantidad desde el monedero a la nueva dirección:

```bash
TXID=$(bitcoin-cli sendtoaddress $ADDR_2 1.5)
echo $TXID
```

La transacción está ahora en la mempool, es decir, en espera de ser incluida en un bloque:

```bash
bitcoin-cli getmempoolentry $TXID
```

> ¿Qué pasaría si, antes de confirmar esta transacción, intentásemos gastar las mismas monedas en otra transacción diferente (Doble gasto)? ¿Quién lo evita en una red real, donde sí hay varios mineros compitiendo?

Mina un bloque para confirmar la transacción:

```bash
bitcoin-cli generatetoaddress 1 $ADDR
```

Consulta la transacción ya confirmada:

```bash
bitcoin-cli gettransaction $TXID
```

Para ver el detalle completo de entradas y salidas (modelo UTXO) necesitamos también el hash del bloque que la confirma:

```bash
HASH_BLOCK=$(bitcoin-cli getbestblockhash)
bitcoin-cli getrawtransaction $TXID true $HASH_BLOCK
```

> ¿Cuántas entradas (`vin`) y cuántas salidas (`vout`) tiene la transacción?

> Una de las salidas va a `$ADDR_2`. ¿A qué dirección va la otra salida, y qué representa?

> Calcula la diferencia entre el valor total de las entradas y el valor total de las salidas. ¿A qué corresponde esa diferencia?

Una UTXO (Unspent Transaction Output, o salida de transacción no gastada) es la cantidad de bitcoin que queda disponible tras una transacción y que aún no se ha gastado. El saldo de una billetera no es un número único en una cuenta, sino la suma de todas las UTXO asociadas a sus direcciones.

## Explorando la red con un explorador de bloques

Para visualizar la blockchain de manera más cómoda que con `bitcoin-cli`, vamos a desplegar un explorador de bloques web conectado a nuestro nodo, usando Docker Compose.

Sitúa la terminal en un directorio nuevo y crea un archivo `docker-compose.yml` con el siguiente contenido:

```yaml
services:
  bitcoind:
    image: ruimarinho/bitcoin-core
    container_name: bitcoind-explorer
    command:
      - -regtest=1
      - -server=1
      - -rpcallowip=0.0.0.0/0
      - -rpcbind=0.0.0.0
      - -rpcuser=labw
      - -rpcpassword=labw
      - -fallbackfee=0.0002

  explorer:
    image: getumbrel/btc-rpc-explorer:v3.5.1
    depends_on:
      - bitcoind
    environment:
      BTCEXP_HOST: 0.0.0.0
      BTCEXP_BITCOIND_HOST: bitcoind
      BTCEXP_BITCOIND_PORT: 18443
      BTCEXP_BITCOIND_USER: labw
      BTCEXP_BITCOIND_PASS: labw
      BTCEXP_NETWORK: regtest
    ports:
      - "3002:3002"
```

Este archivo define dos servicios: `bitcoind`, con un nuevo nodo en `regtest` (independiente del contenedor `bitcoind-regtest` de los apartados anteriores), y `explorer`, la aplicación web [btc-rpc-explorer](https://github.com/janoside/btc-rpc-explorer), que se conecta al servicio `bitcoind` usando su nombre de servicio como host (Docker Compose crea una red donde los contenedores se resuelven entre sí por nombre).

Despliega los servicios:

```bash
docker compose up -d
```

Mina algunos bloques y realiza alguna transacción en este nuevo nodo (Repitiendo los pasos de los apartados 3, 4 y 5, sustituyendo `bitcoind-regtest` por `bitcoind-explorer` en los comandos `docker exec`), y después visita el explorador en <http://localhost:3002>.

> Busca en el explorador un bloque y una transacción que hayas creado. ¿Coincide la información con la que obtenías mediante `bitcoin-cli`?

> Navega hacia atrás, bloque a bloque, hasta llegar al bloque de altura 0. ¿Cómo se llama ese bloque especial?

Para parar los servicios:

```bash
docker compose down
```