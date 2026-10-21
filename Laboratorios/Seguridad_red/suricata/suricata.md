# Laboratorio: Suricata

## Requisitos previos

- Una de las dos opciones:
  - Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar lsi si es necesario, mediante el comando `su - lsi`).
  - Proyecto de Google Cloud con créditos activos (ver laboratorio [Servidor remoto Google Cloud](../../Servidor_remoto_Google_Cloud/Servidor_remoto_Google_Cloud.md)) y pareja de claves SSH pública y privada.
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable.

## Introducción

[Suricata](https://suricata.io) es un motor de seguridad de red de código abierto que funciona como IDS (*Intrusion Detection System*), IPS (*Intrusion Prevention System*) y NSM (*Network Security Monitoring*). Inspecciona en tiempo real el tráfico que atraviesa una interfaz de red, lo compara contra un conjunto de reglas (*rulesets*) y genera alertas cuando detecta tráfico sospechoso o malicioso (escaneos de puertos, explotación de vulnerabilidades conocidas, tráfico hacia dominios maliciosos, etc.).

Este laboratorio despliega Suricata en modo IDS (solo detección, sin bloquear tráfico) sobre una máquina local o sobre una instancia de Google Cloud, y comprueba su funcionamiento generando tráfico que debería disparar una alerta.

## Preparar la máquina

Elegir una de las dos opciones:

- **Local**: usar directamente la máquina GNU/Linux.
- **Google Cloud**: crear una instancia Compute Engine (`Compute Engine` > `VM instances` > `Create instance`):
  - Nombre: `suricata-vm`.
  - Serie: `E2`, tipo de máquina: `e2-medium` (Suricata necesita algo más de CPU/RAM que `e2-micro`).
  - `OS and storage`: `Ubuntu 26.04 LTS Minimal` como sistema operativo.
  - `Networking`: activar el tráfico HTTP (`Allow HTTP traffic`).
  - `Security` > `Manage access`: añadir la clave pública SSH (`Add manually generated SSH keys`).
  - Crear la instancia y conectarse por SSH.

Localizar la interfaz de red por la que pasa el tráfico a vigilar:

```bash
ip -br a
```

`lo` es la interfaz de loopback; la interfaz activa (`UP`) con una IP asignada (por ejemplo `eth0` o `ens4`) es la que usará Suricata.

## Instalar Suricata

```bash
sudo add-apt-repository ppa:oisf/suricata-stable
sudo apt update
sudo apt install -y suricata
```

Comprobar la versión instalada y que el servicio existe:

```bash
suricata --build-info
systemctl status suricata --no-pager
```

## Configuración básica

El fichero principal de configuración es `/etc/suricata/suricata.yaml`. Editarlo (`sudo nano /etc/suricata/suricata.yaml`) y ajustar dos parámetros:

- `HOME_NET`: la red que se considera "propia". Por defecto vale `any`; para esta práctica se puede dejar así o restringirla a la IP/red de la máquina.
- La interfaz de captura, en la sección `af-packet`, sustituyendo `eth0` por la interfaz localizada en el paso anterior:

```yaml
af-packet:
  - interface: eth0
```

## Descargar y actualizar las reglas

Suricata necesita un conjunto de reglas para saber qué tráfico es sospechoso. `suricata-update` descarga el ruleset gratuito de Emerging Threats (ET Open) y lo instala:

```bash
sudo suricata-update
```

> ¿Cuántas reglas se han descargado? (Pista: el propio comando lo indica al finalizar).

## Ejecutar Suricata

Lanzar Suricata en primer plano sobre la interfaz elegida, para ver los mensajes de arranque:

```bash
sudo suricata -c /etc/suricata/suricata.yaml -i eth0
```

Si no hay errores, dejar este proceso corriendo y abrir otra terminal (otra sesión SSH si es Google Cloud) para el resto de la práctica. También se puede lanzar como servicio en segundo plano:

```bash
sudo systemctl enable --now suricata
```

## Generar tráfico y comprobar las alertas

Generar una petición que Suricata debería detectar con una regla del ruleset ET Open, usando el dominio de pruebas [testmyids.com](http://testmyids.com):

```bash
curl http://testmyids.com
```

Consultar el registro de alertas en texto plano:

```bash
sudo tail -n 20 /var/log/suricata/fast.log
```

Debería aparecer una línea con una alerta de tipo `GPL ATTACK_RESPONSE id check returned root`, indicando que Suricata ha detectado la respuesta característica de `testmyids.com`.

También se puede consultar el registro en formato JSON, más completo. Instalar `jq` para filtrar el JSON cómodamente:

```bash
sudo apt install -y jq
sudo tail -n 5 /var/log/suricata/eve.json | jq 'select(.event_type=="alert")'
```

> ¿Qué campos aparecen en el evento de tipo `alert` del fichero `eve.json`? ¿Qué información aportan `signature`, `severity` y `src_ip`/`dest_ip` frente al mensaje de `fast.log`?

Probar ahora con un escaneo de puertos, instalando `nmap` si no está disponible:

```bash
sudo apt install -y nmap
nmap -sS localhost
```

> Vuelve a consultar `fast.log` y `eve.json`. ¿Ha generado alertas el escaneo? ¿Qué firma(s) han saltado?

> Cambia `HOME_NET` en `suricata.yaml` a un valor distinto (por ejemplo `[10.0.0.0/8]` en vez de `any`), reinicia Suricata (`sudo systemctl restart suricata`) y repite la prueba con `curl http://testmyids.com`. ¿Cambia el resultado? ¿Por qué `HOME_NET` afecta a qué tráfico se considera "entrante" o "saliente" en las reglas?

## Limpieza

Si se ha usado una instancia de Google Cloud, eliminar la instancia `suricata-vm` para evitar costes. 