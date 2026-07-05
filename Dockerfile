# ──────────────────────────────────────────────
# Telegram Video Downloader Bot — Dockerfile
# ──────────────────────────────────────────────
# Multi-stage: install deps, then slim runtime.

# ── Stage 1: Dependencies ─────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build tools + ffmpeg (needed by yt-dlp for format merging)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ── Stage 2: Runtime ──────────────────────────
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy pip-installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

# Copy application code
COPY main.py config.py ./
COPY handlers/ ./handlers/
COPY services/ ./services/
COPY __init__.py ./

# Create downloads and logs directories
RUN mkdir -p downloads logs

# Run as non-root user for security
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Health check: verify the Python process is alive
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD pgrep -f "python main.py" || exit 1

# ── Environment variables ────────────────────
ENV BOT_TOKEN=""
ENV LOG_LEVEL="INFO"
ENV DOWNLOAD_DIR="./downloads"
ENV LOG_DIR="logs"

CMD ["python", "main.py"]
