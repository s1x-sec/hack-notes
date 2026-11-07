---
tags: [opsec, dotnet, pinvoke, marshaling, csharp]
status: done
platform: windows
---

# .NET & P/Invoke

> Llamar a APIs nativas de Windows (Win32) desde código C# mediante Platform Invocation Services.

---

## C++ vs C# para Ofensiva

| | C++ | C# (.NET) |
|-|-----|-----------|
| Acceso a Win32 | Directo | Via P/Invoke |
| Overhead | Mínimo | Pequeño (runtime .NET) |
| Facilidad | Compleja | Sencilla |
| Detección | Por la técnica | También por el runtime .NET |
| Uso típico en CS | Artifact Kit, BOFs | execute-assembly, tools |

---

## P/Invoke — Estructura Básica

```csharp
using System.Runtime.InteropServices;

// Declarar la función nativa de Windows
[DllImport("kernel32.dll", SetLastError = true)]
static extern IntPtr OpenProcess(
    uint dwDesiredAccess,
    bool bInheritHandle,
    uint dwProcessId
);

// Usar la función
IntPtr hProc = OpenProcess(0x001F0FFF, false, (uint)pid);
```

---

## Marshaling — Tipos Equivalentes

| Win32 (C++) | C# (Managed) | Notas |
|------------|--------------|-------|
| DWORD | uint / uint32 | Sin signo 32-bit |
| HANDLE | IntPtr | Pointer a handle |
| BOOL | bool | true/false |
| LPVOID | IntPtr | Puntero genérico |
| LPCWSTR | string | Con CharSet.Unicode |
| LPBYTE / byte[] | byte[] | Array de bytes |
| LPCTSTR | string | Depende del charset |

---

## CharSet — Strings Unicode vs ANSI

```csharp
// Para APIs que usan strings Unicode (la mayoría en Windows moderno)
[DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
static extern bool CreateProcess(
    string lpApplicationName,
    string lpCommandLine,
    ...
);

// Para APIs ANSI (antiguas, menos comunes)
[DllImport("kernel32.dll", CharSet = CharSet.Ansi)]
```

---

## Estructuras — StructLayout

Para pasar estructuras a APIs nativas, deben tener layout explícito:

```csharp
[StructLayout(LayoutKind.Sequential)]
public struct STARTUPINFO {
    public uint cb;
    public string lpReserved;
    public string lpDesktop;
    public string lpTitle;
    // ... resto de campos
}

[StructLayout(LayoutKind.Sequential)]
public struct PROCESS_INFORMATION {
    public IntPtr hProcess;
    public IntPtr hThread;
    public uint dwProcessId;
    public uint dwThreadId;
}
```

---

## Ejemplo Completo — VirtualAllocEx + WriteProcessMemory

```csharp
[DllImport("kernel32.dll", SetLastError = true)]
static extern IntPtr VirtualAllocEx(IntPtr hProcess, IntPtr lpAddress, 
    uint dwSize, uint flAllocationType, uint flProtect);

[DllImport("kernel32.dll", SetLastError = true)]
static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress,
    byte[] lpBuffer, uint nSize, out UIntPtr lpNumberOfBytesWritten);

// Uso
IntPtr pRemote = VirtualAllocEx(hProc, IntPtr.Zero, (uint)shellcode.Length, 
                                0x3000, 0x40);  // MEM_COMMIT|RESERVE, PAGE_RWX

UIntPtr bytesWritten;
WriteProcessMemory(hProc, pRemote, shellcode, (uint)shellcode.Length, out bytesWritten);
```

---

## Pinvoke.net — Referencia

Para encontrar las firmas P/Invoke de cualquier función Win32:
→ [https://pinvoke.net](https://pinvoke.net)

