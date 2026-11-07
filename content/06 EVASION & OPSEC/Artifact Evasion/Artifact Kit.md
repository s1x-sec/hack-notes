---
tags: [opsec, evasion, artifact-kit, cobalt-strike, threatcheck]
status: done
platform: windows
---

# Artifact Kit

> Modificar el shellcode wrapper de Cobalt Strike para evadir detección estática de AV/EDR.

---

## Flujo de Trabajo

```
1. ThreatCheck → identifica bytes que disparan la firma
2. Ghidra → localizar el offset exacto en el .c del Artifact Kit
3. Modificar el .c → cambiar el byte/bloque problemático
4. Recompilar → nuevo artifact_kit.cna
5. Cargar en CS → Script Manager → artifact_kit.cna
```

---

## 1. ThreatCheck — Identificar la firma

```powershell
# Escanear el artefacto generado por CS
ThreatCheck.exe -f artifact64.exe
ThreatCheck.exe -f artifact64.exe -e Defender    # Motor específico

# Output: "Bad bytes found" + offset hex donde está la detección
# Ejemplo: Offset: 0x1234  Length: 16
```

---

## 2. Ghidra — Localizar en el código fuente

```
1. Abrir el artifact compilado en Ghidra (artifact64.exe)
2. Ir al offset que reportó ThreatCheck (Window → Go To Address → 0x1234)
3. Identificar la función/lógica que genera esos bytes
4. Localizar la función equivalente en el código fuente (.c del Kit)
```

→ Ver [[../../12 TOOLS & REFERENCIA/Ghidra/Ghidra]] para workflow detallado de Ghidra.

---

## 3. Modificar el Código Fuente

```c
// Ejemplo: fragmento en artifact.c que genera bytes detectados
// Antes (detectado):
char shellcode[] = "\x48\x83\xEC\x28...";

// Después (obfuscado con XOR):
char enc_shellcode[] = "\x58\x93\xFC\x38...";  // XOR 0x10
// + rutina de decodificación en runtime
```

**Técnicas comunes de modificación:**
- XOR encoding del shellcode loader
- Cambiar orden de operaciones del loader
- Insertar NOPs / dead code entre bytes detectados
- Usar indirect function calls en lugar de directas

---

## 4. Recompilar

```bash
# Dentro del directorio del Artifact Kit
./build.sh     # Linux cross-compiler (desde el arsenal kit de CS)
# Genera: artifact_kit.cna + binarios modificados
```

---

## 5. Cargar en Cobalt Strike

```
Cobalt Strike → Script Manager → Load → artifact_kit.cna
```

Desde ahora, todos los payloads generados usarán el artifact modificado.

---

## Verificar

```powershell
# Generar nuevo payload y volver a escanear
ThreatCheck.exe -f nuevo_artifact64.exe
# Objetivo: "No threat found"
```

