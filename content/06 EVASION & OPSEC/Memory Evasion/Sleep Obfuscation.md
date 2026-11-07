---
tags: [opsec, evasion, sleep-obfuscation, ekko, gargoyle, entropy]
status: done
platform: windows
---

# Sleep Obfuscation

> Ocultar el beacon mientras duerme (callback interval) para evadir memory scanning.

---

## El Problema

Entre callbacks, el beacon está "dormido" en memoria. Es el momento en que los EDRs escanean más agresivamente. El beacon sigue visible en memoria — solo está inactivo.

---

## Entropía — Concepto

La entropía mide la aleatoriedad de un bloque de datos (escala 0-8):
- **0** — datos completamente predecibles (todos iguales)
- **8** — datos completamente aleatorios (cifrado, shellcode)

**Problema:** El shellcode del beacon tiene entropía alta (~7.5-8) → detectable como cifrado/shellcode.

**Soluciones para bajar entropía:**
- **Dilución:** Intercalar bytes de valor conocido (ej: 0x00 cada N bytes)
- **Padding:** Añadir secciones de datos con entropía baja
- **XOR con clave de baja entropía:** Usar clave que no incremente mucho la entropía

---

## Ekko

Técnica de sleep obfuscation que cifra el beacon mientras duerme:

```
Funcionamiento:
1. Beacon entra en sleep
2. Ekko cifra la región de memoria del beacon con un patrón de timers (ROP-based)
3. Beacon duerme — en memoria solo hay datos cifrados (sin firma)
4. Al despertar, Ekko descifra y resume ejecución
```

**Ventaja:** Durante el sleep, el scanner del EDR ve solo bytes cifrados sin firma reconocible.

---

## Gargoyle

Alternativa a Ekko. Usa timers de APC para:
1. Cambiar permisos de la región del beacon a NO_ACCESS antes del sleep
2. Durante el sleep → la región es inaccesible (ni leer)
3. Al despertar → restaurar permisos

**Diferencia vs Ekko:** No cifra, sino hace la región inaccesible físicamente.

---

## Configuración en Cobalt Strike

```
# En el perfil Malleable C2
stage {
    set sleep_mask "true";    # Habilitar sleep obfuscation nativa de CS
}
```

La sleep mask nativa de CS es menos avanzada que Ekko/Gargoyle pero más estable.

