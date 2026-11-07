---
tags: [opsec, evasion, beacon, memory, module-stomping]
status: done
platform: windows
---

# Beacon Memory Evasion

> Ocultar el beacon en memoria para evadir scans periódicos de EDRs.

---

## Problema: Memory Scanning

Los EDRs escanean la memoria de procesos periódicamente buscando:
1. **Headers PE** — firma MZ/PE del beacon
2. **Strings conocidas** — literales de texto del beacon
3. **Permisos RWX** — regiones de memoria con permiso de lectura+escritura+ejecución simultáneo

---

## RWX → RX Migration

El beacon por defecto se aloja en memoria RWX (Read-Write-Execute). Los EDRs detectan esto como anomalía (raro en código legítimo).

**Solución:** Configurar el beacon para que cambie los permisos a RX (read+execute) tras cargarse:

```
# En el perfil Malleable C2
stage {
    set userwx "false";       # No usar RWX — cambiar a RX tras cargar
    set startrwx "false";     # No arrancar con RWX
}
```

---

## Module Stomping

En lugar de alojar el beacon en memoria anónima (la que escanean los EDRs), cargarlo dentro de un módulo legítimo ya mapeado en el proceso.

```
# En el perfil Malleable C2
stage {
    set stomppe "true";
    set module_x64 "xpsservices.dll";    # DLL que se va a "pisar"
    set module_x86 "xpsservices.dll";
}
```

**Cómo funciona:** CS carga `xpsservices.dll` en memoria, luego escribe el beacon encima de esa región. La región pertenece a un módulo legítimo → los EDRs que verifican si la región tiene un módulo asociado no lo ven como anomalía.

**Consideración:** La DLL elegida debe:
- Estar en system32 (firmada por Microsoft)
- No ser cargada normalmente por el proceso host (para evitar conflictos)
- Ser del tamaño apropiado para el beacon

---

## Headers PE — copy_pe_header

El beacon contiene un header PE que los scans detectan. Podemos copiarlo de un DLL legítimo:

```
# En el perfil Malleable C2
stage {
    set userwx "false";
    set stomppe "true";
    set obfuscate "true";    # Ofuscar strings del beacon
}
```

---

## Strings — transform-x64

Ofuscar strings literales del beacon que los EDRs conocen:

```
# En el perfil Malleable C2
stage {
    transform-x64 {
        # Reemplazar string conocida
        strrep "ReflectiveLoader" "";
        strrep "beacon.dll" "";
    }
}
```

