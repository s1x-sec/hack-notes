---
tags: [cloud, azure, avd, recon, enumeration]
status: wip
---

# AVD — Enumeración

> Reconocimiento de infraestructura Azure Virtual Desktop: host pools, session hosts, application groups, workspaces y configuración de red.

---

## Pre-requisitos

- Credenciales válidas de un usuario con acceso al tenant (viewer mínimo)
- `az cli` o módulo `Az` PowerShell autenticado
- Para enumeración profunda: rol `Reader` sobre la suscripción o `Desktop Virtualization Reader`

---

## Enumeración del tenant

```powershell
# Login interactivo
az login

# Listar suscripciones accesibles
az account list --output table

# Cambiar a la suscripción target
az account set --subscription <SUB_ID>
```

---

## Host Pools

```powershell
# Listar host pools
az desktopvirtualization hostpool list --output table

# Detalle de un host pool
az desktopvirtualization hostpool show \
  --name <POOL_NAME> \
  --resource-group <RG>

# Puntos clave a buscar:
# - loadBalancerType: BreadthFirst vs DepthFirst (indica uso)
# - maxSessionLimit: sesiones por host
# - registrationInfo: tokens de registro (si accesible → añadir VMs propias)
# - customRdpProperty: configuraciones RDP (clipboard, drives, etc.)
```

---

## Session Hosts

```powershell
# Listar session hosts de un pool
az desktopvirtualization hostpool list-session-hosts \
  --name <POOL_NAME> \
  --resource-group <RG> \
  --output table

# Info relevante por host:
# - allowNewSessions: ¿acepta conexiones?
# - assignedUser: si es personal desktop → usuario asignado
# - sessions: sesiones activas actuales
# - resourceId: ID de la VM subyacente
```

```powershell
# Con el resourceId, obtener info de la VM
az vm show --ids <RESOURCE_ID> --output json

# Buscar:
# - networkProfile → obtener VNET y subnet
# - storageProfile → OS, data disks
# - identity → Managed Identity (System/User assigned)
```

---

## Application Groups & Workspaces

```powershell
# Application groups
az desktopvirtualization applicationgroup list \
  --resource-group <RG> --output table

# Tipo: "Desktop" (escritorio completo) vs "RemoteApp" (apps publicadas)
# Si es RemoteApp → listar aplicaciones publicadas
az desktopvirtualization application list \
  --application-group-name <AG_NAME> \
  --resource-group <RG>

# Workspaces
az desktopvirtualization workspace list \
  --resource-group <RG> --output table
```

---

## Usuarios y Asignaciones

```powershell
# Role assignments en el host pool
az role assignment list \
  --scope "/subscriptions/<SUB>/resourceGroups/<RG>/providers/Microsoft.DesktopVirtualization/hostpools/<POOL>" \
  --output table

# Buscar:
# - "Desktop Virtualization User" → usuarios que pueden conectarse
# - "Desktop Virtualization Contributor" → administradores AVD
# - "Desktop Virtualization Session Host Operator" → puede forzar logoff, drain mode

# Listar sesiones activas de usuarios
az desktopvirtualization user-session list \
  --host-pool-name <POOL> \
  --resource-group <RG> --output table
```

---

## Red y Conectividad

```powershell
# VNET de los session hosts
az network vnet list --resource-group <RG> --output table

# NSG asociados
az network nsg list --resource-group <RG> --output table
az network nsg rule list --nsg-name <NSG_NAME> --resource-group <RG> --output table

# ¿RDP Shortpath habilitado? Buscar en customRdpProperty del host pool:
# "use managed disks:i:1;targetisaadjoined:i:1;enablerdsaadauth:i:1"
# Si hay reglas UDP 3390 en NSG → shortpath activo

# Private Endpoints
az network private-endpoint list --resource-group <RG> --output table
```

---

## FSLogix y Storage

```powershell
# Storage accounts en el RG
az storage account list --resource-group <RG> --output table

# File shares (típicamente "fslogix" o "profiles")
az storage share list --account-name <STORAGE> --output table

# Si hay acceso → los perfiles son VHDs con datos de usuario
# Ruta típica: \\storageaccount.file.core.windows.net\profiles\SID_username\Profile_username.vhdx
```

---

## Enumeración con ROADtools (Entra ID)

```bash
# Autenticar
roadrecon auth -u user@domain.com -p 'password'
# O con token
roadrecon auth --access-token <TOKEN>

# Dump completo del tenant
roadrecon gather

# GUI web para explorar relaciones
roadrecon gui
# → Buscar aplicaciones registradas de AVD, service principals, conditional access policies
```

---

## Enumeración con BloodHound CE

```bash
# Collector Azure (AzureHound)
azurehound -j <JWT_TOKEN> list --tenant <TENANT_ID> -o azurehound-output.json

# Importar en BloodHound CE
# → Buscar paths desde usuarios AVD hacia recursos privilegiados
# → Nodos de tipo AZVMContributor, AZKeyVaultReader sobre session hosts
```

---

## Señales de ataque

| Hallazgo | Implicación |
|----------|-------------|
| `customRdpProperty` sin `drivestoredirect:s:` | Clipboard/drives no restringidos → exfiltración fácil |
| `registrationInfo.token` accesible | Registrar VMs maliciosas en el host pool |
| Session hosts con System Managed Identity | IMDS → token de Azure para pivotar |
| FSLogix en Storage Account sin Private Endpoint | Posible acceso desde internet |
| NSG permisivo (3389 abierto a internet) | Session hosts accesibles directamente vía RDP |
| Multi-session hosts (Windows 10/11 Enterprise Multi-session) | Múltiples usuarios en la misma VM → mayor superficie |

---

## Ver también

- [[09-cloud/azure/azure-virtual-desktop|Azure Virtual Desktop]]
- [[09-cloud/azure/avd---acceso-inicial|AVD - Acceso Inicial]]
- [[09-cloud/azure/avd---session-host-attacks|AVD - Session Host Attacks]]

---

## Referencias

- [Microsoft — AVD Architecture](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-architecture-resilience)
- [AzureHound — BloodHound](https://github.com/BloodHoundAD/AzureHound)
- [ROADtools — dirkjanm](https://github.com/dirkjanm/ROADtools)
