---
title: Android — ADB (Android Debug Bridge)
tags: [mobile, android, adb]
---

# ADB — Android Debug Bridge

## Comandos básicos

| Comando | Descripción |
|---------|-------------|
| `adb devices` | Listar dispositivos conectados |
| `adb connect <ip>:5555` | Conectar via TCP/IP |
| `adb install <apk>` | Instalar APK |
| `adb logcat` | Ver logs del sistema |
| `adb shell netstat -an` | Ver conexiones de red activas |
| `adb push <local> <remote>` | Subir archivo al dispositivo |
| `adb pull <remote> <local>` | Descargar archivo del dispositivo |
| `adb shell` | Abrir shell en el dispositivo |

## Casos de uso en pentesting

```bash
# Conectar al emulador local
adb connect 127.0.0.1:5555

# Instalar apk modificada (repackaged)
adb install -r patched.apk

# Ver logs de la app objetivo
adb logcat | grep com.target.app

# Extraer APK del dispositivo
adb shell pm path com.target.app
adb pull /data/app/com.target.app-1/base.apk ./target.apk

# Explorar sistema de archivos (root)
adb shell
# dentro del shell:
su
ls /data/data/com.target.app/
```

## TCP/IP mode (sin cable USB)

```bash
# Con el dispositivo conectado por USB:
adb tcpip 5555
adb connect <device-ip>:5555
adb disconnect  # desconectar USB, ya va por red
```

## Ver también
- [[Rootear Telefono]]
- [[Teoría Android]]
