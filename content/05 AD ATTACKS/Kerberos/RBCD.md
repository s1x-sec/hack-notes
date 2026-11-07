---
tags: [ad, kerberos, rbcd, delegation]
status: pendiente
---

# Resource-Based Constrained Delegation (RBCD)

> 🔴 Por completar con experiencia de campo.

---

## Concepto

RBCD configura la delegación en el recurso destino (no en el cliente). Si podemos escribir en el atributo `msDS-AllowedToActOnBehalfOfOtherIdentity` del objeto AD, podemos abusar de S4U2Proxy para impersonar a cualquier usuario.

---

## Referencias

- [HackTricks — RBCD](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/resource-based-constrained-delegation)
- Elad Shamir — Wagging the Dog

