---
tags: [web, recon, parametros, arjun]
status: done
---

# Arjun — Descubrimiento de Parámetros

> Descubre parámetros HTTP ocultos en peticiones GET y POST.

---

## Uso básico

```bash
# GET
arjun -i base_urls.txt -m GET -c 250 -o arjun_output.json

# POST
arjun -i base_urls.txt -m POST -c 250 -o arjun_output.json
```

## Extraer parámetros del output JSON

```bash
jq -r 'to_entries[] | .key as $url | .value[] | "\($url)?\(.)="' arjun_output.json > params_arjun.txt
```

## Combinar con Katana

```bash
# Unificar parámetros de Katana + Arjun
cat params_existentes.txt params_arjun.txt | sort -u > todos_los_parametros.txt
```
