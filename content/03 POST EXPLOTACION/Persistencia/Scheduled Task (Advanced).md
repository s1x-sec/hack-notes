---
tags: [persistence, windows, scheduled-task, crto]
status: done
platform: windows
---

# Scheduled Task — Variantes Avanzadas

> Persistencia con tareas programadas más allá del trigger básico: arranque, logon y eventos, con principal privilegiado.

> Básico (comando `schtasks` desde Beacon) en [[03-post-explotacion/persistencia/scheduled-tasks-cs|Scheduled Tasks CS]].

---

## Concepto

Una tarea programada ejecuta una **acción** cuando se cumple un **trigger**. Para persistencia robusta interesa: un trigger fiable, un *principal* con el privilegio justo, y un nombre/ruta que se mezcle con las tareas del sistema.

---

## Triggers útiles

| Trigger | Dispara en | Nota |
|---------|-----------|------|
| **BootTrigger** | Arranque del sistema | Requiere SYSTEM/admin |
| **LogonTrigger** | Inicio de sesión | Opcional `UserId` concreto |
| **EventTrigger** | Un Event ID (p.ej. 4624) | Vía subscription XML |
| **CalendarTrigger** | Recurrente (diario/horario) | Usa `RandomDelay` |

---

## Registro vía XML

Definir la tarea en XML da control total (trigger + principal + acción):

```xml
<Triggers><BootTrigger><Enabled>true</Enabled></BootTrigger></Triggers>
<Principals><Principal>
  <UserId>S-1-5-18</UserId>
  <RunLevel>HighestAvailable</RunLevel>
</Principal></Principals>
<Actions><Exec><Command>C:\Windows\Temp\loader.exe</Command></Exec></Actions>
```

```
schtasks /create /tn "\Microsoft\Windows\<ruta-plausible>\Updater" /xml task.xml /ru SYSTEM
```

---

## OPSEC

> - Nombra la tarea imitando rutas reales (`\Microsoft\Windows\...`).
> - Evita `cmd /c` directo; apunta a un loader con nombre plausible.
> - `RandomDelay` evita ejecuciones a horas redondas.
> - Detección defensiva: **Security 4698** (task creada), archivos en `C:\Windows\System32\Tasks\`.

---

## Recursos

- **MITRE ATT&CK — T1053.005** (Scheduled Task).
- **HackTricks** — Windows scheduled tasks / privesc.
- **CRTO** — módulo *Persistence*.
