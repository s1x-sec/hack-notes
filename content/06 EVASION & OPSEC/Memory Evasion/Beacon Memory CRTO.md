---
tags: [evasion, opsec, cobalt-strike, memory, crto]
status: done
platform: windows
---

# Beacon Memory — Indicadores y Evasión

> Reducir la huella en memoria del Beacon para evadir el escaneo de memoria de los EDR (YARA/firmas), sobre todo mientras duerme.

> Relacionado: [[06-evasion--and--opsec/memory-evasion/sleep-obfuscation|Sleep Obfuscation]] · [[06-evasion--and--opsec/edr/funcionamiento-de-edr|Funcionamiento de EDR]].

---

## Concepto

El Beacon vive en memoria dentro de un proceso. Los EDR escanean memoria buscando:

- Páginas **RWX** (read/write/execute) → anómalo; raro en código legítimo.
- Memoria privada ejecutable **sin respaldo en disco** (*unbacked / floating code*).
- **Firmas/YARA** del contenido del Beacon (cadenas, cabeceras, estructura) mientras está "dormido".

El objetivo de OPSEC es que, especialmente **durante el sleep**, el contenido del Beacon no sea identificable.

---

## 1. Malleable C2 — perfil de memoria

El perfil C2 controla cómo se asigna y ofusca la memoria:

- `set userwx "false"` → evita páginas RWX (asigna RW y luego cambia a RX).
- `set cleanup "true"` → libera la memoria del loader tras cargar el Beacon.
- `set obfuscate "true"` → ofusca el Beacon en reposo.
- **Module stomping** (`module_x64`) → mapea el Beacon sobre una DLL legítima ya cargada (memoria tipo *image*, no privada).

---

## 2. Sleep Mask

Mientras el Beacon está en sleep, el **Sleep Mask** cifra sus páginas y las restaura al despertar, de modo que un escaneo durante el reposo solo ve datos cifrados.

- CS incluye un sleep mask por defecto; técnicas públicas conocidas (Ekko, Foliage, Zilean) además enmascaran el *stack* mediante timers/ROP.
- Detalle en [[06-evasion--and--opsec/memory-evasion/sleep-obfuscation|Sleep Obfuscation]].

---

## 3. Allocation y stack

- **RW → RX** en lugar de RWX al asignar/inyectar.
- **Module stomping**: ejecutar desde una sección *image* respaldada en disco reduce la sospecha de "unbacked".
- **Call stack spoofing**: oculta el stack del hilo del Beacon durante llamadas sensibles.

---

## OPSEC — checklist

> - `userwx false`, `cleanup true`, sleep mask activo.
> - Evita asignaciones RWX en inyección; usa RW→RX.
> - Sleep largo + jitter reduce las ventanas de escaneo.
> - **Valida** tu huella con herramientas de detección antes de operar.

---

## Recursos (incl. detección/validación)

- **Moneta** (@forrest-orr) — detección de memoria anómala.
- **pe-sieve / hollows_hunter** (@hasherezade) — implantes en memoria.
- **Hunt-Sleeping-Beacons** — detección de beacons en sleep.
- **Cobalt Strike docs** — Malleable C2 (bloques `stage` / `process-inject` / `sleepmask`).
- **CRTO** — módulo *Evasion* (memory / sleep / artifacts).
