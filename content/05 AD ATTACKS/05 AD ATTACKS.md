---
tags: [active-directory]
status: wip
---

# ACTIVE DIRECTORY ATTACKS

---

## Enumeración & Discovery

| Técnica | Nota |
|---------|------|
| Enumeración AD (nxc, PowerView) | [[05-ad-attacks/discovery/enumeración-ad|Enumeración AD]] |
| LDAP Discovery | [[05-ad-attacks/discovery/ldap-discovery|LDAP Discovery]] |
| LDAP Avanzado (Cobalt) | [[05-ad-attacks/discovery/ldap-avanzado-(cobalt)|LDAP Avanzado (Cobalt)]] |
| BOFHound | [[05-ad-attacks/discovery/bofhound|BOFHound]] |
| Default Domain Policy | [[05-ad-attacks/discovery/default-domain-policy|Default Domain Policy]] |
| Force Password Change | [[05-ad-attacks/discovery/force-password-change|Force Password Change]] |
| Generic Write sobre Usuario | [[05-ad-attacks/discovery/generic-write-sobre-usuario|Generic Write Sobre Usuario]] |
| GenericAll sobre DC | [[05-ad-attacks/discovery/genericall-dc|GenericAll DC]] |
| ReadGMSAPassword | [[05-ad-attacks/discovery/readgmsapassword|ReadGMSAPassword]] |
| RBCD (Discovery) | [[05-ad-attacks/discovery/resourced-based-constrained-delegation|Resourced Based Constrained Delegation]] |

---

## Ataques Kerberos

| Técnica | Nota |
|---------|------|
| Kerberos (teoría) | [[05-ad-attacks/kerberos|Kerberos]] |
| Kerberoasting | [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]] |
| AS-REP Roasting | [[05-ad-attacks/kerberos/as-rep-roasting|AS-REP Roasting]] |
| Unconstrained Delegation | [[05-ad-attacks/kerberos/unconstrained-delegation|Unconstrained Delegation]] |
| Constrained Delegation | [[05-ad-attacks/kerberos/constrained-delegation|Constrained Delegation]] |
| RBCD | [[05-ad-attacks/kerberos/rbcd|RBCD]] |
| S4U2Self / S4U2Proxy | [[05-ad-attacks/kerberos/s4u2self|S4U2Self]] |
| Lateral Movement Services (CS) | [[05-ad-attacks/kerberos/lateral-movement-services-(cs)|Lateral Movement Services (CS)]] |
| Service Name Substitution (CS) | [[05-ad-attacks/kerberos/service-name-substitution-(cs)|Service Name Substitution (CS)]] |

---

## Credential Access AD

| Técnica | Nota |
|---------|------|
| Kerberos Tickets (Rubeus, BOFs) | [[05-ad-attacks/credential-access/kerberos-tickets|Kerberos Tickets]] |

---

## Ataques Varios

| Técnica | Nota |
|---------|------|
| Envenenamiento Responder | [[05-ad-attacks/ataques/envenenamiento-responder|Envenenamiento Responder]] |
| RunAS | [[05-ad-attacks/ataques/runas|RunAS]] |
| Silver Ticket | [[05-ad-attacks/ataques/silver-ticket|Silver Ticket]] |

---

## ADCS & Trusts

| Área | Nota |
|------|------|
| ADCS — ESC1-8 | [[05-ad-attacks/adcs|ADCS]] |
| Forest & Domain Trusts | [[05-ad-attacks/trusts|Trusts]] |

---

## Flujo de Ataque AD

```
1. RECONOCIMIENTO OPSEC
   └── [[05-ad-attacks/discovery/enumeración-ad|Enumeración AD]] → nxc, PowerView, ldapsearch
   └── [[05-ad-attacks/discovery/bofhound|BOFHound]] — sin SharpHound

2. CREDENTIAL ACCESS
   ├── Cuenta servicio con SPN  → [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]]
   ├── Pre-auth deshabilitado   → [[05-ad-attacks/kerberos/as-rep-roasting|AS-REP Roasting]]
   └── Tickets en memoria       → [[05-ad-attacks/credential-access/kerberos-tickets|Kerberos Tickets]]

3. ESCALADA EN DOMINIO
   ├── Delegaciones             → Unconstrained / Constrained / RBCD
   └── Certificados             → [[05-ad-attacks/adcs|ADCS]]

4. MOVIMIENTO ENTRE DOMINIOS
   └── [[05-ad-attacks/trusts|Trusts]]
```
