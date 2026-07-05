# -*- mode: python ; coding: utf-8 -*-
"""
Spec para compilar Telegram Video Downloader Bot con PyInstaller.
Uso: python -m PyInstaller BotDownloader.spec
"""

from __future__ import annotations

import os
import sys

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[],
    hiddenimports=[
        'services',
        'services.logger',
        'services.downloader',
        'services.url_parser',
        'services.file_manager',
        'handlers',
        'handlers.message',
        'handlers.callback',
        # yt-dlp hidden imports
        'yt_dlp',
        'yt_dlp.extractor',
        'yt_dlp.extractor.youtube',
        'yt_dlp.extractor.tiktok',
        'yt_dlp.extractor.instagram',
        'yt_dlp.extractor.twitter',
        'yt_dlp.extractor.facebook',
        'yt_dlp.downloader',
        'yt_dlp.postprocessor',
        # aiogram
        'aiogram',
        'aiogram.fsm',
        'aiogram.fsm.state',
        'aiogram.fsm.storage.memory',
        'aiogram.client',
        'aiogram.client.session',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tests',
        'pytest',
        'unittest',
        'tkinter',
        'matplotlib',
        'numpy',
        'PIL',
        'cv2',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TelegramDownloaderBot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # True para ver logs en terminal
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
