---
tags: [post-explotacion]
---

# 03 POST EXPLOTACION

---

## Transferencia de Ficheros

| Plataforma | Nota |
|-----------|------|
| Linux | [[03-post-explotacion/transferencia-de-ficheros/transferencia-linux\|Transferencia Linux]] |
| Windows | [[03-post-explotacion/transferencia-de-ficheros/transferencia-windows\|Transferencia Windows]] |

---

## Credential Access

| Técnica | Nota |
|---------|------|
| OS Credential Dumping (LSASS, SAM, DCSync) | [[03-post-explotacion/credential-access/os-credential-dumping\|OS Credential Dumping]] |
| Kerberos Tickets (Rubeus, BOFs) | [[03-post-explotacion/credential-access/kerberos-tickets\|Kerberos Tickets]] |
| Cracking (hashcat) | [[03-post-explotacion/cracking\|Cracking]] |

---

## Persistencia

| Técnica | Nota |
|---------|------|
| Índice de Persistencia | [[03-post-explotacion/persistencia\|Persistencia]] |
| Scheduled Tasks (CS) | [[03-post-explotacion/persistencia/scheduled-tasks-cs\|Scheduled Tasks CS]] |
| Registry Keys & Startup Folder | [[03-post-explotacion/persistencia/registry-keys--and--startup-folder\|Registry Keys & Startup Folder]] |
| PowerShell Profile | [[03-post-explotacion/persistencia/powershell-profile\|PowerShell Profile]] |
| Logon Scripts | [[03-post-explotacion/persistencia/logon-scripts\|Logon Scripts]] |
| COM Hijacking | [[03-post-explotacion/persistencia/com-hijacking\|COM Hijacking]] |
| **Persistencia Avanzada** | |
| Scheduled Task avanzada | [[03-post-explotacion/persistencia/persistencia-avanzada/scheduled-task\|Scheduled Task]] |
| Windows Service | [[03-post-explotacion/persistencia/persistencia-avanzada/windows-service\|Windows Service]] |
| WMI Eventing | [[03-post-explotacion/persistencia/persistencia-avanzada/wmi/wmi-eventing\|WMI Eventing]] |
| WMI Queries | [[03-post-explotacion/persistencia/persistencia-avanzada/wmi/wmi-queries\|WMI Queries]] |
| WMI Remote Triggers | [[03-post-explotacion/persistencia/persistencia-avanzada/wmi/wmi-remote-triggers\|WMI Remote Triggers]] |

---

## Escalada de Privilegios — Linux

| Técnica | Nota |
|---------|------|
| Checklist Linux PrivEsc | [[03-post-explotacion/privilege-escalation/linux/linux-privesc\|Linux PrivEsc]] |
| Búsqueda de Credenciales | [[03-post-explotacion/privilege-escalation/linux/búsqueda-de-credenciales-linux\|Búsqueda de Credenciales Linux]] |
| SETUID/SGID | [[03-post-explotacion/privilege-escalation/linux/setuid-linux\|SETUID Linux]] |
| Path Abuse | [[03-post-explotacion/privilege-escalation/linux/path-abuse-linux\|Path Abuse Linux]] |
| Wildcard Abuse | [[03-post-explotacion/privilege-escalation/linux/wildcard-abuse\|Wildcard Abuse]] |
| Shell Restrictiva | [[03-post-explotacion/privilege-escalation/linux/shell-restrictiva\|Shell Restrictiva]] |
| Grupos (Docker/LXD/Disk/ADM) | [[03-post-explotacion/privilege-escalation/linux/grupos/grupos-linux\|Grupos Linux]] |

---

## Escalada de Privilegios — Windows

| Técnica | Nota |
|---------|------|
| Índice Windows PrivEsc | [[03-post-explotacion/privilege-escalation/windows/privesc-windows\|PrivEsc Windows]] |
| Servicios Débiles | [[03-post-explotacion/privilege-escalation/windows/servicios/servicios-windows\|Servicios Windows]] |
| DLL Hijacking | [[03-post-explotacion/privilege-escalation/windows/dll-hijacking\|DLL Hijacking]] |
| Binary Hijacking | [[03-post-explotacion/privilege-escalation/windows/binary-hijacking\|Binary Hijacking]] |
| Unquoted Paths | [[03-post-explotacion/privilege-escalation/windows/path-hijacking/unquoted-paths\|Unquoted Paths]] |
| Search Order Hijacking | [[03-post-explotacion/privilege-escalation/windows/path-hijacking/search-order-hijacking\|Search Order Hijacking]] |
| PATH Env Variable | [[03-post-explotacion/privilege-escalation/windows/path-hijacking/path-environment-variable\|PATH Environment Variable]] |
| Tareas Programadas | [[03-post-explotacion/privilege-escalation/windows/schtasks\|Schtasks]] |
| Privilegios de Token | [[03-post-explotacion/privilege-escalation/windows/privilegios/privilegios-windows\|Privilegios Windows]] |
| Credenciales almacenadas | [[03-post-explotacion/privilege-escalation/windows/credenciales/credenciales-windows\|Credenciales Windows]] |
| UAC Bypass | [[03-post-explotacion/privilege-escalation/windows/uac-bypass\|UAC Bypass]] |
| Local Service Privs | [[03-post-explotacion/privilege-escalation/windows/local-service-privs\|Local Service Privs]] |
| Living Off the Land | [[03-post-explotacion/privilege-escalation/windows/livingontheland\|LivingOnTheLand]] |
| windows.old | [[03-post-explotacion/privilege-escalation/windows/windows.old\|windows.old]] |

---

## CS Post-Explotación (Comandos Beacon)

| Comando | Nota |
|---------|------|
| Processes | [[03-post-explotacion/cs-post-ex/processes\|Processes]] |
| File System | [[03-post-explotacion/cs-post-ex/file-system\|File System]] |
| Registry | [[03-post-explotacion/cs-post-ex/registry\|Registry]] |
| Screenshots | [[03-post-explotacion/cs-post-ex/screenshots\|Screenshots]] |
| Keylogger | [[03-post-explotacion/cs-post-ex/keylogger\|Keylogger]] |
| Clipboard | [[03-post-explotacion/cs-post-ex/clipboard\|Clipboard]] |
| VNC | [[03-post-explotacion/cs-post-ex/vnc\|VNC]] |
| Downloading Files | [[03-post-explotacion/cs-post-ex/downloading-files\|Downloading Files]] |
| Executing Custom Tools | [[03-post-explotacion/cs-post-ex/executing-custom-tools\|Executing Custom Tools]] |
| Execution Commands | [[03-post-explotacion/cs-post-ex/execution-commands\|Execution Commands]] |
| Session Passing | [[03-post-explotacion/cs-post-ex/session-passing\|Session Passing]] |
