# Laboratorio: Seguridad red

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.
- Cuenta Google Cloud.

## Captura de tráfico de red mediante WireShark

[WireShark](https://www.wireshark.org) es un sniffer para visualizar trafico entrante y saliente de un host concreto. Para instalar, en la web Wireshark pinchar en "Download Now", "Stable release 4.6.9" y luego en "Ubuntu", seguir las instrucciones:

```bash
sudo add-apt-repository ppa:wireshark-dev/stable
sudo apt update
sudo apt install wireshark
```

Hay que elegir "Si" en la pregunta de seguridad. De lo contrario:

```bash
sudo dpkg-reconfigure wireshark-common
sudo usermod -aG wireshark $USER
```

Y volver a logearse con ese usuario.

Localizar la interfaz de red:

```bash
ip -br a
```

`lo` es el interfaz de loopback, es decir el localhost conectandose a si mismo. Normalmente las interfaces activas aparecen como `UP`. Elegir interfaz en Wirewhark y pinchar en capturar. 

Abrir una web en el navegador, por ejemplo `https://phrack.org/issues/72/linenoise_md#article`. Parar la captura y filtrar por HTTP para buscar la primera peticion GET.

> ¿Qué protocolos se usan? ¿Que bits del mensaje se corresponden con cada uno?