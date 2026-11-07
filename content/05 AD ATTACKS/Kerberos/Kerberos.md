---
title: Kerberos — Teoría y Flujo
tags: [kerberos, active-directory, authentication]
---

# Kerberos

Reemplazó NTLM como protocolo de autenticación de dominio desde Windows Server 2000. Funciona con **tickets** — los principals (usuarios y equipos) se autentican contra un servidor central de confianza (KDC) y reciben tickets para acceder a servicios sin reenviar la contraseña.

> Kerberos **asume red sin cifrado** (los paquetes pueden leerse/modificarse/replicarse) — por eso usa criptografía de clave compartida.

---

## Componentes clave

| Componente | Descripción |
|-----------|-------------|
| **KDC** (Key Distribution Center) | Fuente de confianza. En Windows = Domain Controller. Contiene la BBDD de principals + sus hashes |
| **AS** (Authentication Server) | Sub-componente del KDC. Valida identidad y emite TGTs |
| **TGS** (Ticket Granting Server) | Sub-componente del KDC. Emite Service Tickets |
| **TGT** (Ticket Granting Ticket) | Ticket de identidad verificada. Se usa en lugar de la contraseña para pedir STs |
| **ST / TGS Ticket** | Service Ticket. Permite acceder a un servicio concreto |
| **SPN** (Service Principal Name) | Identifica cada instancia de servicio. Formato: `clase/instancia:puerto` (ej: `cifs/srv01.lab.local`) |
| **PAC** (Privileged Attribute Certificate) | Estructura dentro del ticket con datos del usuario: RID, grupos, UAC flags. El servicio lo usa para decidir acceso sin consultar AD |

---

## Flujo Kerberos estándar

```
1. Cliente → KDC: AS-REQ (solicita TGT)
2. KDC → Cliente: AS-REP (TGT cifrado con clave del krbtgt)
3. Cliente → KDC: TGS-REQ (TGT + nombre de servicio)
4. KDC → Cliente: TGS-REP (TGS cifrado con hash del servicio)
5. Cliente → Servicio: AP-REQ (TGS)
6. Servicio valida el TGS y concede acceso
```

---

## Claves de cifrado — quién cifra qué

| Objeto | Cifrado con |
|--------|-------------|
| TGT (EncTicketPart) | Hash de `krbtgt` |
| Logon session key en AS-REP | Hash del **usuario** |
| Service Ticket (EncTicketPart) | Hash de la **cuenta de servicio** |
| Service session key en TGS-REP | Logon session key del usuario |
| Authenticator en TGS-REQ | Logon session key del usuario |

> **Red Team:** El cliente **nunca puede descifrar** el TGT (no sabe el hash de krbtgt) ni el ST (no sabe el hash del servicio). Solo descifra las session keys.

---

## Pre-autenticación

Por defecto los usuarios deben hacer **pre-auth**: cifrar el timestamp actual con el hash de su contraseña antes de recibir el TGT.

- Si se **deshabilita** → el KDC devuelve el AS-REP sin verificar identidad → **AS-REP Roasting** (`[[AS-REP Roasting]]`)
- El `EncASRepPart` (logon session key cifrada con hash del usuario) es lo que se crackea

---

## Autorización vs Autenticación

| Rol | Quien lo hace |
|-----|--------------|
| Autenticación del principal | KDC (verifica que eres quien dices) |
| Autorización al servicio | **El propio servicio** (comprueba DACL, roles, etc.) |

El KDC **no valida permisos**. Solo emite tickets técnicamente válidos.

---

## PAC Validation

- **Sin validación (default):** el servicio confía en el PAC del ticket para saber grupos/RID → explotable con tickets forjados
- **Con validación:** el servicio hace RPC al KDC para verificar la firma del PAC (firmada con hash de krbtgt) → si el ticket es forjado, la firma no cuadra → acceso denegado

---

## Red Team takeaways

| Concepto | Ataque |
|---------|--------|
| Pre-auth deshabilitada | [[05-ad-attacks/kerberos/as-rep-roasting\|AS-REP Roasting]] — crackear EncASRepPart offline |
| SPN asociado a cuenta de usuario | [[05-ad-attacks/kerberos/kerberoasting\|Kerberoasting]] — pedir ST y crackear EncTicketPart offline |
| Conocemos hash de krbtgt | [[05 AD ATTACKS/Ataques/Silver Ticket]] — forjar ST para cualquier servicio |
| Delegación sin restricciones | [[05-ad-attacks/kerberos/unconstrained-delegation\|Unconstrained Delegation]] — robar TGTs de otros |
| Delegación restringida | [[05-ad-attacks/kerberos/constrained-delegation\|Constrained Delegation]] / [[05-ad-attacks/kerberos/rbcd\|RBCD]] — impersonar usuarios a servicios específicos |

---

## Ver también

- [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]]
- [[05-ad-attacks/kerberos/as-rep-roasting|AS-REP Roasting]]
- [[05-ad-attacks/kerberos/unconstrained-delegation|Unconstrained Delegation]]
- [[05-ad-attacks/kerberos/constrained-delegation|Constrained Delegation]]
- [[05-ad-attacks/kerberos/rbcd|RBCD]]
- [[05-ad-attacks/kerberos/s4u2self|S4U2Self]]
