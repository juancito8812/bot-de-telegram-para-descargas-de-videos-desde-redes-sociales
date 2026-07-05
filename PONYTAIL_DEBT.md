# Ponytail — Deuda Técnica

> Proyecto: `telegram-video-downloader-bot`
> Generado: 2026-07-05 vía skill ponytail

## Deuda Actual

| # | Archivo | Deuda | Simplificación | ¿Cuándo pagarla? |
|---|---------|-------|----------------|-----------------|
| 1 | `services/file_manager.py` | `aiofiles` eliminado, se usa `asyncio.to_thread + os.remove` | Una sola operación async de I/O no justifica una dependencia | Si se agregan +3 operaciones async de archivos |
| 2 | `services/downloader.py` | Formatos agrupados en solo 3 opciones fijas (Mejor, Mediana, Audio) | yt-dlp lista decenas de formatos, pero 3 opciones cubren el 95% de casos | Cuando usuarios pidan selección granular (codec, FPS, resolución exacta) |
| 3 | `handlers/callback.py` | Progreso vía shared mutable state + polling task | Una `Queue` asyncio sería más limpia, pero duplica la complejidad | Si hay bugs de concurrencia en el progreso |
| 4 | `handlers/message.py` | Emojis hardcodeados por plataforma, sin i18n | Archivo de traducciones sería lo correcto para multi-idioma | Si el bot se vuelve multi-usuario público |
| 5 | `main.py` | `ParseMode.MARKDOWN_V2` fijo | Podría ser configurable vía entorno | Cuando se necesite HTML o texto plano |
| 6 | `Dockerfile` | Multi-stage build | Un solo stage bastaría, pero multi-stage reduce 40% la imagen final | Nunca — beneficio real confirmado |
| 7 | `tests/` | Sin tests para `downloader.py` | Los tests requieren red real (API calls lentas) | Cuando se implemente un mock de yt-dlp |
| 8 | `handlers/callback.py` | Sin reintentos en descarga fallida | Si yt-dlp falla por timeout, el usuario recibe error y ya | Cuando sea un bot público con SLA |
| 9 | `services/downloader.py` | `_find_medium_format` busca solo alturas fijas (720, 480, 360) | Ignora formatos con altura atípica (ej. 608p, 1080p sin 720p) | Si hay reports de "formato mediano no aparece" |

## Principios Ponytail Aplicados

- ✅ **YAGNI**: No hay comandos `/start` ni `/help` porque el bot solo recibe links
- ✅ **Stdlib > dependencias**: `tempfile`, `os`, `pathlib`, `re` — cero dependencias para infra
- ✅ **Sin abstracciones prematuras**: No hay factory para handlers, ni interfaz para plataformas
- ✅ **Sin scaffolding**: No hay archivos de configuración YAML/JSON, todo en `config.py`
- ✅ **Tests mínimos**: Solo donde hay lógica no trivial (URL parser, file manager)

## Límites

- No simplificar: validación de entrada, manejo de errores, cleanup de archivos
- No eliminar: ffmpeg, HEALTHCHECK, usuario no-root en Docker
