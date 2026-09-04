import os
import psycopg2
from flask import Flask, render_template_string, request

app = Flask(__name__)
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://demo:demo123@db:5432/demo')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username and password:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        'INSERT INTO users_plain (username, password) VALUES (%s, %s) ON CONFLICT (username) DO UPDATE SET password = EXCLUDED.password',
                        (username, password),
                    )
            message = 'Usuario registrado con contraseña en texto plano.'

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT username, password FROM users_plain ORDER BY id')
            users = cur.fetchall()

    html = '''
    <!doctype html>
    <html>
    <head>
        <title>Plain Password Storage</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2rem; background: #fff7f7; }
            form { margin-bottom: 2rem; }
            input { margin: 0.5rem 0; padding: 0.5rem; display: block; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }
            .danger { color: #a00; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Versión insegura: texto plano</h1>
        <p class="danger">Esta versión guarda la contraseña tal cual en la base de datos.</p>
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
            <tr><th>Usuario</th><th>Contraseña</th></tr>
            {% for user, password in users %}
            <tr><td>{{ user }}</td><td>{{ password }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html, message=message, users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
