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
1. Con build.sh se construyen las plantillas
2. ThreatCheck → identifica bytes que disparan la firma
3. Ghidra → localizar el offset exacto en el .c del Artifact Kit
4. Modificar el .c → cambiar el byte/bloque problemático
5. Recompilar → nuevo artifact_kit.cna
6. Cargar en CS → Script Manager → artifact_kit.cna
```

---
## 1. Buildsh para construir los artefactos

Tiene que ser desde WSL

![[Pasted image 20261114135611.png]]

```
./build.sh mailslot VirtualAlloc 344564 0 false false none /mnt/c/Tools/cobaltstrike/custom-artifacts
```

## 1. ThreatCheck — Identificar la firma

```powershell
# Escanear el artefacto generado por CS
C:\Tools\ThreatCheck\ThreatCheck\bin\Debug\ThreatCheck.exe -f .\artifact64big.exe

ThreatCheck.exe -f artifact64.exe
ThreatCheck.exe -f artifact64.exe -e Defender    # Motor específico

# Output: "Bad bytes found" + offset hex donde está la detección
# Ejemplo: Offset: 0x1234  Length: 16
```

![[Pasted image 20261114135919.png]]

---

## 2. Ghidra — Localizar en el código fuente

```
1. Abrir el artifact compilado en Ghidra (artifact64.exe)
2. Ir al offset que reportó ThreatCheck (Window → Go To Address → 0x1234)
3. Identificar la función/lógica que genera esos bytes
4. Localizar la función equivalente en el código fuente (.c del Kit)
```

Navigation -- Goto

![[Pasted image 20261114140645.png]]



→ Ver [[12-tools--and--referencia/ghidra|Ghidra]] para workflow detallado de Ghidra.

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

