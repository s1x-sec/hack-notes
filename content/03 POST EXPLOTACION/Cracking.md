---
tags: [cracking, hashcat, john]
---

# Cracking

## Identificar el Hash

```bash
hashid '<hash>'
hash-identifier '<hash>'
```

## Hashcat

```bash
# NTLM (Windows)
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt

# Net-NTLMv2 (Responder)
hashcat -m 5600 hashes.txt /usr/share/wordlists/rockyou.txt

# Kerberoasting
hashcat -m 13100 hashes.kerberoast /usr/share/wordlists/rockyou.txt -r best64.rule

# AS-REP Roasting
hashcat -m 18200 hashes.asreproast /usr/share/wordlists/rockyou.txt -r best64.rule

# MD5
hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt

# SHA-256
hashcat -m 1400 hashes.txt /usr/share/wordlists/rockyou.txt

# bcrypt
hashcat -m 3200 hashes.txt /usr/share/wordlists/rockyou.txt

# Con reglas
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Mostrar hashes crackeados
hashcat -m 1000 hashes.txt --show
```

## John the Ripper

```bash
john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
john hashes.txt --show

# SSH Keys
ssh2john id_rsa > id_rsa.hash
john id_rsa.hash --wordlist=/usr/share/wordlists/rockyou.txt

# ZIP
zip2john archivo.zip > zip.hash
john zip.hash --wordlist=/usr/share/wordlists/rockyou.txt
```

## Tipos de Hash Comunes

| Tipo          | Modo hashcat |
| ------------- | ------------ |
| MD5           | 0            |
| SHA-256       | 1400         |
| NTLM          | 1000         |
| Net-NTLMv1    | 3000         |
| Net-NTLMv2    | 5600         |
| Kerberoasting | 13100        |
| AS-REP Roast  | 18200        |
| bcrypt        | 3200         |

