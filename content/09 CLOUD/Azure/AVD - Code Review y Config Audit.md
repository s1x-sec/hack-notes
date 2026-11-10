---
tags: [cloud, azure, avd, code-review, config-audit, iac, whitebox]
status: wip
---

# AVD — Code Review y Config Audit

> Qué revisar cuando se tiene acceso al código fuente (IaC, scripts, pipelines) y credenciales del entorno AVD. Enfoque whitebox / grey-box.

---

## IaC — Infraestructura como Código

### Terraform / Bicep / ARM Templates

```bash
# Buscar ficheros de definición
find . -name "*.tf" -o -name "*.bicep" -o -name "*.json" | head -50

# Qué buscar en la definición del host pool:
```

| Parámetro | Qué revisar | Riesgo |
|-----------|-------------|--------|
| `customRdpProperty` | ¿Clipboard habilitado? ¿Drive redirection? ¿USB? | Exfiltración de datos |
| `maxSessionLimit` | Límite muy alto en multi-session → más usuarios expuestos | Mayor blast radius |
| `loadBalancerType` | `DepthFirst` llena hosts → más creds en un solo host | Credential harvesting |
| `registrationInfo` | ¿Token hardcodeado o rotado? ¿Expiry largo? | Host pool hijacking |
| `validationEnvironment` | Si es `true` → entorno de validación, posible stepping stone | Lateral movement |
| `startVMOnConnect` | Si `true` → VMs se encienden al conectar usuario | Persistencia más fácil |

```hcl
# Ejemplo Terraform — señales de alarma
resource "azurerm_virtual_desktop_host_pool" "example" {
  custom_rdp_properties = "drivestoredirect:s:*;camerastoredirect:s:*;audiocapturemode:i:1;redirectclipboard:i:1"
  # ⚠️ Todo redirigido: drives, cámara, audio, clipboard
  
  maximum_sessions_allowed = 50
  # ⚠️ 50 sesiones por host → LSASS dump masivo
}
```

### Network — NSGs y Firewall Rules

```hcl
# Buscar reglas permisivas
# En Terraform:
grep -r "0.0.0.0/0" *.tf
grep -r "source_address_prefix.*\*" *.tf
grep -r "3389" *.tf

# En ARM/Bicep:
grep -r "0.0.0.0/0" *.json *.bicep
grep -r "3389" *.json *.bicep
```

| Hallazgo | Riesgo |
|----------|--------|
| RDP (3389) abierto a `0.0.0.0/0` | Acceso directo desde internet |
| Sin NSG entre subnets | Lateral movement libre entre session hosts y otros recursos |
| Outbound `*` permitido | Exfiltración sin restricciones, C2 directo |
| Sin Private Endpoints para Storage | FSLogix profiles accesibles fuera de la VNET |

### Managed Identity

```bash
# Buscar asignación de Managed Identity en las VMs
grep -r "identity" *.tf *.bicep *.json | grep -i "systemassigned\|userassigned"

# Luego verificar qué role assignments tiene:
# En Terraform:
grep -r "azurerm_role_assignment" *.tf
# Buscar scopes demasiado amplios (suscripción completa, Contributor/Owner)
```

---

## Conditional Access Policies

```powershell
# Con credenciales de Global Reader o Security Reader:
# Exportar todas las políticas CA

# Via Graph API
az rest --method GET \
  --url "https://graph.microsoft.com/v1.0/identity/conditionalAccessPolicies" \
  --output json > ca_policies.json

# O con AADInternals
Import-Module AADInternals
Get-AADIntConditionalAccessPolicies | ConvertTo-Json -Depth 10 > ca_policies.json
```

