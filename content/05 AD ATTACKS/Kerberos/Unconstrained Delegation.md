---
tags: [ad, kerberos, delegation]
status: pendiente
---

# Unconstrained Delegation

> 🔴 Por completar con experiencia de campo.

---

## Concepto

Cuando un equipo o cuenta tiene Unconstrained Delegation, cualquier usuario que se autentique a un servicio en ese host deposita su TGT en la memoria de LSASS del servidor delegado. El atacante con acceso a ese host puede extraer esos TGTs y usarlos para impersonar a los usuarios.

---

## Referencias

- [HackTricks — Unconstrained Delegation](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/unconstrained-delegation)

