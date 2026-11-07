---
title: Android — Rootear Teléfono
tags: [mobile, android, root, magisk, frida, burp]
---

# Rootear Teléfono Android (para Pentesting)

## Repo de automatización

> [!tip] Repo con scripts automatizados para rootear dispositivos de prueba.
> https://github.com/rodrigo-pentest/android-root-scripts

## Stack completo de pentesting móvil

| Herramienta | Función |
|-------------|---------|
| **Magisk** | Root + gestión de módulos |
| **Frida** | Dynamic instrumentation (hooking) |
| **Burp Suite** | Interceptar tráfico HTTPS |

## Setup paso a paso

### 1. Instalar Magisk

1. Desbloquear bootloader del dispositivo
2. Flashear Magisk en el boot.img
3. Instalar Magisk Manager APK

### 2. Instalar certificado de Burp

```bash
# Exportar certificado de Burp como DER
# Renombrar a cert.pem o cert.crt

# Via Magisk Module (Android 7+)
# Instalar módulo "Move Certificates" en Magisk
# O usar script de instalación al sistema

# Verificar instalación
adb shell ls /system/etc/security/cacerts/ | grep burp
```

### 3. Instalar Frida Server

```bash
# Descargar frida-server para la arch del dispositivo
wget https://github.com/frida/frida/releases/download/XX.X.X/frida-server-XX.X.X-android-arm64.xz
xz -d frida-server*.xz

# Subir al dispositivo
adb push frida-server /data/local/tmp/
adb shell chmod +x /data/local/tmp/frida-server

# Arrancar frida-server (requiere root)
adb shell su -c '/data/local/tmp/frida-server &'
```

## Bypass Anti-Root Detection

### Método 1: Magisk Hide

En Magisk Manager → Magisk Hide → activar para la app objetivo.

### Método 2: Decompile + Patch + Repack

```bash
# Decompilar APK
apktool d target.apk -o target_decompiled/

# Buscar y parchear detección de root
grep -r "RootBeer\|isRooted\|superuser\|Magisk" target_decompiled/smali/

# Recompilar y firmar
apktool b target_decompiled/ -o patched.apk
apksigner sign --ks-key-alias key0 --ks debug.jks patched.apk
adb install patched.apk
```

### Método 3: Frida Script

```javascript
// bypass_root.js
Java.perform(function() {
    var RootBeer = Java.use('com.scottyab.rootbeer.RootBeer');
    RootBeer.isRooted.overload().implementation = function() {
        return false;
    };
});
```

```bash
frida -U -n com.target.app -l bypass_root.js
```

## Ver también
- [[10-mobile/android/adb|ADB]]
- [[10-mobile/android/teoría-android|Teoría Android]]
