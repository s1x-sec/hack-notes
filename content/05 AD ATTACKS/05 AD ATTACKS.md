---
tags: [active-directory]
status: wip
---

# ACTIVE DIRECTORY ATTACKS

---

## Enumeración & Discovery

| Técnica | Nota |
|---------|------|
| Enumeración AD (nxc, PowerView) | [[Discovery/Enumeración AD]] |
| LDAP Discovery | [[Discovery/LDAP Discovery]] |
| LDAP Avanzado (Cobalt) | [[Discovery/LDAP Avanzado (Cobalt)]] |
| BOFHound | [[Discovery/BOFHound]] |
| Default Domain Policy | [[Discovery/Default Domain Policy]] |
| Force Password Change | [[Discovery/Force Password Change]] |
| Generic Write sobre Usuario | [[Discovery/Generic Write Sobre Usuario]] |
| GenericAll sobre DC | [[Discovery/GenericAll DC]] |
| ReadGMSAPassword | [[Discovery/ReadGMSAPassword]] |
| RBCD (Discovery) | [[Discovery/Resourced Based Constrained Delegation]] |

---

## Ataques Kerberos

| Técnica | Nota |
|---------|------|
| Kerberos (teoría) | [[Kerberos/Kerberos]] |
| Kerberoasting | [[Kerberos/Kerberoasting]] |
| AS-REP Roasting | [[Kerberos/AS-REP Roasting]] |
| Unconstrained Delegation | [[Kerberos/Unconstrained Delegation]] |
| Constrained Delegation | [[Kerberos/Constrained Delegation]] |
| RBCD | [[Kerberos/RBCD]] |
| S4U2Self / S4U2Proxy | [[Kerberos/S4U2Self]] |
| Lateral Movement Services (CS) | [[Kerberos/Lateral Movement Services (CS)]] |
| Service Name Substitution (CS) | [[Kerberos/Service Name Substitution (CS)]] |

---

## Credential Access AD

| Técnica | Nota |
|---------|------|
| Kerberos Tickets (Rubeus, BOFs) | [[Credential Access/Kerberos Tickets]] |

---

## Ataques Varios

| Técnica | Nota |
|---------|------|
| Envenenamiento Responder | [[Ataques/Envenenamiento Responder]] |
| RunAS | [[Ataques/RunAS]] |
| Silver Ticket | [[Ataques/Silver Ticket]] |

---

## ADCS & Trusts

| Área | Nota |
|------|------|
| ADCS — ESC1-8 | [[ADCS/ADCS]] |
| Forest & Domain Trusts | [[Trusts/Trusts]] |

---

## Flujo de Ataque AD

```
1. RECONOCIMIENTO OPSEC
   └── [[Discovery/Enumeración AD]] → nxc, PowerView, ldapsearch
   └── [[Discovery/BOFHound]] — sin SharpHound

2. CREDENTIAL ACCESS
   ├── Cuenta servicio con SPN  → [[Kerberos/Kerberoasting]]
   ├── Pre-auth deshabilitado   → [[Kerberos/AS-REP Roasting]]
   └── Tickets en memoria       → [[Credential Access/Kerberos Tickets]]

3. ESCALADA EN DOMINIO
   ├── Delegaciones             → Unconstrained / Constrained / RBCD
   └── Certificados             → [[ADCS/ADCS]]

4. MOVIMIENTO ENTRE DOMINIOS
   └── [[Trusts/Trusts]]
```