| Qué buscar | Riesgo |
|------------|--------|
| Políticas en modo `reportOnly` (no enforce) | Protección aparente pero sin bloqueo real |
| Exclusiones de usuarios/grupos | Cuentas excluidas = bypass directo |
| Sin MFA para la app `Azure Virtual Desktop` (ID: `9cdead84-a844-4324-93f2-b2e6bb768d07`) | Acceso solo con contraseña |
| Sin device compliance | Dispositivos no gestionados pueden conectar |
| Trusted locations muy amplias | Bypass desde rangos IP corporativos amplios |
| Sin session controls (sign-in frequency) | Tokens de larga duración |
| App `Microsoft Remote Desktop` (ID: `a4a365df-50f1-4397-bc59-1a1564b8bb9c`) no cubierta | El cliente nativo no está protegido |

```python
# Script rápido para auditar exclusiones
import json

with open("ca_policies.json") as f:
    data = json.load(f)

for policy in data.get("value", []):
    name = policy["displayName"]
    state = policy["state"]
    excluded = policy["conditions"]["users"].get("excludeUsers", [])
    excluded_groups = policy["conditions"]["users"].get("excludeGroups", [])
    
    if excluded or excluded_groups:
        print(f"[!] {name} ({state}): {len(excluded)} users + {len(excluded_groups)} groups excluded")
    
    if state == "reportOnly":
        print(f"[!] {name}: reportOnly — NOT enforcing")
```

---

## Intune / Endpoint Manager Policies

```powershell
# Si los session hosts están managed por Intune:
# Revisar configuración de seguridad aplicada

# Con Graph API (requiere DeviceManagementConfiguration.Read.All)
az rest --method GET \
  --url "https://graph.microsoft.com/beta/deviceManagement/deviceConfigurations" \
  --output json

# O con IntuneManagement PowerShell
# https://github.com/nicolgit/intune-management-powershell
```

| Política | Qué verificar |
|----------|--------------|
| **AppLocker / WDAC** | ¿Está configurado? ¿En Enforce o Audit? ¿Reglas default sin hardening? |
| **Windows Defender** | ¿Real-time protection? ¿Tamper protection? ¿Exclusiones sospechosas? |
| **ASR Rules** | ¿Attack Surface Reduction habilitado? ¿Qué reglas están activas? |
| **BitLocker** | ¿Discos cifrados? ¿Recovery key en Entra ID? |
| **Firewall** | ¿Windows Firewall habilitado? ¿Reglas permisivas? |
| **PowerShell** | ¿Constrained Language Mode? ¿Script Block Logging? ¿Transcription? |
| **Credential Guard** | ¿Habilitado? Si no → LSASS dump trivial |
| **LAPS** | ¿Local admin password rotation? ¿O misma pass en todos los hosts? |

---

## FSLogix Configuration

```powershell
# Configuración FSLogix en registry de los session hosts
# O en GPO/Intune profiles

# Claves a revisar:
# HKLM\SOFTWARE\FSLogix\Profiles
```

| Clave | Valor seguro | Riesgo si mal configurado |
|-------|-------------|--------------------------|
| `VHDLocations` | Share con Private Endpoint | Si es público → acceso externo a perfiles |
| `DeleteLocalProfileWhenVHDShouldApply` | 1 | Si 0 → datos residuales en el host |
| `PreventLoginWithFailure` | 1 | Si 0 → login sin perfil = datos en disco local |
| `PreventLoginWithTempProfile` | 1 | Si 0 → perfiles temporales con datos |
| `SizeInMBs` | Adecuado | Muy grande → más datos exfiltrables |
| `IsDynamic` | 1 | Si 0 → VHD tamaño fijo, más espacio consumido |
| `LockedRetryCount` / `LockedRetryInterval` | Bajo | Si alto → posible montar perfil ajeno |
| `AccessNetworkAsComputerObject` | 1 | Si 0 → usuario accede al share directamente |
| `VolumeType` | VHDX | VHD tiene límite 2TB y peor rendimiento |

