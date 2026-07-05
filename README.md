# Telegram Video Downloader Bot

Bot de Telegram que descarga videos de redes sociales: YouTube, TikTok, Instagram, Twitter/X y Facebook.

## Requisitos

- Python 3.11+
- Token de bot de Telegram (de [@BotFather](https://t.me/botfather))

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

```bash
export BOT_TOKEN="tu_token_aqui"
```

(Opcional) Cambiar directorio de descargas:

```bash
export DOWNLOAD_DIR="./downloads"
```

## Uso

```bash
python main.py
```

Envía cualquier enlace de video al bot y selecciona la calidad deseada mediante los botones inline.

## Redes Soportadas

| Plataforma | Dominios |
|-----------|----------|
| ▶️ YouTube | youtube.com, youtu.be |
| 🎵 TikTok | tiktok.com |
| 📸 Instagram | instagram.com |
| 🐦 Twitter / X | twitter.com, x.com |
| 👍 Facebook | facebook.com, fb.com |

## Características

- ✅ Detección automática de enlaces (sin comandos)
- ✅ Selección de calidad: Mejor, Mediana, Solo audio
- ✅ Descargas asíncronas (no bloquea el bot)
- ✅ Límite de 50MB de Telegram manejado
- ✅ Limpieza automática de archivos temporales

## Estructura del Proyecto

```
telegram-video-downloader-bot/
├── main.py              # Entry point
├── config.py            # Configuración
├── handlers/
│   ├── message.py       # Detecta URLs
│   └── callback.py      # Procesa selección de calidad
├── services/
│   ├── url_parser.py    # Identifica red social
│   ├── downloader.py    # Descarga con yt-dlp
│   └── file_manager.py  # Archivos temporales
├── tests/               # Tests unitarios
├── requirements.txt
└── README.md
```
