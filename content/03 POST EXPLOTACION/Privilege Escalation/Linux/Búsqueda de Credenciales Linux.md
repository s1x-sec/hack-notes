---
tags: [privesc, linux, credentials]
---

# Búsqueda de Credenciales — Linux

> [!tip]
> Cada escenario puede ser diferente ya sea para un pentest real o para un CTF — lo que hay aquí son paths y tips recopilados en experiencia real.

## Rutas Clásicas

```bash
find / ! -path "*/proc/*" -iname "*config*" -type f 2>/dev/null

grep 'DB_USER\|DB_PASSWORD' wp-config.php

/home/$USER/.ssh/id_rsa
/var/www/*
history
/root/.ssh/id_rsa
```

## Búsqueda Masiva de Credenciales

```bash
find / \( -path /proc -o -path /sys -o -path /usr -o -path /snap -o -path /lib \) \
  -prune -o -type f \( -name "*.conf" -o -name "*.config" -o -name ".env" \) \
  -readable -exec grep -HniE "pass|user|key|token|secret|pwd|credential" {} \; 2>/dev/null
```

## Ficheros Shell

```bash
find / -type f -name "*.sh" 2>/dev/null | grep -v "src\|snap\|share"
```

## Ficheros History

```bash
find / -type f \( -name *_hist -o -name *_history \) -exec ls -l {} \; 2>/dev/null
```

