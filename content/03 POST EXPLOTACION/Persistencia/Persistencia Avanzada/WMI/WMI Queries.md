---
title: WMI — Queries
tags: [wmi, persistence, cobalt-strike, wql]
---

# WMI Queries

## Instance Queries

Consultas sobre el estado actual del sistema.

```powershell
# Procesos con nombre específico
Get-WmiObject -Query "SELECT * FROM Win32_Process WHERE Name = 'notepad.exe'"

# Servicios activos
Get-WmiObject -Query "SELECT * FROM Win32_Service WHERE State = 'Running'"

# Información del sistema
Get-WmiObject -Query "SELECT * FROM Win32_ComputerSystem"
```

## Event Queries

WQL permite suscribirse a eventos. El parámetro `WITHIN` define el intervalo de polling (en segundos).

```powershell
# Detectar cuando un proceso arranca
$query = "SELECT * FROM __InstanceCreationEvent WITHIN 5 WHERE TargetInstance ISA 'Win32_Process' AND TargetInstance.Name = 'notepad.exe'"

# Detectar conexiones de red
$query = "SELECT * FROM __InstanceCreationEvent WITHIN 5 WHERE TargetInstance ISA 'Win32_NetworkAdapterConfiguration'"
```

## Uso con PowerShell

```powershell
# Query puntual
$results = Get-WmiObject -Query "SELECT * FROM Win32_Process WHERE Name = 'notepad.exe'"

# Evento local (no persistente)
Register-WmiEvent -Query $query -SourceIdentifier "ProcessWatch"
Wait-Event -SourceIdentifier "ProcessWatch"
```

## Ver también
- [[03-post-explotacion/persistencia/persistencia-avanzada/wmi/wmi-eventing|WMI Eventing]]
- [[03-post-explotacion/persistencia/persistencia-avanzada/wmi/wmi-remote-triggers|WMI Remote Triggers]]
