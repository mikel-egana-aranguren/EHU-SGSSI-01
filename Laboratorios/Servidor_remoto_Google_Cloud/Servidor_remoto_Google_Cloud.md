# Laboratorio: Servidor remoto Google Cloud

## Requisitos previos

- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Dos cuentas de correo: 
  - Correo universidad (@ehu.eus, @ikasle.ehu.eus) para obtener los créditos Google Cloud.
  - Correo Gmail nuevo (Por ejemplo mi_nombre_sgssi_26_27@gmail.com) para usar el servicio Google Cloud durante el curso.
- Pareja de claves SSH pública y privada (Se puede usar la misma que para GitHub o generar una nueva).

## Introducción

[Google Cloud](https://cloud.google.com/) es la plataforma de Google para computación en la nube. Ofrece créditos gratuitos para [educación](https://cloud.google.com/billing/docs/how-to/edu-grants) que usaremos para crear un servidor y trabajar con él, conectándonos al mismo mediante SSH.

## Obtener el crédito y crear un proyecto

Entrar en Gmail en la cuenta creada para el curso (**IMPORTANTE**: no tiene que haber ninguna otra pestaña abierta con otra cuenta Gmail abierta). En otra pestaña nueva, entrar en [Google Cloud Console](https://console.cloud.google.com):

![Google Cloud Console no project](GoogleCloudConsole_no_project.png)

(**IMPORTANTE**: no pinchar en los créditos de 300$).

Pinchar en `Select a project` y luego en `New project`:

![Google Cloud Console select project new project](GoogleCloudConsole_select_project_new_project.png)

Crear un proyecto, por ejemplo "SGSSI-26-27" y seleccionarlo; pinchar en `Select a project` y luego en `SGSSI-26-27`:

![Google Cloud Console select project SGSSI-26-27](GoogleCloudConsole_select_project_sgssi_26_27.png)










Añadir clave SSH profesor en usuario nuevo

En el servidor, crear usuario bgpegarm, en el grupo sudoer y con contraseña "lsi".
Añadir la clave pública del profesor en el directorio home de ese usuario, en .ssh/authorized_keys.
Enviar IP (Sólo IP) en entrega.
