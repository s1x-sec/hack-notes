---
title: Envenenamiento Responder
tags: [ad, responder, llmnr, ntlm, poisoning]
---

# Envenenamiento Responder

> [!tip] Cuándo usarlo
> En entornos de AD cuando podemos hacer peticiones hacia nuestra máquina. Responder envenena la red via LLMNR/NBT-NS y captura hashes NTLMv2.

## Ataque

```bash
sudo responder -I tun0
```

Cuando un usuario del dominio intenta conectarse a un recurso que no existe, Responder responde haciéndose pasar por ese recurso y captura el hash NTLMv2.

> [!important] Resultado
> Se obtiene un hash **NTLMv2** que se puede crackear con hashcat:
> ```bash
> hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt
> ```

## Caso práctico: HEIST
En la máquina HEIST se explota un envenenamiento tras descubrir que se pueden hacer peticiones hacia la máquina atacante. Al tratarse de un entorno AD, envenena la red con Responder al conectarse a sí mismo y se obtiene el hash NTLM.

## Ver también
- [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]]
- [[05-ad-attacks/kerberos/as-rep-roasting|AS-REP Roasting]]
