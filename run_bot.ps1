# run_bot.ps1 — Lanza el bot en background con registro de PID
# Útil para ejecutar al iniciar sesión o vía Task Scheduler

param(
    [string]$BotToken = "",
    [string]$LogLevel = "INFO"
)

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogDir = Join-Path $ProjectDir "logs"

# Crear directorio de logs si no existe
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# Variables de entorno
$env:BOT_TOKEN = $BotToken
$env:LOG_LEVEL = $LogLevel
$env:DOWNLOAD_DIR = Join-Path $ProjectDir "downloads"
$env:LOG_DIR = $LogDir

# Lanzar el bot
$logFile = Join-Path $LogDir "startup.log"
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    $process = Start-Process -FilePath "python" -ArgumentList "main.py" `
        -WorkingDirectory $ProjectDir `
        -NoNewWindow -PassThru `
        -RedirectStandardOutput (Join-Path $LogDir "stdout.log") `
        -RedirectStandardError (Join-Path $LogDir "stderr.log")

    # Guardar PID
    $process.Id | Out-File (Join-Path $ProjectDir "bot.pid")
    "$date [INFO] Bot iniciado con PID $($process.Id)" | Out-File $logFile -Append
    Write-Host "Bot iniciado con PID $($process.Id)"
}
catch {
    "$date [ERROR] Fallo al iniciar el bot: $_" | Out-File $logFile -Append
    Write-Error "Fallo al iniciar el bot: $_"
}
