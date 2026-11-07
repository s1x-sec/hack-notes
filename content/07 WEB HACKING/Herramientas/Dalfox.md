---
tags: [web, xss, dalfox, automatización]
status: done
---

# Dalfox — Automatización de XSS

> Herramienta para detectar y explotar automáticamente vulnerabilidades XSS.

---

## Escaneo básico desde lista de URLs

```bash
dalfox scan urls_con_parametros.txt
```

## Con certificados autofirmados

```bash
dalfox file urls_con_parametros.txt \
  --skip-grepping \
  --skip-headless \
  -o dalfox_results.txt
```

---

## Ver también

- [[07-web-hacking/xss|XSS]] — técnicas manuales
