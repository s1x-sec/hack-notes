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
- [ ] Grupos especiales: `id` → ir a [[03-post-explotacion/privilege-escalation/linux/grupos/grupos-linux|Grupos Linux]]
- [ ] Procesos como root: `ps aux | grep root` (combinar con **pspy64**)
- [ ] Binarios SUID/SGID → [[03-post-explotacion/privilege-escalation/linux/setuid-linux|SETUID Linux]]
- [ ] Capabilities: `getcap -r / 2>/dev/null`
- [ ] Tareas programadas: `crontab -l`, `cat /etc/crontab` (también pspy)
- [ ] Puertos internos — si hay web interna → explotar → usuario `www-data`
- [ ] Credenciales perdidas → [[03-post-explotacion/privilege-escalation/linux/búsqueda-de-credenciales-linux|Búsqueda de Credenciales Linux]]
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
| Búsqueda de Credenciales | [[03-post-explotacion/privilege-escalation/linux/búsqueda-de-credenciales-linux\|Búsqueda de Credenciales Linux]] |
| SETUID/SGID | [[03-post-explotacion/privilege-escalation/linux/setuid-linux\|SETUID Linux]] |
| Path Abuse | [[03-post-explotacion/privilege-escalation/linux/path-abuse-linux\|Path Abuse Linux]] |
| Wildcard Abuse | [[03-post-explotacion/privilege-escalation/linux/wildcard-abuse\|Wildcard Abuse]] |
| Shell Restrictiva | [[03-post-explotacion/privilege-escalation/linux/shell-restrictiva\|Shell Restrictiva]] |
| Grupos (Docker, LXD, Disk, ADM) | [[03-post-explotacion/privilege-escalation/linux/grupos/grupos-linux\|Grupos Linux]] |
| ADM | [[03-post-explotacion/privilege-escalation/linux/grupos/adm\|ADM]] |
| Disk | [[03-post-explotacion/privilege-escalation/linux/grupos/disk\|Disk]] |
| Docker | [[03-post-explotacion/privilege-escalation/linux/grupos/docker\|Docker]] |
| LXC/LXD | [[03-post-explotacion/privilege-escalation/linux/grupos/lxc-lxd\|LXC-LXD]] |
