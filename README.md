# Telegram Video Downloader Bot

Bot de Telegram que descarga videos de redes sociales: YouTube, TikTok, Instagram, Twitter/X y Facebook.

## Requisitos

- Python 3.11+
- Token de bot de Telegram (de [@BotFather](https://t.me/botfather))

## Instalación

### Opción 1: Docker (recomendado)

```bash
docker compose up -d --build
```

### Opción 2: Podman (rootless)

```bash
podman-compose up -d --build
```

### Opción 3: Python directo

```bash
pip install -r requirements.txt
python main.py
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto:

```bash
BOT_TOKEN="tu_token_aqui"
LOG_LEVEL=INFO
```

(Opcional) Cambiar directorio de descargas:

```bash
DOWNLOAD_DIR="./downloads"
```

## Uso

```bash
docker compose up -d   # o: podman-compose up -d
```

Envía cualquier enlace de video al bot y selecciona la calidad deseada mediante los botones inline.

### Deploy en debianm700 (M700 ThinkCentre)

El bot corre como servicio systemd user en `debianserver@debianm700` (100.77.200.34):

```bash
ssh debianm700

# Ver logs
podman logs telegram-downloader-bot

# Reiniciar
systemctl --user restart telegram-bot.service

# Actualizar
cd ~/bot-descargas && git pull && podman-compose build && podman-compose up -d

# Estado
systemctl --user status telegram-bot.service
```

**Stack**: podman-compose (rootless) + systemd user service + linger (auto-start en boot).

## Redes Soportadas

| Plataforma | Dominios |
|-----------|----------|
| ▶️ YouTube | youtube.com, youtu.be |
| 🎵 TikTok | tiktok.com |
| 📸 Instagram | instagram.com |
| 🐦 Twitter / X | twitter.com, x.com |
| 👍 Facebook | facebook.com, fb.com |

## Variables de Entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `BOT_TOKEN` | — | **Requerido.** Token del bot de Telegram |
| `LOG_LEVEL` | `INFO` | Nivel de logging: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `DOWNLOAD_DIR` | `./downloads` | Directorio para archivos descargados |
| `LOG_DIR` | `logs` | Directorio para archivos de log |

## Características

- ✅ Detección automática de enlaces (sin comandos)
- ✅ Selección de calidad: Mejor, Mediana, Solo audio
- ✅ Descargas asíncronas (no bloquea el bot)
- ✅ Límite de 50MB de Telegram manejado
- ✅ Limpieza automática de archivos temporales
- ✅ Logging con rotación (5MB por archivo, 3 backups)

## Estructura del Proyecto

```
telegram-video-downloader-bot/
├── main.py              # Entry point
├── config.py            # Configuración
├── Dockerfile           # Multi-stage build (Python 3.11 + ffmpeg)
├── docker-compose.yml   # Orquestación Docker/Podman
├── handlers/
│   ├── message.py       # Detecta URLs
│   └── callback.py      # Procesa selección de calidad
├── services/
│   ├── url_parser.py    # Identifica red social
│   ├── downloader.py    # Descarga con yt-dlp
│   └── file_manager.py  # Archivos temporales
├── tests/               # Tests unitarios
├── .env                 # Variables de entorno (NO commitear)
├── requirements.txt
└── README.md
```
