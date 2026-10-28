# Laboratorio: Subredes en Google Cloud

## Requisitos previos

- Proyecto de Google Cloud con créditos activos (ver laboratorio [Servidor remoto Google Cloud](../../Servidor_remoto_Google_Cloud/Servidor_remoto_Google_Cloud.md)).
- Pareja de claves SSH pública y privada.

## Introducción

Este laboratorio despliega una pequeña aplicación web de agenda telefónica con dos niveles de red separados:

- **Nivel web**: una instancia Compute Engine con una aplicación Web Python, accesible desde internet por SSH y HTTP.
- **Nivel de base de datos**: una instancia Cloud SQL (MySQL), accesible únicamente desde el nivel web.

El objetivo es practicar la segmentación de red mediante subredes VPC y reglas de firewall.

## Crear la red VPC y las subredes

En el menú de navegación, ir a `VPC network` > `VPC networks` > `Create VPC network`:

- Nombre: `phonebook-vpc`.
- Modo de creación de subredes: `Custom`.
- Añadir una subred:
  - Nombre: `web-subnet`.
  - Región: una región dentro de Europa.
  - Rango de direcciones IPv4: `10.0.1.0/24`.
- Añadir una segunda subred:
  - Nombre: `db-subnet`.
  - Región: la misma región que `web-subnet`.
  - Rango de direcciones IPv4: `10.0.2.0/24`.

Pulsar `Create`.

## Crear las reglas de firewall

Ir a `VPC network` > `Firewall` > `Create firewall rule`.

Regla para el nivel web:

- Nombre: `phonebook-allow-web`.
- Red: `phonebook-vpc`.
- Dirección de tráfico: `Ingress`.
- Destinos: `Specified target tags`, etiqueta `http-server`.
- Filtro de origen: `IPv4 ranges`, rango `0.0.0.0/0`.
- Protocolos y puertos: `TCP`, puertos `22, 80`.

Regla para el nivel de base de datos:

- Nombre: `phonebook-allow-db`.
- Red: `phonebook-vpc`.
- Dirección de tráfico: `Ingress`.
- Destinos: `Specified target tags`, etiqueta `db-server`.
- Filtro de origen: `IPv4 ranges`, rango `10.0.1.0/24` (la subred `web-subnet`).
- Protocolos y puertos: `tcp`, puerto `3306`.

## Crear la instancia del servidor web

Ir a `Compute Engine` > `VM instances` > `Create instance`.

- Nombre: `phonebook-web`.
- Región/zona: la misma región que `web-subnet`.
- Serie: `E2`, tipo de máquina: `e2-micro`.
- `OS and storage`: `Ubuntu 26.04 LTS Minimal` como sistema operativo.
- `Networking`:
  - Activar el tráfico HTTP (`Allow HTTP traffic`).
  - En `Network interfaces`, seleccionar la red `phonebook-vpc` y la subred `web-subnet`.
  - Reservar una IP externa estática (`External IPv4 address` > `Reserve static external IP address`).
- `Security` > `Manage access`: añadir la clave pública SSH (`Add manually generated SSH keys`).
- `Advanced options` > `Management` > `Automation`: pegar el siguiente script de arranque para instalar y configurar automáticamente la aplicación:

```bash
sudo apt-get update
sudo apt-get install -y apache2 python3-pymysql
sudo a2enmod cgid
systemctl restart apache2
cd /usr/lib/cgi-bin/
wget https://raw.githubusercontent.com/mikel-egana-aranguren/EHU-SGSSI-01/refs/heads/develop/Laboratorios/Seguridad_red/vpc-google-cloud/index.py
sudo chmod +x index.py
sudo chown www-data:www-data index.py
```

Crear la instancia. Visitar `http://IP_EXTERNA_SERVIDOR_WEB/cgi-bin/index.py` y debería aparecer el siguiente error, ya que no se puede conectar a la BBDD: `Database error: (2003, "Can't connect to MySQL server on 'DB_PRIVATE_IP' ([Errno -3] Temporary failure in name resolution)")`


## Crear la base de datos (Cloud SQL)

Ir a `Cloud SQL` > `Instances` > `Create free instance` (Cloud SQL gratis durante 30 dias) > `MySQL`:

- Database Engine: `MySQL`.
- Instance ID: `phonebook-db`.
- Contraseña del usuario `root`.
- Versión de base de datos: `MySQL 8.0`.
- Región: la misma que `db-subnet`.

Editar la instancia: 
- `Connections`:
  - Desactivar `Public IP`.
  - Activar `Private IP` y seleccionar la red `phonebook-vpc`. Si se solicita, seguir el asistente para reservar un rango de IP y habilitar el acceso a servicios privados (`Service Networking API`).

Guardar. 

- Pestaña `Databases` > `Create database`: nombre `mydb`.
- Pestaña `Users` > `Add user account`: usuario `admin` con una contraseña.

Añadir los datos de `addressbook.sql`.

## Conectar el servidor web con la base de datos

Conectarse por SSH a `phonebook-web` y editar el archivo de configuración de la aplicación con los datos de conexión a la base de datos (IP privada de la instancia Cloud SQL, nombre de la base de datos, usuario y contraseña creados en el paso anterior):

```
HOSTNAME = "DB_PRIVATE_IP"
USERNAME = "admin"
PASSWORD = "DB_PASSWORD"
DATABASE = "mydb"
```

## Probar la aplicación

Visitar `http://IP_EXTERNA_SERVIDOR_WEB/cgi-bin/index.py`. Deberían aparecer datos de la agenda.



