# Laboratorio: DevSecOps

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar usuario `lsi` si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.

## DevSecOps

DevSecOps (Development, Security, Operations) integra la seguridad en el desarrollo y la operación del software. En este laboratorio construiremos una aplicación pequeña, ejecutaremos pruebas y análisis de seguridad y automatizaremos estas comprobaciones en GitHub Actions.

Usaremos herramientas sobre código y dependencias propios. No incluyas contraseñas, tokens ni otros secretos en el repositorio. Si un análisis encuentra un problema, revisa el resultado y corrige la causa antes de volver a ejecutar los controles.

## Preparar el proyecto

Crea un repositorio en GitHub llamado devsecops-demo y clonalo. Comprueba que tienes Python 3 y Docker:

```bash
python3 --version
docker --version
```

Crea un entorno virtual para que las dependencias del laboratorio no se mezclen con las del sistema:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Asegurate de que aparece `(.venv)` en la terminal, antes del prompt:

```bash
[bgpegarm@U113356 DevSecOpsDemo]$ source .venv/bin/activate
(.venv) [bgpegarm@U113356 DevSecOpsDemo]$
```

## Crear y probar una aplicación

Crea el archivo `app.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return {"message": "Aplicación de demostración DevSecOps"}
```

Crea el archivo `requirements.txt` con la dependencia de la aplicación:

```text
Flask>=3,<4
```

Instala la dependencia y ejecuta la aplicación localmente:

```bash
python -m pip install -r requirements.txt
flask --app app run
```

Visita <http://127.0.0.1:5000/> y comprueba la respuesta. Detén el servidor con `Ctrl+C`.

Crea `tests/test_app.py`:

```python
from app import app


def test_index():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.json == {
        "message": "Aplicación de demostración DevSecOps"
    }
```

Instala las herramientas de desarrollo y ejecuta la prueba:

```bash
python -m pip install pytest bandit pip-audit
python -m pytest
```

> ¿Qué comprueba la prueba y qué información ofrece si falla?

> ¿Por qué instalamos las dependencias en un entorno virtual?

> ¿Qué diferencia hay entre las dependencias de la aplicación y las herramientas de desarrollo?

## Analizar el código y las dependencias

Bandit busca patrones potencialmente inseguros en código Python. Ejecuta el análisis sobre el archivo de la aplicación:

```bash
bandit app.py
```

`pip-audit` comprueba si las dependencias declaradas tienen vulnerabilidades conocidas:

```bash
pip-audit -r requirements.txt
```

Si una herramienta informa de hallazgos, lee el detalle, identifica el archivo o paquete afectado y aplica una corrección. Vuelve a ejecutar las pruebas y los análisis para verificar el resultado.

> ¿Qué tipo de problemas puede encontrar Bandit? ¿Qué problemas no puede descartar?

> ¿Por qué una prueba correcta no demuestra por sí sola que la aplicación sea segura?

> ¿Qué información necesitas para decidir cómo responder a una vulnerabilidad de una dependencia?

## 5. Construir y ejecutar un contenedor

Crea un archivo `Dockerfile` en el directorio del proyecto:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER 10001
EXPOSE 5000
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000"]
```

Construye la imagen:

```bash
docker build -t devsecops-demo .
```

Ejecuta el contenedor y publica el servicio solo en la interfaz local de la máquina:

```bash
docker run --rm -p 127.0.0.1:5000:5000 devsecops-demo
```

Visita <http://127.0.0.1:5000/> y detén el contenedor con `Ctrl+C`.

> ¿Qué instrucciones del Dockerfile instalan la dependencia y copian el código?

> ¿Qué usuario ejecuta la aplicación dentro del contenedor?

> ¿Por qué el puerto se publica en `127.0.0.1` y no en todas las interfaces de red?

> ¿Qué riesgos introduce incluir credenciales o archivos innecesarios en la imagen?

Como comprobación adicional, puedes analizar la imagen con [Trivy](https://trivy.dev/). Para instalarlo, seguir las [instrucciones](https://trivy.dev/docs/latest/getting-started/installation/#debianubuntu-official):

```bash
sudo apt-get install wget gnupg
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

Analizar imagen:

```bash
trivy image devsecops-demo
```

Revisa el resumen y las recomendaciones. Un escáner ayuda a priorizar riesgos, pero no sustituye la revisión de la imagen base ni garantiza que no existan vulnerabilidades.

## Automatizar los controles con GitHub Actions

Crea el directorio `.github/workflows` y el archivo `.github/workflows/security.yml` en la raiz del repositorio:

```yaml
name: Pruebas y seguridad

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - name: Obtener el código
        uses: actions/checkout@v4

      - name: Preparar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Instalar dependencias y herramientas
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt pytest bandit pip-audit

      - name: Ejecutar pruebas
        run: pytest

      - name: Analizar código
        run: bandit app.py

      - name: Auditar dependencias
        run: pip-audit -r requirements.txt

      - name: Construir imagen
        run: docker build -t devsecops-demo .
```

Guarda y sube los archivos al repositorio:

```bash
git add .github/ Dockerfile app.py requirements.txt tests/test_app.py
git commit -m "Añadir laboratorio DevSecOps"
git push
```

Consulta la pestaña **Actions** del repositorio y comprueba el resultado de cada paso. Si un control falla, revisa sus mensajes, corrige el problema y vuelve a subir los cambios.

> ¿En qué eventos se ejecuta este flujo de trabajo?

> ¿Qué sucede con el flujo si una prueba o un análisis falla?

>  ¿Por qué el workflow declara `contents: read` en vez de conceder permisos amplios?

> ¿Qué controles añadirías para comprobar secretos o analizar la imagen construida?

## Mejora continua

La automatización da feedback repetible, pero el equipo sigue siendo responsable de interpretar los resultados y mantener los controles. En un proyecto real:

- Fija y actualiza las versiones de las dependencias de forma controlada.
- Revisa los permisos del pipeline y concede únicamente los necesarios.
- Protege los secretos con el almacén del sistema de CI; no los escribas en el código ni en los logs.
- Revisa periódicamente las imágenes base y reconstruye las imágenes para incorporar actualizaciones.
- Prioriza los hallazgos según su impacto y exposición, y documenta las decisiones.
