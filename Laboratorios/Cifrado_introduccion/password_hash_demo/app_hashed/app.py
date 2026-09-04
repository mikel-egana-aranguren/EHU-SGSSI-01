import hashlib
import os
import psycopg2
from flask import Flask, render_template_string, request

app = Flask(__name__)
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://demo:demo123@db:5432/demo')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username and password:
            stored = hash_password(password)
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        'INSERT INTO users_hashed (username, password_hash) VALUES (%s, %s) ON CONFLICT (username) DO UPDATE SET password_hash = EXCLUDED.password_hash',
                        (username, stored),
                    )
            message = 'Usuario registrado con hash SHA-256.'

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT username, password_hash FROM users_hashed ORDER BY id')
            users = cur.fetchall()

    html = '''
    <!doctype html>
    <html>
    <head>
        <title>Hashed Password Storage</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2rem; background: #f7f7ff; }
            form { margin-bottom: 2rem; }
            input { margin: 0.5rem 0; padding: 0.5rem; display: block; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }
            .warning { color: #7a5200; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Versión con hash</h1>
        <p class="warning">Se almacena un hash SHA-256 en vez de la contraseña.</p>
        <form method="post">
            <label>Nombre de usuario</label>
            <input name="username" placeholder="usuario">
            <label>Contraseña</label>
            <input name="password" type="password" placeholder="contraseña">
            <button type="submit">Registrar</button>
        </form>
        {% if message %}<p>{{ message }}</p>{% endif %}
        <h2>Usuarios almacenados</h2>
        <table>
            <tr><th>Usuario</th><th>Hash</th></tr>
            {% for user, password_hash in users %}
            <tr><td>{{ user }}</td><td>{{ password_hash }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html, message=message, users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
