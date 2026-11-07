---
tags: [privesc, linux, suid]
---

# SETUID / SGID

Permite ejecutar un programa o script con los permisos de otro usuario.

## SETUID

```bash
find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null
```

## SETGID

```bash
find / -user root -perm -6000 -exec ls -ldb {} \; 2>/dev/null
```

Siempre que veamos alguno sospechoso → revisar **GTFOBins**: https://gtfobins.github.io/

