---
title: Persistencia — COM Hijacking
tags: [persistence, com-hijacking, registry]
---

# COM Hijacking

## Descripción

El hijacking de COM Objects permite persistencia sin privilegios elevados sobrescribiendo la referencia a un objeto COM en `HKCU` (tiene prioridad sobre `HKLM`).

## Metodología

1. Identificar COM Objects cargados por aplicaciones legítimas (Process Monitor)
2. Verificar que el CLSID tiene entrada en `HKLM` pero NO en `HKCU`
3. Crear la entrada en `HKCU` apuntando a nuestro payload

```
HKCU\SOFTWARE\Classes\CLSID\{CLSID}\InProcServer32
  → valor: C:\Users\user\AppData\Local\payload.dll
```

> [!tip] No requiere privilegios de administrador. Es más difícil de detectar que Run Keys.

> [!important] El DLL debe exportar las funciones COM esperadas para no romper la aplicación legítima.
