---
tags: [web, recon, subdominios, enumeracion]
status: done
---

# Descubrimiento de Subdominios

> Objetivo: descubrir la mayor cantidad posible de subdominios mediante fuentes pasivas.

---

## Herramientas

```bash
# Subfinder — fuentes pasivas / APIs
subfinder -d target.com -o subfinder.txt

# Assetfinder — búsqueda rápida de activos
assetfinder --subs-only target.com > assetfinder.txt

# Amass — enumeración pasiva profunda
amass enum -passive -d target.com -o amass.txt

# Sublist3r — motores de búsqueda + open-source
sublist3r -d target.com -o sublist3r.txt

# Chaos — base de datos ProjectDiscovery
chaos -d target.com -silent -o chaos.txt
```

---

## Consolidación

```bash
# Unir todos los resultados, eliminar duplicados
cat *.txt | sort -u > all_subs.txt
```

---

## Siguiente paso

→ [[Filtrado]] — verificar cuáles responden
