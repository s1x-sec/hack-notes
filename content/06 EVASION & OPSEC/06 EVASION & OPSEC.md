---
tags: [opsec, evasion]
status: done
---

# EVASION & OPSEC

> Operar sin dejar artefactos detectables por AV/EDR.

---

## Evasión de Artefactos

| Técnica | Nota |
|---------|------|
| Artifact Kit (shellcode en disco) | [[Artifact Evasion/Artifact Kit]] |
| Script Artifact (AMSI/PS) | [[Artifact Evasion/Script Artifact]] |
| Command Line Detections | [[Artifact Evasion/Command Line Detections]] |

---

## Evasión de Memoria

| Técnica | Nota |
|---------|------|
| Beacon Memory (scans de memoria) | [[Memory Evasion/Beacon Memory]] |
| Sleep Obfuscation | [[Memory Evasion/Sleep Obfuscation]] |

---

## Process Injection

| Técnica | Nota |
|---------|------|
| Process Injection (clásica, APC, hijack) | [[Process Injection/Process Injection]] |
| Process Injection Avanzado | [[Process Injection/Process Injection Avanzado]] |
| PPID Spoofing | [[Process Injection/PPID Spoofing]] |

---

## Teoría & Fundamentos

| Tema | Nota |
|------|------|
| .NET & P/Invoke | [[NET y PInvoke]] |
| Funcionamiento EDR | [[EDR/Funcionamiento de EDR]] |
| Malware Essentials | [[Malware/Malware Essentials]] |

---

## Decision Tree

> [!question] ¿Dónde está la detección?
>
> **Ejecutable / shellcode en disco**
> → [[Artifact Evasion/Artifact Kit]]
>
> **Script PowerShell detectado**
> → [[Artifact Evasion/Script Artifact]] — AMSI bypass + ofuscación
>
> **Beacon detectado en memoria**
> → Strings/headers visibles → [[Memory Evasion/Beacon Memory]]
> → Beacon activo mientras duerme → [[Memory Evasion/Sleep Obfuscation]]
>
> **Proceso padre o línea de comandos sospechosa**
> → [[Process Injection/PPID Spoofing]] + `spawnto`
>
> **Inyección de proceso detectada**
> → [[Process Injection/Process Injection]] — elegir técnica menos agresiva
