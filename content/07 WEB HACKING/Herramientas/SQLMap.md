---
tags: [web, sqli, sqlmap, automatización]
status: done
---

# SQLMap — Automatización de SQL Injection

> Herramienta para detectar y explotar automáticamente vulnerabilidades SQLi.

---

## Uso básico desde lista de URLs

```bash
sqlmap -m urls_con_parametros.txt \
  --batch \
  --smart \
  --technique=BEU \
  --level=1 \
  --risk=1 \
  --threads=5 \
  --answers="follow=Y" \
  -o detection_results.txt
```

**Flags:**
- `-m` — lista de URLs con parámetros (una por línea)
- `--batch` — modo no interactivo (responde automáticamente)
- `--smart` — solo testea parámetros prometedores (reduce ruido)
- `--technique=BEU` — Boolean-based, Error-based, Union-based
- `--level / --risk` — agresividad del test (1-5)
- `-o` — heuristics output

---

## Ver también

- [[SQL Injection]] — técnicas manuales
