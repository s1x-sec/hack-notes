---
tags: [ad, adcs, certificates, esc]
status: pendiente
---

# ADCS — Introducción

> Active Directory Certificate Services (ADCS) emite y gestiona certificados PKI integrados con AD. El vector de ataque principal: **usar certificados para autenticación Kerberos (PKINIT)** en lugar de contraseñas.

## Conceptos clave

| Campo | Descripción |
|-------|-------------|
| **EKU** | Extended Key Usage — define para qué sirve el certificado (OIDs) |
| **SAN** | Subject Alternative Name — nombre alternativo del sujeto; si lo controla el requestor → ESC1 |
| **Manager Approval** | Si está desactivado → certificados se emiten sin revisión manual |
| **ENROLLEE_SUPPLIES_SUBJECT** | Flag que permite al requestor poner cualquier nombre → impersonación |

### OIDs relevantes

| OID | Nombre |
|-----|--------|
| `1.3.6.1.5.5.7.3.2` | Client Authentication ← necesario para autenticar |
| `1.3.6.1.5.5.7.3.1` | Server Authentication |
| `2.5.29.37.0` | Any Purpose ← abusable como cualquier EKU |
| `1.3.6.1.4.1.311.20.2.1` | Certificate Request Agent ← ESC3 |

## Enumeración

```
# Enumerar CAs
beacon> execute-assembly Certify.exe enum-cas --quiet

# Enumerar templates vulnerables
beacon> execute-assembly Certify.exe enum-templates --filter-enabled --filter-vulnerable --hide-admins --quiet
```

**Señales de alarma en un template:**
- `ENROLLEE_SUPPLIES_SUBJECT` → ESC1
- EKU `Certificate Request Agent` → ESC3
- EKU `Any Purpose` o vacío → ESC2
- `WriteDacl/WriteProperty` para Domain Users → ESC4
- CA con HTTP enrollment sin channel binding → ESC8

## Ver también

- [[05-ad-attacks/adcs/esc1---client-auth-templates|ESC1 - Client Auth Templates]]
- [[05-ad-attacks/adcs/esc3---certificate-request-agent|ESC3 - Certificate Request Agent]]
- [[05-ad-attacks/adcs/esc2---any-purpose-templates|ESC2 - Any Purpose Templates]]
- [[05-ad-attacks/adcs/esc4---template-access-control|ESC4 - Template Access Control]]
- [[05-ad-attacks/adcs/esc8---ntlm-relay-adcs|ESC8 - NTLM Relay ADCS]]
- [[05-ad-attacks/adcs/golden-certificates-(dpersist1)|Golden Certificates (DPERSIST1)]]

## Referencias

- [Certified Pre-Owned — SpecterOps](https://posts.specterops.io/certified-pre-owned-d95910965cd2)
- [HackTricks ADCS](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/ad-certificates)

