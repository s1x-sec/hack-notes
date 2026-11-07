---
tags: [privesc, linux]
---

# Privilege Escalation — Linux

## Checklist

- [ ] OS, Kernel y servicios corriendo (`uname -a`, `cat /etc/os-release`)
- [ ] Otros usuarios logados: `ps au`
- [ ] Directorios home — claves SSH, scripts, configs, `.bashrc`, `history`
- [ ] `sudo -l` — permisos de sudo sobre comandos
- [ ] `sudo -V` — versión de sudo vulnerable?
- [ ] Aliases: `alias`
- [ ] Grupos especiales: `id` → ir a [[Grupos Linux]]
- [ ] Procesos como root: `ps aux | grep root` (combinar con **pspy64**)
- [ ] Binarios SUID/SGID → [[SETUID Linux]]
- [ ] Capabilities: `getcap -r / 2>/dev/null`
- [ ] Tareas programadas: `crontab -l`, `cat /etc/crontab` (también pspy)
- [ ] Puertos internos — si hay web interna → explotar → usuario `www-data`
- [ ] Credenciales perdidas → [[Búsqueda de Credenciales Linux]]
- [ ] Permisos sobre `/etc/passwd`
- [ ] Exploits de kernel

---

## SUID / SGID

```bash
find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null   # SUID
find / -user root -perm -6000 -exec ls -ldb {} \; 2>/dev/null   # SGID
find / -type f -perm -4000 2>/dev/null
```

→ Binario sospechoso: consultar **GTFOBins**

---

## Capabilities

```bash
getcap -r / 2>/dev/null
```

---

## Tareas Programadas

```bash
crontab -l
cat /etc/crontab 2>/dev/null
# Ver procesos en tiempo real
./pspy64
```

---

## Puertos Internos

```bash
ss -tlnp
netstat -tlnp
```


---

## Navegación

| Técnica | Nota |
|---------|------|
| Búsqueda de Credenciales | [[Búsqueda de Credenciales Linux]] |
| SETUID/SGID | [[SETUID Linux]] |
| Path Abuse | [[Path Abuse Linux]] |
| Wildcard Abuse | [[Wildcard Abuse]] |
| Shell Restrictiva | [[Shell Restrictiva]] |
| Grupos (Docker, LXD, Disk, ADM) | [[Grupos/Grupos Linux]] |
| ADM | [[Grupos/ADM]] |
| Disk | [[Grupos/Disk]] |
| Docker | [[Grupos/Docker]] |
| LXC/LXD | [[Grupos/LXC-LXD]] |
