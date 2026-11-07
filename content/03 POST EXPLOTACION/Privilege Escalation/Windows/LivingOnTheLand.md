---
tags: [privesc, windows, lolbas]
---

# Living Off The Land — Escritura

## Buscar Rutas Escribibles

```powershell
$path = "C:\inetpub"
Get-ChildItem $path -Directory -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
    $testFile = Join-Path $_.FullName "test_write.txt"
    try {
        New-Item -Path $testFile -ItemType File -Force -ErrorAction Stop | Out-Null
        Remove-Item $testFile -Force
        Write-Output "Writable: $($_.FullName)"
    } catch {}
}
```

