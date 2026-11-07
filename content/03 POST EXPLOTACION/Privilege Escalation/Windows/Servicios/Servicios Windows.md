---
tags: [privesc, windows, services]
---

# Servicios Débiles — Windows

| Tipo | Nota |
|------|------|
| Weak Service Permissions | [[03-post-explotacion/privilege-escalation/windows/servicios/weak-windows-services\|Weak Windows Services]] |

## Revisión Manual de Servicios

```powershell
wmic service get Name,DisplayName,State,StartMode,StartName,PathName

# Revisar DACL de un servicio
sc sdshow <service_name>

# Con accesschk
accesschk.exe /accepteula -uwcqv "Authenticated Users" *
accesschk.exe /accepteula -uwcqv <service_name>
```

## Herramientas

```
PowerUp.ps1 → Invoke-AllChecks
WinPEAS → sección de servicios
```
