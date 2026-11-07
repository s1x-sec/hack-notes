---
tags: [lateral-movement, pivoting, ssh, port-forwarding]
status: done
platform: linux
---

# Port Forwarding — SSH

> Tunelizar tráfico a través de SSH cuando no hay C2 disponible.

---

## Local Port Forwarding

```bash
# Exponer servicio interno (172.16.50.217:445) a través del pivot (10.4.50.215)
ssh -N -L 0.0.0.0:4455:172.16.50.217:445 database_admin@10.4.50.215

# Túnel específico para un servicio en localhost del pivot
ssh -L 65432:localhost:65432 -i id_ed25519 user@192.168.230.210
```

**Formato:** `-L [bind_address:]port:host:hostport`

- `0.0.0.0:4455` — escuchar en todas las interfaces locales, puerto 4455
- `172.16.50.217:445` — destino interno al que reenviar
- `database_admin@10.4.50.215` — pivot host (salto SSH)

---

## Dynamic SOCKS Proxy

```bash
# SOCKS4/5 dinámico via SSH (reemplaza múltiples -L)
ssh -D 1080 -N user@pivot-host

# En proxychains4.conf:
# socks5 127.0.0.1 1080
proxychains4 nmap -sT -Pn 172.16.50.0/24
```

---

## Ver también

- [[04-lateral-movement/tecnicas/pivoting-con-cobalt|Pivoting con Cobalt]] — SOCKS4a via Cobalt Strike + Proxifier
- [[04-lateral-movement/tecnicas/ligolo-ng|Ligolo-ng]] — pivoting de capa 3 más robusto
