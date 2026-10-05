#!/usr/bin/env python3
# CGI script: queries the address table and renders it as HTML.
# Deploy to /usr/lib/cgi-bin/index.py on Ubuntu + Apache (mod_cgi).
import html
import pymysql

# Edit these four values with your Cloud SQL connection details
HOSTNAME = "DB_PRIVATE_IP"
USERNAME = "admin"
PASSWORD = "DB_PASSWORD"
DATABASE = "mydb"

print("Content-Type: text/html\n")
print("<!DOCTYPE html><html><head><title>Agenda telefónica</title></head><body>")
print("<h1>Agenda</h1>")

try:
    conn = pymysql.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, database=DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT name, phone, email FROM address;")
    rows = cur.fetchall()

    print('<table border="1" cellpadding="5">')
    print("<tr><th>name</th><th>phone</th><th>email</th></tr>")
    for name, phone, email in rows:
        print(f"<tr><td>{html.escape(name)}</td><td>{html.escape(phone)}</td><td>{html.escape(email)}</td></tr>")
    print("</table>")

    cur.close()
    conn.close()
except Exception as e:
    print(f"<p>Database error: {html.escape(str(e))}</p>")

print("</body></html>")
