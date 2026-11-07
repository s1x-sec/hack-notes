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
| Artifact Kit (shellcode en disco) | [[06-evasion--and--opsec/artifact-evasion/artifact-kit\|Artifact Kit]] |
| Script Artifact (AMSI/PS) | [[06-evasion--and--opsec/artifact-evasion/script-artifact\|Script Artifact]] |
| Command Line Detections | [[06-evasion--and--opsec/artifact-evasion/command-line-detections\|Command Line Detections]] |

---

## Evasión de Memoria

| Técnica | Nota |
|---------|------|
| Beacon Memory (scans de memoria) | [[06-evasion--and--opsec/memory-evasion/beacon-memory\|Beacon Memory]] |
| Sleep Obfuscation | [[06-evasion--and--opsec/memory-evasion/sleep-obfuscation\|Sleep Obfuscation]] |

---

## Process Injection

| Técnica | Nota |
|---------|------|
| Process Injection (clásica, APC, hijack) | [[06-evasion--and--opsec/process-injection\|Process Injection]] |
| Process Injection Avanzado | [[06-evasion--and--opsec/process-injection/process-injection-avanzado\|Process Injection Avanzado]] |
| PPID Spoofing | [[06-evasion--and--opsec/process-injection/ppid-spoofing\|PPID Spoofing]] |

---

## Teoría & Fundamentos

| Tema | Nota |
|------|------|
| .NET & P/Invoke | [[06-evasion--and--opsec/net-y-pinvoke\|NET y PInvoke]] |
| Funcionamiento EDR | [[06-evasion--and--opsec/edr/funcionamiento-de-edr\|Funcionamiento de EDR]] |
| Malware Essentials | [[06-evasion--and--opsec/malware/malware-essentials\|Malware Essentials]] |

---

## Decision Tree

> [!question] ¿Dónde está la detección?
>
> **Ejecutable / shellcode en disco**
> → [[06-evasion--and--opsec/artifact-evasion/artifact-kit|Artifact Kit]]
>
> **Script PowerShell detectado**
> → [[06-evasion--and--opsec/artifact-evasion/script-artifact|Script Artifact]] — AMSI bypass + ofuscación
>
> **Beacon detectado en memoria**
> → Strings/headers visibles → [[06-evasion--and--opsec/memory-evasion/beacon-memory|Beacon Memory]]
> → Beacon activo mientras duerme → [[06-evasion--and--opsec/memory-evasion/sleep-obfuscation|Sleep Obfuscation]]
>
> **Proceso padre o línea de comandos sospechosa**
> → [[06-evasion--and--opsec/process-injection/ppid-spoofing|PPID Spoofing]] + `spawnto`
>
> **Inyección de proceso detectada**
> → [[06-evasion--and--opsec/process-injection|Process Injection]] — elegir técnica menos agresiva
