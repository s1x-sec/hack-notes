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
| LLM API Attack Surface | [[11-ai--and--llm/llm-api-attack-surface|LLM API Attack Surface]] |
| Indirect Prompt Injection | [[11-ai--and--llm/indirect-prompt-injection|Indirect Prompt Injection]] |
| Chaining Vulnerabilities | [[11-ai--and--llm/chaining-vulnerabilities|Chaining Vulnerabilities]] |
| Agentes de IA | [[11-ai--and--llm/agentes|Agentes]] |
| MCP Servers (índice) | [[11-ai--and--llm/agentes/mcp-servers|MCP SERVERS]] |
| mcp_recon (overview) | [[11-ai--and--llm/agentes/mcp-servers/mcp_recon|mcp_recon]] |
| mcp_recon — package.json | [[11-ai--and--llm/agentes/mcp-servers/mcp_recon/package.json|package.json]] |
| mcp_recon — server.js | [[11-ai--and--llm/agentes/mcp-servers/mcp_recon/server.js|server.js]] |

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
