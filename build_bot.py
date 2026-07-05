#!/usr/bin/env python3
"""
Telegram Video Downloader Bot — Build .EXE
-------------------------------------------
Compila el bot a un ejecutable portátil con PyInstaller.

Uso:  python build_bot.py
      python build_bot.py --quick   (salta instalación PyInstaller)
      python build_bot.py --no-clean (no limpia builds anteriores)
"""

import os
import sys
import subprocess
import shutil
import time

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def print_step(num, total, text):
    print(f"\n{YELLOW}[{num}/{total}] > {text}...{RESET}")

def print_ok(text):
    print(f"  {GREEN}[OK] {text}{RESET}")

def print_warn(text):
    print(f"  {YELLOW}[WARN] {text}{RESET}")

def print_error(text):
    print(f"  {RED}[ERROR] {text}{RESET}")


def run_command(cmd, desc="Comando", timeout=300):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, (result.stderr or result.stdout).strip()
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def check_python():
    ok, ver = run_command("python --version")
    if ok:
        print_ok(f"Python {ver.split()[-1]}")
        return True
    print_error("Python no está en PATH")
    return False


def check_pyinstaller():
    ok, ver = run_command("python -m PyInstaller --version", timeout=30)
    if ok:
        print_ok(f"PyInstaller {ver.strip()}")
        return True
    print("  [..] Instalando PyInstaller...")
    ok, out = run_command("pip install pyinstaller", timeout=120)
    if ok:
        print_ok("PyInstaller instalado")
        return True
    print_error(f"No se pudo instalar PyInstaller: {out[:200]}")
    return False


def clean_old_builds():
    for path, is_file in [
        ("dist/TelegramDownloaderBot.exe", True),
        ("dist/TelegramDownloaderBot", False),
        ("build/TelegramDownloaderBot", False),
    ]:
        if os.path.exists(path):
            try:
                if is_file:
                    os.remove(path)
                else:
                    shutil.rmtree(path)
            except Exception:
                pass


def compile_exe(no_clean=False):
    cmd = "python -m PyInstaller BotDownloader.spec"
    if not no_clean:
        cmd += " --clean"
    print(f"\n  Ejecutando: {cmd}")
    print(f"  {YELLOW}Esto puede tomar 2-3 minutos...{RESET}\n")
    start = time.time()
    ok, out = run_command(cmd, timeout=300)
    elapsed = time.time() - start
    if ok:
        print_ok(f"Compilación completada en {int(elapsed)}s")
        return True
    lines = out.split("\n")
    print_error(f"Fallo ({int(elapsed)}s):\n  " + "\n  ".join(lines[-15:]))
    return False


def verify_exe():
    exe_path = "dist/TelegramDownloaderBot.exe"
    if not os.path.exists(exe_path):
        print_error(f"No se encontró: {exe_path}")
        return False
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print()
    print(f"{GREEN}╔══════════════════════════════════════════╗{RESET}")
    print(f"{GREEN}║   [OK] EXE CREADO EXITOSAMENTE!         ║{RESET}")
    print(f"{GREEN}╚══════════════════════════════════════════╝{RESET}")
    print()
    print(f"  {CYAN}Ubicación:{RESET} {os.path.abspath(exe_path)}")
    print(f"  {CYAN}Tamaño:{RESET}    {size_mb:.1f} MB")
    print()
    return True


def main():
    quick = "--quick" in sys.argv
    no_clean = "--no-clean" in sys.argv

    print(f"{CYAN}{BOLD}╔══════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}{BOLD}║  Telegram Downloader Bot - Build .EXE   ║{RESET}")
    print(f"{CYAN}{BOLD}╚══════════════════════════════════════════╝{RESET}")
    print()

    if not check_python():
        sys.exit(1)

    total = 2
    step = 0

    if not quick:
        step += 1
        if not check_pyinstaller():
            sys.exit(1)

    step += 1
    if not no_clean:
        clean_old_builds()
    if not compile_exe(no_clean):
        sys.exit(1)

    verify_exe()
    print(f"\n{YELLOW}Ruta del exe:{RESET}  dist\\TelegramDownloaderBot.exe")
    print(f"{YELLOW}Token (CMD):{RESET}        set BOT_TOKEN=tu_token")
    print(f"{YELLOW}Token (PowerShell):{RESET}  \$env:BOT_TOKEN=\"tu_token\"")
    print(f"{YELLOW}O .env:{RESET}            echo BOT_TOKEN=tu_token > .env")
    print()


if __name__ == "__main__":
    main()
