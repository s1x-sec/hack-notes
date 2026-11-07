---
tags: [ad, kerberos, s4u]
status: pendiente
---

# S4U2Self / S4U2Proxy

> 🔴 Por completar con experiencia de campo.

---

## Concepto

- **S4U2Self:** Permite a un servicio obtener un TGS para sí mismo en nombre de otro usuario (aunque ese usuario no se haya autenticado al servicio). Útil para elevar permisos cuando tenemos acceso a una cuenta de servicio.
- **S4U2Proxy:** Extensión de S4U2Self — permite al servicio usar el TGS de S4U2Self para solicitar un TGS adicional para otro servicio en nombre del usuario.

---

## Referencias

- [HackTricks — S4U](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/silver-ticket)

