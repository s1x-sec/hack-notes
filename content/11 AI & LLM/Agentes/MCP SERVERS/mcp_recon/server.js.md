---
tags: [ai, mcp, recon, nodejs, servidor]
status: done
---

# server.js — recon-mcp

MCP server propio para tools de recon, sobre HTTP (Streamable HTTP transport).

Envuelve **subfinder / httpx / naabu / nuclei / katana** como tools MCP, con:
- Validación de scope contra `scope.yaml` antes de ejecutar cualquier comando
- Timeouts y límite de output para no reventar el contexto del modelo

> [!NOTE] Sin autenticación
> `HOST=127.0.0.1` por defecto → no escucha en interfaz pública.
> El acceso remoto pasa por túnel SSH o Tailscale (capa de auth real).
> Si cambias `HOST` a `0.0.0.0`, añade auth antes.

---

## Tools MCP registradas

| Tool | Descripción |
|------|-------------|
| `subfinder` | Enumeración pasiva de subdominios |
| `httpx_probe` | HTTP probing con tech-detect y status code |
| `naabu_scan` | Escaneo de puertos |
| `katana_crawl` | Crawl de endpoints, JS, formularios |
| `nuclei_scan` | Escaneo de vulnerabilidades (activo) |
| `dnsx_resolve` | Resolución DNS (A, CNAME) |
| `tlsx_certinfo` | Info de certificado TLS + SANs |
| `gau_urls` | URLs históricas (Wayback, Common Crawl, OTX) |
| `waybackurls_fetch` | URLs históricas de Wayback Machine |
| `alterx_permute` | Permutaciones de subdominios |
| `puredns_resolve` | Resolución bulk DNS anti-wildcard |

---

## scope.yaml esperado

```yaml
in_scope:
  - "*.target.com"
  - "target.com"
out_of_scope:
  - "admin.target.com"
```

---

## Código completo

```js
// recon-mcp — MCP server propio para tools de recon, sobre HTTP (Streamable HTTP transport)
//
// Envuelve subfinder / httpx / naabu / nuclei / katana como tools MCP, con:
//   - validación de scope contra scope.yaml antes de ejecutar cualquier comando
//   - timeouts y límite de output para no reventar el contexto del modelo

import express from "express";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs";
import yaml from "js-yaml";
import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";

const execFileAsync = promisify(execFile);

// ---------- Config ----------
const HOST = process.env.RECON_MCP_HOST || "127.0.0.1";
const PORT = parseInt(process.env.RECON_MCP_PORT || "8082", 10);
const SCOPE_FILE = process.env.RECON_MCP_SCOPE || "./scope.yaml";
const MAX_OUTPUT_CHARS = 8000;
const CMD_TIMEOUT_MS = 5 * 60 * 1000;

// ---------- Scope check ----------
function loadScope() {
  if (!fs.existsSync(SCOPE_FILE)) {
    console.warn(`AVISO: no existe ${SCOPE_FILE} — TODO objetivo será rechazado.`);
    return { in_scope: [], out_of_scope: [] };
  }
  const doc = yaml.load(fs.readFileSync(SCOPE_FILE, "utf8"));
  return { in_scope: doc.in_scope || [], out_of_scope: doc.out_of_scope || [] };
}

function matchesPattern(host, pattern) {
  const regex = new RegExp("^" + pattern.replace(/\./g, "\\.").replace(/\*/g, ".*") + "$");
  return regex.test(host);
}

function isInScope(target) {
  const scope = loadScope();
  const host = target.replace(/^https?:\/\//, "").split("/")[0].split(":")[0];
  const blocked = scope.out_of_scope.some((p) => matchesPattern(host, p));
  if (blocked) return { ok: false, reason: `"${host}" está fuera de scope` };
  const allowed = scope.in_scope.some((p) => matchesPattern(host, p));
  if (!allowed) return { ok: false, reason: `"${host}" no coincide con ningún patrón in_scope` };
  return { ok: true };
}

// ---------- Ejecución segura ----------
async function runTool(bin, args, stdinInput) {
  try {
    const child = execFileAsync(bin, args, { timeout: CMD_TIMEOUT_MS, maxBuffer: 20 * 1024 * 1024 });
    if (stdinInput && child.child && child.child.stdin) {
      child.child.stdin.write(stdinInput);
      child.child.stdin.end();
    }
    const { stdout, stderr } = await child;
    let out = stdout || stderr || "(sin output)";
    if (out.length > MAX_OUTPUT_CHARS) {
      out = out.slice(0, MAX_OUTPUT_CHARS) + `\n\n[...truncado...]`;
    }
    return out;
  } catch (err) {
    if (err.killed) return `ERROR: timeout (${CMD_TIMEOUT_MS / 1000}s)`;
    return `ERROR ejecutando ${bin}: ${err.message}`;
  }
}

// ---------- Servidor HTTP ----------
const app = express();
app.use(express.json());

app.post("/mcp", async (req, res) => {
  const server = buildServer();
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  res.on("close", () => { transport.close(); server.close(); });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

app.listen(PORT, HOST, () => {
  console.log(`recon-mcp escuchando en http://${HOST}:${PORT}/mcp`);
  console.log(`Scope file: ${SCOPE_FILE}`);
});
```

---

## Ver también

→ [[mcp_recon]] — arranque e integración con Claude
