---
tags: [lateral-movement, impersonation, token, access-token]
status: done
platform: windows
---

# User Impersonation — Índice

> Usar credenciales o tokens de otro usuario para moverse lateralmente en el dominio.

---

## Mecanismos de Windows

### Sesiones de inicio de sesión (Logon Sessions)

Al hacer login con éxito, Windows crea una sesión temporal que almacena:
- **SID** del usuario
- **LUID** (identificador único de sesión)
- Método de autenticación
- Dominio

Esta información se envía a la LSA (Local Security Authority) para generar un token.

### Tokens de acceso (Access Tokens)

Funcionan como tarjeta de identificación interna que contiene:
- Privilegios del usuario
- Membresía de grupos
- Nivel de integridad (Low / Medium / High / System)

Cada proceso que se abre recibe una copia del token principal. Windows lo evalúa constantemente para autorizar accesos.

### Caché de credenciales (LSASS)

El proceso LSASS guarda en memoria las credenciales de sesiones activas. Cuando un proceso accede a un recurso de red, Windows cruza el token de acceso con esta caché para autenticar automáticamente (sin pedir contraseña de nuevo).

---

## Técnicas de Impersonación

| Técnica | Nota |
|---------|------|
| Token Impersonation | [[04-lateral-movement/user-impersonation/token-impersonation\|Token Impersonation]] |
| Pass the Hash | [[04-lateral-movement/user-impersonation/pass-the-hash\|Pass the Hash]] |
| Pass the Ticket | [[04-lateral-movement/user-impersonation/pass-the-ticket\|Pass The Ticket]] |
| Process Injection | [[06 EVASION & OPSEC/Process Injection/Process Injection Avanzado]] |

---

## Ver también

- [[03 POST EXPLOTACION/Credential Access/OS Credential Dumping]] — obtener las credenciales / hashes primero
- [[05 AD ATTACKS/Credential Access/Kerberos Tickets]] — extraer tickets para Pass The Ticket
