---
title: LLM — API Attack Surface
tags: [ai, llm, api, excessive-agency]
---

# LLM API Attack Surface

## Flujo de una llamada API al LLM

```
1. Cliente envía petición → API Gateway
2. API Gateway valida auth (API key, OAuth)
3. Request llega al LLM Engine
4. LLM procesa: System Prompt + Conversation History + User Input
5. LLM genera respuesta
6. Si hay Tools/Functions → LLM llama herramientas externas
7. Resultado de herramientas → vuelve al LLM
8. LLM genera respuesta final → cliente
```

## Superficie de ataque por punto

| Punto | Vulnerabilidades |
|-------|-----------------|
| API Gateway | Auth bypass, rate limit bypass, IDOR |
| System Prompt | Extracción de prompt, manipulación |
| User Input | Prompt Injection, Jailbreak |
| Conversation History | Context manipulation |
| Tool calls | SSRF, SQLi, RCE, Path traversal |
| Output | Data exfiltration, XSS stored |

## Excessive Agency

El LLM tiene más permisos/capacidades de los necesarios para su función:

```
Ejemplo: Un chatbot de soporte que:
- Puede leer/escribir cualquier tabla de la DB (no solo la de tickets)
- Puede enviar emails a cualquier dirección
- Puede acceder a APIs internas sin restricción
```

> [!warning] **Excessive Agency** = el LLM puede hacer daño involuntario o ser manipulado para hacer daño intencionado.

## Mitigaciones

- Auditar todas las tools/functions del LLM
- Aplicar mínimo privilegio en cada herramienta
- Logs de todas las llamadas a herramientas
- Output filtering antes de mostrar al usuario

## Ver también
- [[11-ai--and--llm/indirect-prompt-injection|Indirect Prompt Injection]]
- [[Chaining Vulnerabilities (LLM)]]