```powershell
# Permisos en el share de FSLogix — CRITICO
# El usuario solo debería poder crear carpeta, no leer las de otros

# Verificar ACLs en el share
icacls "\\storageaccount.file.core.windows.net\profiles"

# Configuración correcta:
# Creator/Owner: Full Control (Subfolders and Files)
# Domain Users: Modify (This Folder Only) — para crear su carpeta
# Domain Users: NO read en subcarpetas de otros

# Si Domain Users tiene Read/List en el root → puede ver perfiles de otros
```

---

## Storage Account Security

```powershell
# Con acceso a la suscripción:
az storage account show --name <STORAGE> --resource-group <RG>
```

| Configuración | Valor seguro | Riesgo |
|--------------|-------------|--------|
| `networkRuleSet.defaultAction` | `Deny` | Si `Allow` → acceso público |
| `networkRuleSet.virtualNetworkRules` | Solo subnet de session hosts | Si vacío con Allow → cualquiera accede |
| `encryption.services.file.enabled` | `true` | Si false → datos sin cifrar |
| `minimumTlsVersion` | `TLS1_2` | Versiones antiguas → downgrade attacks |
| `allowSharedKeyAccess` | `false` (idealmente) | Si true → con la storage key se accede a todo |
| `privateEndpointConnections` | Configurado | Sin Private Endpoint → tráfico por internet |
| `allowBlobPublicAccess` | `false` | Si true → blobs potencialmente públicos |

```bash
# Intentar listar con la storage key (si se encuentra)
az storage share list --account-name <STORAGE> --account-key <KEY>
az storage file list --share-name profiles --account-name <STORAGE> --account-key <KEY>

# Buscar storage keys en el código
grep -ri "AccountKey=" . --include="*.tf" --include="*.json" --include="*.yaml" --include="*.ps1" --include="*.py"
grep -ri "DefaultEndpointsProtocol=https;AccountName=" .
```

---

## Secretos y Credenciales en el Código

```bash
# Buscar secrets hardcodeados en IaC, scripts, pipelines

# Patterns genéricos
grep -rni "password\|secret\|key\|token\|credential\|connectionstring" \
  --include="*.tf" --include="*.json" --include="*.yaml" --include="*.yml" \
  --include="*.ps1" --include="*.py" --include="*.sh" --include="*.bicep" .

# Azure-specific
grep -rni "AccountKey=\|SharedAccessSignature=\|sig=" .
grep -rni "client_secret\|clientSecret\|appSecret" .
grep -rni "-----BEGIN.*PRIVATE KEY-----" .

# En pipelines CI/CD (GitHub Actions, Azure DevOps)
grep -rni "secret\|password\|key" --include="*.yml" .github/ azure-pipelines/ .azuredevops/

# Herramientas automatizadas
# trufflehog — busca secrets en repos git
trufflehog filesystem --directory=. --only-verified

# gitleaks
gitleaks detect --source=. -v
```

---

## Azure RBAC — Role Assignments

```powershell
# Exportar todos los role assignments de la suscripción
az role assignment list --all --output json > rbac.json

# Buscar over-privileged assignments
# ⚠️ Contributor/Owner a nivel de suscripción o RG
az role assignment list --all --query "[?roleDefinitionName=='Contributor' || roleDefinitionName=='Owner']" --output table

# Custom roles — pueden tener permisos excesivos
az role definition list --custom-role-only true --output json

# Service Principals con permisos altos
az ad sp list --all --query "[?servicePrincipalType=='Application']" --output table
# → Verificar role assignments de cada SP
```

| Hallazgo | Riesgo |
|----------|--------|
| `Contributor` en la suscripción para el SP de deploy | Puede ejecutar Run Command en cualquier VM |
| `Owner` para usuarios no-admin | Escalada completa |
| Custom role con `Microsoft.Compute/virtualMachines/*` | Control total de VMs (Run Command, extensions) |
| `Desktop Virtualization Contributor` para muchos usuarios | Pueden modificar host pools, obtener registration tokens |
| `User Access Administrator` en algún scope | Puede asignarse cualquier rol a sí mismo |

