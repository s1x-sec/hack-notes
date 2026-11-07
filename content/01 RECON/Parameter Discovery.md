---
tags: [recon, web, parameters, arjun]
---

# Parameter Discovery

---

## Arjun

```bash
arjun -i base_urls.txt -m GET -c 250 -o arjun_output.json
arjun -i base_urls.txt -m POST -c 250 -o arjun_output.json
```

Extraer los parámetros encontrados:

```bash
jq -r 'to_entries[] | .key as $url | .value[] | "\($url)?\(.)="' arjun_output.json > params_arjun.txt
```

---

## Extracción de Parámetros Existentes (desde Katana)

```python
import sys
from urllib.parse import urlparse, parse_qs

urls_con_params = set()
with open("solo_urls.txt", "r") as f:
    for line in f:
        line = line.strip()
        if "?" in line:
            parsed = urlparse(line)
            base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            query_params = parse_qs(parsed.query)
            for param in query_params.keys():
                urls_con_params.add(f"{base_url}?{param}=")

with open("params_existentes.txt", "w") as out:
    for item in sorted(urls_con_params):
        out.write(item + "\n")
```

---

## Unificar Todo

```bash
cat params_existentes.txt params_arjun.txt | sort -u > todos_los_parametros.txt
```

