---
tags: [tools, powershell, obfuscation, amsi]
status: done
---

# Invoke-Obfuscation

> Ofuscación de scripts PowerShell a nivel de AST (Abstract Syntax Tree).

---

## Instalación

```powershell
git clone https://github.com/danielbohannon/Invoke-Obfuscation.git
cd Invoke-Obfuscation
Import-Module .\Invoke-Obfuscation.psd1
Invoke-Obfuscation
```

---

## Interfaz Interactiva

```
Invoke-Obfuscation> SET SCRIPTPATH C:\scripts\payload.ps1
Invoke-Obfuscation> TOKEN

# Sub-menú TOKEN
Invoke-Obfuscation\TOKEN> ALL       # Todas las técnicas de token
Invoke-Obfuscation\TOKEN> 1         # Solo STRING
Invoke-Obfuscation\TOKEN> 2         # Solo COMMAND
Invoke-Obfuscation\TOKEN> 3         # Solo ARGUMENT
Invoke-Obfuscation\TOKEN> 4         # Solo MEMBER
Invoke-Obfuscation\TOKEN> 5         # Solo WHITESPACE

# Guardar resultado
Invoke-Obfuscation\TOKEN> OUT C:\output\obfuscated.ps1
```

---

## Uso Directo

```powershell
Invoke-Obfuscation -ScriptPath C:\payload.ps1 -Command "TOKEN\ALL" -Quiet |
    Out-File C:\obfuscated.ps1
```

---

## Por qué funciona contra AMSI

Genera variantes semánticamente equivalentes con representación léxica diferente. El scanner de AMSI no reconoce los patrones obfuscados — solo conoce las firmas de las versiones sin ofuscar.

**Limitación:** AMSI en PS 5.1+ también puede analizar el AST compilado, no solo el texto → algunas técnicas TOKEN siguen siendo detectadas. Combinarlo con técnicas de bypass de AMSI en memoria.
