# 🔧 PLUGINS SETUP

> Configuración recomendada para este vault. Instalar por orden de prioridad.

---

## INSTALACIÓN RÁPIDA

En Obsidian: `Settings → Community plugins → Browse`

---

## TIER 1 — IMPRESCINDIBLES

### 📊 Dataview
**Por qué:** Consultas SQL sobre tus notas. La query del HOME MAP que muestra notas activas depende de esto.
```
Instalar: Dataview
Configurar: Settings → Dataview → Enable JavaScript Queries ✅
```
**Uso inmediato:** El bloque `dataview` en el HOME ya funciona al instalar.

---

### 📁 Folder Notes
**Por qué:** Convierte el archivo `RECON.md` en la nota de la carpeta `01 RECON/`. Click en la carpeta abre la nota-índice directamente.
```
Instalar: Folder Notes
Configurar: Settings → Folder Notes → Note name = folder name ✅
```

---

### ⌨️ Quick Switcher++
**Por qué:** `Ctrl+Shift+O` busca símbolos dentro de un fichero. Busca headings, bloques de código, aliases. Mil veces mejor que el switcher nativo.
```
Instalar: Quick Switcher++
Hotkeys:
  Ctrl+O         → Open file
  Ctrl+Shift+O   → Search headings/symbols
  Ctrl+Shift+P   → Search commands
```

---

### 📝 Templater
**Por qué:** Templates con fecha automática, tipo de nota, tags. Evita crear notas vacías.
```
Instalar: Templater
Configurar:
  Settings → Templater → Template folder = _TEMPLATES ✅
  Settings → Templater → Trigger on new file creation ✅
Hotkey: Alt+N → New note from template
```
→ Ver [[_TEMPLATES/TEMPLATE NOTE]] para el template estándar.

---

## TIER 2 — RECOMENDADOS

### 🎨 Icon Folder
**Por qué:** Emojis/iconos en las carpetas del sidebar. Mejora la navegación visual enormemente.
```
Instalar: Iconize (Icon Folder)
```
Iconos sugeridos por carpeta:
- 00 HOME → 🏠
- 01 RECON → 🔭
- 02 INITIAL ACCESS → 💣
- 03 POST EXPLOTACION → ⚙️
- 04 LATERAL MOVEMENT → ↔️
- 05 AD ATTACKS → 🏛️
- 06 EVASION & OPSEC → 👻
- 07 WEB HACKING → 🌐
- 08 INFRAESTRUCTURA C2 → 🎯
- 09 CLOUD → ☁️
- 10 MOBILE → 📱
- 11 AI & LLM → 🤖
- 12 TOOLS & REFERENCIA → 🔧

---

### ✏️ Excalidraw
**Por qué:** Diagramas de red, flujos de ataque, arquitecturas AD directamente en Obsidian. Útil para documentar entornos de labs.
```
Instalar: Excalidraw
Crear diagrama: New note → Change to Excalidraw
```

---

### 📋 Kanban
**Por qué:** Tablero de tareas para gestionar el progreso de un engagement o de rellenar notas vacías.
```
Instalar: Kanban
Crear tablero: New note → Change to Kanban
```

---

### 🔀 Git
**Por qué:** Backup automático del vault a GitHub. MUCHO mejor que Syncthing (sin conflict files).
```
Instalar: Obsidian Git
Setup:
  1. git init en la carpeta del vault
  2. git remote add origin <tu-repo-privado>
  3. Settings → Obsidian Git → Auto pull interval: 10 min ✅
  4. Settings → Obsidian Git → Auto push interval: 30 min ✅
  5. Settings → Obsidian Git → Commit message: "vault: {{date}}" ✅

IMPORTANTE: Añadir al .gitignore:
  .obsidian/workspace*
  .trash/
  *.sync-conflict-*
```

---

## TIER 3 — OPCIONALES

### 🎨 Style Settings
**Por qué:** Si usas el tema Minimal o AnuPpuccin, este plugin da control granular sobre colores, fuentes y espaciado.
```
Instalar: Style Settings
Requiere: Tema compatible (Minimal recomendado)
```

### 🔍 Tag Wrangler
**Por qué:** Renombrar y gestionar tags masivamente. Útil cuando los tags crezcan.
```
Instalar: Tag Wrangler
```

---

## CONFIGURACIÓN OBSIDIAN BASE (sin plugins)

```
Settings → Editor:
  Default view for new tabs: Source mode ✅ (o Live Preview, según preferencia)
  Spell check: OFF (para notas técnicas)
  
Settings → Files & Links:
  Default location for new notes: Same folder as current file ✅
  Use Wikilinks ✅
  
Settings → Appearance:
  Theme: Minimal (instalar desde Community themes)
  Font size: 16px
```

---

## TEMA RECOMENDADO: Minimal

El tema más limpio para notas técnicas. Se combina con **Minimal Theme Settings** (plugin adicional) para personalizar colores de los code blocks por lenguaje.

```
Settings → Appearance → Manage → Buscar "Minimal" → Install and use
```

