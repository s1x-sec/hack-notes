---
title: Containers — Mark of the Web Bypass
tags: [initial-access, motw, container, phishing, packmypayload]
---

# Containers — Mark of the Web Bypass

Los contenedores se usan para bypassear la protección **Mark of the Web (MotW)**: archivos descargados de internet quedan marcados como sospechosos, lo que impide ejecución de macros y alerta a EDRs/AVs.

## PackMyPayload

Empaqueta el payload dentro de un contenedor de imagen (.img, .iso) que no propaga el MotW a su contenido.

```bash
python3 PackMyPayload.py -H decoy.xlsx,payload.xlam /mnt/c/Payloads/xlam /mnt/c/Payloads/xlam/package.img
```

Repo: https://github.com/mgeeky/PackMyPayload

## Ver también
- [[02-initial-access/triggers|Triggers]]
- [[02-initial-access/payloads|Payloads]]
- [[02-initial-access/técnicas/delivery|Delivery]]
