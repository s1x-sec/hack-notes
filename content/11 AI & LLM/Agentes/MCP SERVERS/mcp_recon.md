---
title: mcp_recon — MCP Server de Reconocimiento
tags: [ai, mcp, recon, pentest-agents]
---

# mcp_recon — Setup

## Instalación y arranque

```bash
cd mcp_recon/
npm install
node server.js &
```

## SSH Tunnel (si el servidor está en remoto)

```bash
ssh -L 8080:localhost:8080 root@169.58.204.70 -N
```

Mapea el puerto local 8080 al puerto 8080 del servidor remoto.

## Registrar en Claude

```bash
claude mcp add recon-mcp --transport http http://localhost:8082/mcp
```

> [!tip] Cambiar el puerto según la configuración del servidor (8080 ó 8082).

## Ver también
- [[11-ai--and--llm/agentes/mcp-servers|MCP SERVERS]]
- [[11-ai--and--llm/agentes|Agentes]]
