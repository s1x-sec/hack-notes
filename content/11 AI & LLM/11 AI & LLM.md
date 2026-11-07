---
tags: [ai, llm, mcp, prompt-injection]
status: wip
---

# AI & LLM SECURITY

> Ataques contra sistemas basados en LLMs y agentes de IA.

---

## Índice

| Tema | Nota |
|------|------|
| LLM API Attack Surface | [[LLM API Attack Surface]] |
| Indirect Prompt Injection | [[Indirect Prompt Injection]] |
| Chaining Vulnerabilities | [[Chaining Vulnerabilities]] |
| Agentes de IA | [[Agentes/Agentes]] |
| MCP Servers (índice) | [[Agentes/MCP SERVERS/MCP SERVERS]] |
| mcp_recon (overview) | [[Agentes/MCP SERVERS/mcp_recon]] |
| mcp_recon — package.json | [[Agentes/MCP SERVERS/mcp_recon/package.json]] |
| mcp_recon — server.js | [[Agentes/MCP SERVERS/mcp_recon/server.js]] |

---

## Surface de Ataque

```
LLM System
    ├── Prompt Injection (directo e indirecto)
    │     ├── Jailbreak — evadir restricciones del modelo
    │     └── Indirect injection — via datos externos que el LLM procesa
    │
    ├── Agentes (LLM con herramientas)
    │     ├── Tool abuse — forzar uso incorrecto de herramientas
    │     ├── SSRF via tool de URL fetching
    │     └── Privilege escalation via contexto del agente
    │
    └── MCP Servers
          ├── Tool poisoning — herramienta maliciosa en servidor MCP
          ├── Inyección en tool output — output que redirige al LLM
          └── Exfiltración via llamadas a herramientas externas
```

---

## Referencias

- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [PromptInjection.com](https://www.promptinjection.com/)
- [Gandalf — práctica de prompt injection](https://gandalf.lakera.ai/)
