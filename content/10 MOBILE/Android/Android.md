---
tags: [mobile, android, adb]
status: wip
---

# Android

> Análisis y explotación de aplicaciones Android.

---

## ADB — Comandos Básicos

```bash
# Listar dispositivos conectados
adb devices

# Shell en el dispositivo
adb shell

# Instalar APK
adb install app.apk

# Transferir archivos
adb push local_file /sdcard/remote_file
adb pull /sdcard/remote_file local_file

# Logs del sistema
adb logcat | grep -i "app.name"

# Captura de pantalla
adb exec-out screencap -p > screenshot.png
```

---

## Análisis Estático

```bash
# Descompilar APK
apktool d app.apk -o app_decompiled

# Decompile a Java (más legible)
jadx -d output_dir app.apk

# Buscar secrets en el código fuente
grep -r "api.key\|secret\|password\|http://" app_decompiled/

# Analizar AndroidManifest.xml
cat app_decompiled/AndroidManifest.xml | grep -E "exported|permission|activity|service"
```

---

## Análisis Dinámico con Frida

```bash
# Instalar frida-server en el dispositivo
adb push frida-server /data/local/tmp/
adb shell chmod 755 /data/local/tmp/frida-server
adb shell /data/local/tmp/frida-server &

# Listar procesos
frida-ps -U

# Hookear función específica
frida -U -n "com.target.app" -l script.js
```

---

## SSL Pinning Bypass

```bash
# Con objection (automatizado)
objection -g com.target.app explore
ios sslpinning disable

# Con Frida + script
frida -U -n "com.target.app" --codeshare akabe4/frida-multiple-unpinning
```
