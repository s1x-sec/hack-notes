---
tags: [ad, adcs, esc2, privilege-escalation, certificates]
status: completo
---

# ESC2 — Misconfigured Any Purpose Templates

> Template con EKU `Any Purpose` (o sin EKUs). Un certificado así puede usarse como **cualquier EKU sin restricción**.

## Condiciones necesarias

- EKU `Any Purpose` (`2.5.29.37.0`) **o** EKUs vacíos (tratado como Subordinate CA)
- `Manager Approval Required: False`
- Domain Users tienen `Enrollment Rights`

## Detección

```
beacon> execute-assembly Certify.exe enum-templates --filter-enabled --filter-vulnerable --hide-admins --quiet

Template Name          : ESC2
Extended Key Usage     : Any Purpose
Manager Approval       : False
Enrollment Rights      : CONTOSO\Domain Users
```

## Ataque

Dependiendo de los flags del template:

| Condición | Técnica a usar |
|-----------|---------------|
| Sin `ENROLLEE_SUPPLIES_SUBJECT` | Usar como [[05-ad-attacks/adcs/esc3---certificate-request-agent\|ESC3 - Certificate Request Agent]] (el cert actúa como Request Agent) |
| Con `ENROLLEE_SUPPLIES_SUBJECT` | Usar como [[05-ad-attacks/adcs/esc1---client-auth-templates\|ESC1 - Client Auth Templates]] (poner cualquier SAN) |

## Ver también

- [[05-ad-attacks/adcs/esc1---client-auth-templates|ESC1 - Client Auth Templates]]
- [[05-ad-attacks/adcs/esc3---certificate-request-agent|ESC3 - Certificate Request Agent]]
- [[05-ad-attacks/adcs|ADCS]]
