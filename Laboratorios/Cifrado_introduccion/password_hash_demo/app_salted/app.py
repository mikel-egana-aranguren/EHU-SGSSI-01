import hashlib
import os
import secrets
import psycopg2
from flask import Flask, render_template_string, request

app = Flask(__name__)
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://demo:demo123@db:5432/demo')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn


def hash_password_with_salt(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100_000).hex()


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username and password:
            salt = secrets.token_hex(16)
            stored_hash = hash_password_with_salt(password, salt)
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        'INSERT INTO users_salted (username, salt, password_hash) VALUES (%s, %s, %s) ON CONFLICT (username) DO UPDATE SET salt = EXCLUDED.salt, password_hash = EXCLUDED.password_hash',
                        (username, salt, stored_hash),
                    )
            message = 'Usuario registrado con salt aleatorio y hash PBKDF2.'

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT username, salt, password_hash FROM users_salted ORDER BY id')
            users = cur.fetchall()

    html = '''
    <!doctype html>
    <html>
    <head>
        <title>Salted Password Storage</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2rem; background: #f7fff7; }
            form { margin-bottom: 2rem; }
            input { margin: 0.5rem 0; padding: 0.5rem; display: block; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }
            .safe { color: #0b6b3a; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Versión con sal</h1>
        <p class="safe">Cada usuario tiene un salt distinto y se usa PBKDF2-HMAC-SHA256.</p>
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
            <tr><th>Usuario</th><th>Salt</th><th>Hash</th></tr>
            {% for user, salt, password_hash in users %}
            <tr><td>{{ user }}</td><td>{{ salt }}</td><td>{{ password_hash }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html, message=message, users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
