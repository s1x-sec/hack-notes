---
tags: [lateral-movement, logon-types, double-hop, opsec]
status: done
platform: windows
---

# Security Logon Types & Double Hop

> Cómo los tipos de logon afectan qué credenciales quedan en memoria y el problema del double hop.

---

## Tipos de Logon Relevantes

| Tipo | Nombre | Creds en LSASS | Uso típico |
|------|--------|----------------|------------|
| 2 | Interactive | ✅ Sí (hash + ticket) | Consola local, RDP |
| 3 | Network | ❌ No | WinRM, PsExec, net use |
| 4 | Batch | ✅ Sí | Scheduled Tasks |
| 5 | Service | ✅ Sí | Servicios de Windows |
| 9 | NewCredentials | Solo para red | runas /netonly, make_token |
| 10 | RemoteInteractive | ✅ Sí | RDP completo |

---

## El Double Hop Problem

```
[Atacante] → Beacon en PC-A (Logon Type 3 via WinRM)
                 └── PC-A intenta LDAP al DC
                           └── ❌ ACCESS DENIED
```

**Causa:** Logon Type 3 (Network) NO almacena TGT en LSASS del destino.
Al llegar a PC-A, el beacon puede hacer cosas locales, pero **no puede autenticarse a recursos de red adicionales** porque no tiene TGT.

---

## Soluciones

### Opción 1 — Inyectar credenciales en la sesión remota

```
# Desde el beacon en PC-A
beacon> make_token DOMAIN\admin Passw0rd!      # Para autenticación NTLM en red
beacon> kerberos_ticket_use admin.kirbi        # Para Kerberos
```

### Opción 2 — Hacer la consulta desde el beacon original

Si PC-A solo era un trampolín, quizá la enumeración puede hacerse desde el beacon inicial (que sí tiene TGT):

```
# En lugar de pivotear a PC-A y enumerar desde ahí
# Hacer la enumeración LDAP directamente desde el beacon original
beacon> ldapsearch ...
```

### Opción 3 — Usar Logon Type 2 (interactivo)

- RDP da un Logon Type 10 → credenciales en LSASS del destino
- Útil si necesitamos múltiples saltos

---

## OPSEC

> ⚠️ Logon Type 2/10 **deja credenciales en LSASS** del sistema destino.
> Si hay un responder que llega después, encontrará las credenciales de nuestro usuario allí.
> En engagements con VIP accounts, preferir siempre Type 3 aunque haya double hop.