---

## Logging y Monitoring

```powershell
# Verificar si hay monitoreo configurado — si no hay, el pentest es más silencioso

# Diagnostic settings
az monitor diagnostic-settings list --resource <HOST_POOL_RESOURCE_ID>

# Log Analytics workspace
az monitor log-analytics workspace list --resource-group <RG>

# ¿Microsoft Sentinel habilitado?
az sentinel alert-rule list --workspace-name <WORKSPACE> --resource-group <RG>
```

| Verificación | Implicación |
|-------------|-------------|
| Sin Diagnostic Settings en host pool | No se registran eventos de conexión AVD |
| Sin Log Analytics en session hosts | Sin Sysmon, sin Security Events centralizados |
| Sin Sentinel / sin alert rules | Sin detección automatizada |
| NLA (Network Level Authentication) deshabilitado | Posible pre-auth information disclosure |
| Sin Azure AD Sign-in Logs exportados | Spraying y token theft no monitorizados |

---

## CI/CD Pipeline Review

```bash
# Si hay pipelines de deploy (GitHub Actions, Azure DevOps):

# Verificar:
# 1. ¿Service connection con permisos excesivos?
# 2. ¿Secrets inyectados como variables de entorno? (pueden loguearse)
# 3. ¿Self-hosted agents? → comprometer el runner = acceso al SP
# 4. ¿Pipeline puede deployar a producción sin approval gates?

# En GitHub Actions:
cat .github/workflows/*.yml
# Buscar: secrets.*, env vars, actions de terceros no pinned a SHA

# En Azure DevOps:
# Verificar service connections, variable groups, agent pools
```

---

## Checklist rápido

```
[ ] IaC: ¿RDP properties restrictivos? (clipboard, drives, USB off)
[ ] IaC: ¿NSGs restrictivos entre subnets?
[ ] IaC: ¿Private Endpoints para Storage?
[ ] IaC: ¿Managed Identity con least privilege?
[ ] CA: ¿MFA para app AVD y Remote Desktop?
[ ] CA: ¿Sin exclusiones injustificadas?
[ ] CA: ¿Policies en Enforce, no reportOnly?
[ ] Intune: ¿Credential Guard habilitado?
[ ] Intune: ¿AppLocker/WDAC en Enforce?
[ ] Intune: ¿PowerShell CLM + logging?
[ ] Intune: ¿ASR rules activas?
[ ] FSLogix: ¿ACLs correctas en el share?
[ ] FSLogix: ¿PreventLoginWithFailure + TempProfile?
[ ] Storage: ¿defaultAction: Deny?
[ ] Storage: ¿allowSharedKeyAccess: false?
[ ] RBAC: ¿Sin Contributor/Owner excesivos?
[ ] Código: ¿Sin secrets hardcodeados?
[ ] Monitoring: ¿Diagnostic settings + Sentinel?
[ ] Pipeline: ¿Service connection least privilege?
```

---

## Ver también

- [[09-cloud/azure/azure-virtual-desktop|Azure Virtual Desktop]]
- [[09-cloud/azure/avd---enumeración|AVD - Enumeración]]
- [[09-cloud/azure/avd---acceso-inicial|AVD - Acceso Inicial]]
- [[09-cloud/azure/avd---session-host-attacks|AVD - Session Host Attacks]]

---

## Referencias

- [CIS Benchmark — Azure Virtual Desktop](https://www.cisecurity.org/benchmark/azure)
- [Microsoft — AVD Security Best Practices](https://learn.microsoft.com/en-us/azure/virtual-desktop/security-guide)
- [FSLogix Security Reference](https://learn.microsoft.com/en-us/fslogix/reference-configuration-settings)
- [trufflehog](https://github.com/trufflesecurity/trufflehog)
- [gitleaks](https://github.com/gitleaks/gitleaks)
