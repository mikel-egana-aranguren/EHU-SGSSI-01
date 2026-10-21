# Laboratorio: Balanceador de carga en Google Cloud

## Requisitos previos

- Proyecto de Google Cloud con créditos activos (ver laboratorio [Servidor remoto Google Cloud](../../Servidor_remoto_Google_Cloud/Servidor_remoto_Google_Cloud.md)).
- Pareja de claves SSH pública y privada.

## Introducción

Este laboratorio despliega un servicio web replicado en varias instancias de Compute Engine, y un balanceador de carga HTTP que reparte las peticiones entre ellas:

- **Nivel de backend**: un grupo de instancias gestionado (`Managed Instance Group`) con dos servidores web Apache, cada uno de los cuales muestra su propio nombre de host.
- **Nivel de balanceo**: un balanceador de carga HTTP(S) externo con una única IP pública, que comprueba la salud de las instancias y solo envía tráfico a las que responden correctamente.

El objetivo es practicar la disponibilidad y la distribución de tráfico, y comprobar que el servicio sigue funcionando aunque una instancia falle.

## Crear la red VPC y la regla de firewall

En el menú de navegación, ir a `VPC network` > `VPC networks` > `Create VPC network`:

- Nombre: `lb-vpc`.
- Modo de creación de subredes: `Custom`.
- Añadir una subred:
  - Nombre: `lb-subnet`.
  - Región: una región dentro de Europa.
  - Rango de direcciones IPv4: `10.0.1.0/24`.

Pulsar `Create`.

Ir a `VPC network` > `Firewall` > `Create firewall rule`.

Regla para el tráfico de usuarios y del balanceador:

- Nombre: `lb-allow-web`.
- Red: `lb-vpc`.
- Dirección de tráfico: `Ingress`.
- Destinos: `Specified target tags`, etiqueta `lb-backend`.
- Filtro de origen: `IPv4 ranges`, rangos `130.211.0.0/22` y `35.191.0.0/16` (balanceador y comprobaciones de salud de Google).
- Protocolos y puertos: `TCP`, puerto `80`.

Regla para la administración:

- Nombre: `lb-allow-ssh`.
- Red: `lb-vpc`.
- Dirección de tráfico: `Ingress`.
- Destinos: `Specified target tags`, etiqueta `lb-backend`.
- Filtro de origen: `IPv4 ranges`, rango `0.0.0.0/0`.
- Protocolos y puertos: `TCP`, puerto `22`.

## Crear la plantilla de instancia

Ir a `Compute Engine` > `Instance templates` > `Create instance template`.

- Nombre: `lb-template`.
- Serie: `E2`, tipo de máquina: `e2-micro`.
- `OS and storage`: `Ubuntu 26.04 LTS Minimal` como sistema operativo.
- `Networking`:
  - Etiqueta de red: `lb-backend`.
  - En `Network interfaces`, seleccionar la red `lb-vpc` y la subred `lb-subnet`.
- `Security` > `Manage access`: añadir la clave pública SSH (`Add manually generated SSH keys`).
- `Advanced options` > `Management` > `Automation`: pegar el siguiente script de arranque, que instala Apache y publica una página con el nombre de la instancia:

```bash
sudo apt-get update
sudo apt-get install -y apache2
echo "<h1>Servidor: $(hostname)</h1>" | sudo tee /var/www/html/index.html
sudo systemctl restart apache2
```

Pulsar `Create`.

## Crear el grupo de instancias gestionado

Ir a `Compute Engine` > `Instance groups` > `Create instance group` > `New managed instance group (stateless)`:

- Nombre: `lb-mig`.
- Plantilla de instancia: `lb-template`.
- Ubicación: `Multiple zones` en la región de `lb-subnet`.
- Número de instancias: `2` (autoescalado desactivado).
- `Port mapping`: nombre `http`, puerto `80`.
- `Autohealing` > `Create a health check`:
  - Nombre: `lb-health-check`.
  - Protocolo: `HTTP`, puerto `80`, ruta `/`.

Pulsar `Create`. Esperar a que las dos instancias estén en ejecución.

## Crear el balanceador de carga

Ir a `Network services` > `Load balancing` > `Create load balancer`:

- Tipo: `Application Load Balancer (HTTP/HTTPS)`.
- Público (`Internet facing`), global.
- Nombre: `lb-http`.

Configuración:

- `Frontend configuration`:
  - Nombre: `lb-frontend`.
  - Protocolo: `HTTP`, puerto `80`.
  - IP: `Create IP address`, nombre `lb-ip` (IP externa estática).
- `Backend configuration` > `Create a backend service`:
  - Nombre: `lb-backend-service`.
  - Tipo de backend: `Instance group`.
  - Grupo de instancias: `lb-mig`, puerto `80`.
  - Comprobación de salud: `lb-health-check`.
- `Host and path rules`: dejar las reglas por defecto.

Pulsar `Create`. La puesta en marcha del balanceador puede tardar varios minutos.

## Probar el balanceador

Visitar `http://IP_BALANCEADOR` (la IP `lb-ip`) y recargar la página varias veces (o ejecutar `for i in $(seq 1 20); do curl -s http://IP_BALANCEADOR; done`). Debería aparecer el nombre de las distintas instancias del grupo.

## Probar la tolerancia a fallos

1. Conectarse por SSH a una de las instancias y detener Apache: `sudo systemctl stop apache2`.
2. Tras unos segundos la comprobación de salud marcará la instancia como no saludable (`Load balancing` > `lb-http` > `Backends`).
3. Volver a visitar `http://IP_BALANCEADOR`: todas las respuestas proceden de la instancia restante.
4. Reiniciar Apache (`sudo systemctl start apache2`) y comprobar que la instancia vuelve a recibir tráfico.

## Limpieza

Para evitar costes, eliminar el balanceador (`lb-http`), el grupo de instancias (`lb-mig`), la plantilla (`lb-template`), la IP estática (`lb-ip`), las reglas de firewall y la red `lb-vpc`.
