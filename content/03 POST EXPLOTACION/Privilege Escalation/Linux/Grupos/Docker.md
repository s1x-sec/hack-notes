---
tags: [privesc, linux, docker]
---

# Docker Group

Añadir un usuario al grupo docker es prácticamente equivalente a tener acceso de root al sistema de archivos, sin necesidad de contraseña.

```bash
docker image ls

# Montar /root del host dentro del contenedor
docker run -v /root:/mnt -it ubuntu
```

Una vez dentro:
- Acceder a archivos del host
- Leer o añadir claves SSH de root
- Montar `/etc` → leer `/etc/shadow` para crackear contraseñas offline
- Añadir usuarios con privilegios elevados

