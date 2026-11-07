---
tags: [tools, ghidra, reverse-engineering, threatcheck]
status: done
---

# Ghidra — Workflow para Evasión

> Usar Ghidra para localizar el origen de una detección identificada por ThreatCheck.

---

## Flujo Completo

```
ThreatCheck → offset donde está la detección
     ↓
Ghidra → localizar ese offset en el desensamblado
     ↓
Identificar la función/bloque de código que lo genera
     ↓
Localizar ese bloque en el código fuente del Artifact Kit
     ↓
Modificar + recompilar
```

---

## 1. Importar Artifact en Ghidra

```
1. File → Import File → artifact64.exe
2. Seleccionar formato: PE COFF
3. Auto-analyze: YES (esperar)
```

---

## 2. Ir al Offset de ThreatCheck

ThreatCheck da un offset hexadecimal donde está la detección:

```
[ThreatCheck output]
Bad bytes found at offset 0x1234
Length: 16 bytes
```

En Ghidra:
```
Window → Go To Address → 0x1234
```

**Importante:** El offset de ThreatCheck es desde el inicio del archivo (raw offset). Para convertir a dirección virtual: `raw offset + ImageBase`.

---

## 3. Analizar el Código

```
- Click derecho → Disassemble si no está desensamblado
- Ctrl+E → Decompile Window (versión C aproximada)
- Identificar qué APIs llama el bloque detectado
```

---

## 4. Correlacionar con Código Fuente

```bash
# Buscar en el Artifact Kit la función equivalente
grep -r "VirtualAlloc\|CreateThread\|WriteProcess" artifact_kit/src/
```

---

## Tips

- El decompiler es aproximado — confiar más en el asm
- Las funciones importadas (IAT) dicen qué APIs usa el artifact
- Si usa syscalls directas, buscar instrucción `syscall`
