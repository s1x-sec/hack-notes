---
tags: [opsec, evasion, ppid, process-creation, kernel]
status: done
platform: windows
---

# Command Line Detections

> Evadir detección basada en argumentos de línea de comandos y creación de procesos.

---

## El Problema

Los EDRs monitorean la creación de procesos a nivel de kernel via:
- `PsSetCreateProcessNotifyRoutineEx` — callback del kernel registrado por el AV/EDR
- Captura: imagen del proceso, línea de comandos, proceso padre

Esto significa que incluso si ofuscamos el script, la línea de comandos del proceso creado puede delatar la operación.

---

## PPID Spoofing

Falsificar el proceso padre del beacon para parecer un proceso legítimo (ej: parecer que Word nos lanzó, no cmd.exe).

→ Ver [[../Process Injection/PPID Spoofing]] para el workflow completo.

---

## Bloqueo a Nivel Kernel (spawnto)

Cobalt Strike usa un proceso temporal para fork & run. El `spawnto` configura qué proceso usa:

```
# En el perfil Malleable C2
post-ex {
    set spawnto_x64 "%windir%\\sysnative\\dllhost.exe";
    set spawnto_x86 "%windir%\\syswow64\\dllhost.exe";
}

# O interactivamente en CS
beacon> spawnto x64 c:\windows\sysnative\dllhost.exe
beacon> spawnto x86 c:\windows\syswow64\dllhost.exe
```

**Proceso de selección:** Usar procesos que:
1. Se ejecutan frecuentemente en el entorno
2. No tienen firma con restricciones (no Protected Processes)
3. Son esperables en el contexto de la sesión

---

## Bloqueo de Creación de Procesos Hijos (Token-based)

Windows permite configurar políticas que impidan que un proceso cree hijos. Esto puede usarse para endurecer nuestros procesos beacon contra técnicas de inyección, pero también es detección de los EDRs.

**Mitigación Job Object:**
```c
// En C++ — configurar proceso para no crear hijos
JOBOBJECT_BASIC_LIMIT_INFORMATION limits = {};
limits.LimitFlags = JOB_OBJECT_LIMIT_ACTIVE_PROCESS;
limits.ActiveProcessLimit = 1;
SetInformationJobObject(hJob, JobObjectBasicLimitInformation, &limits, sizeof(limits));
```

---

## Parent Process como Indicador

Correlación sospechosa que deben evitarse:

| Proceso Padre | Proceso Hijo Sospechoso |
|--------------|------------------------|
| WINWORD.EXE | cmd.exe, powershell.exe |
| OUTLOOK.EXE | cmd.exe, wscript.exe |
| explorer.exe | wscript.exe (script de internet) |
| cmd.exe | powershell -enc ... (base64 largo) |

