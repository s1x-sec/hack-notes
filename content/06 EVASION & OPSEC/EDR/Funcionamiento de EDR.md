---
title: Funcionamiento de EDR — Entropía y Evasión
tags: [opsec, edr, entropy, sleep-obfuscation, evasion]
---

# Funcionamiento de EDR — Entropía y Evasión

## Entropía

Los AVs/EDRs analizan el nivel de "aleatoriedad" de un archivo o región de memoria (escala 0-8).

| Tipo | Entropía |
|------|----------|
| Archivo de texto / .exe legítimo | 4.0 – 6.0 |
| Código cifrado con AES | 7.9 – 8.0 |

> [!warning] Alta entropía = alerta crítica de "Posible Malware Empaquetado"

## Técnicas para evitar detección por entropía

### 1. XOR en lugar de AES

En lugar de cifrar con algoritmos pesados, usar **XOR con contraseñas largas**. Desordena las firmas estáticas sin elevar demasiado la entropía.

### 2. Dilución (Padding)

Añadir al archivo megabytes de texto normal (ej: libro completo) o imágenes. La media de entropía del archivo baja y el EDR lo da por legítimo.

### 3. Sleep Obfuscation (Ekko / Gargoyle)

La técnica moderna por excelencia:

1. El Beacon va a dormir
2. **Se cifra su propia memoria** antes de dormir
3. Un milisegundo antes de despertar, **se descifra**
4. Se conecta al C2 y vuelve a cifrar

> [!tip] El EDR tendría que escanear la memoria en el milisegundo exacto en que el Beacon está despierto.

## Hooks del EDR

Los EDRs insertan instrucciones `JMP` en las primeras líneas de funciones nativas de `ntdll.dll` para redirigir la ejecución al motor del EDR antes de llegar al kernel.

### Direct Syscalls
El Beacon ejecuta `syscall` directamente desde su propia memoria.
- **Detectable**: el Call Stack muestra que la transición al kernel salió fuera de `ntdll.dll`.

### Indirect Syscalls
El Beacon lee `ntdll.dll` en memoria, calcula dónde está la instrucción `syscall` original y hace un JMP hacia allí.
- **Muy difícil de detectar**: la instrucción `syscall` se ejecuta desde la dirección legítima de `ntdll.dll`.

## Ver también
- [[06-evasion--and--opsec/malware/malware-essentials|Malware Essentials]]
- [[06-evasion--and--opsec/process-injection|Process Injection]]
- [[06-evasion--and--opsec/memory-evasion/beacon-memory-crto|Beacon Memory CRTO]]
- [[06-evasion--and--opsec/memory-evasion/sleep-obfuscation|Sleep Obfuscation]]
