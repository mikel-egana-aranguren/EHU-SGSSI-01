# Demo: contraseñas en texto plano, hash y sal

Este proyecto muestra tres versiones de la misma aplicación web para comparar cómo se almacenan las contraseñas.

## Servicios incluidos

- `plain`: almacena la contraseña en texto plano.
- `hashed`: almacena una suma SHA-256 de la contraseña.
- `salted`: almacena un salt aleatorio y la contraseña hasheada con PBKDF2-HMAC-SHA256.

## Arranque

```bash
cd EHU-SGSSI-01/Laboratorios/Cifrado_introduccion/password_hash_demo
docker compose up --build
```

Luego abre:

- http://localhost:5001/  -> versión insegura
- http://localhost:5002/  -> versión con hash
- http://localhost:5003/  -> versión con sal

## Cómo usarlo

1. Registra un usuario con la misma contraseña en cada versión.
2. Mira la base de datos o la vista de usuarios del navegador.
3. Comprueba que:
   - en la versión `plain`, la contraseña se ve tal cual.
   - en la versión `hashed`, todos los hashes iguales para la misma contraseña.
   - en la versión `salted`, cada usuario tiene un salt distinto y el hash cambia incluso con la misma contraseña.

## Conceptos clave

- Sin sal: dos usuarios con la misma contraseña comparten el mismo hash.
- Con sal: el mismo password produce hashes distintos al usar un valor aleatorio por usuario.
- El almacenamiento en texto plano es vulnerable y debe evitarse siempre.

## Limpieza

```bash
docker compose down -v
```
