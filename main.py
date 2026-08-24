#!/usr/bin/env python3
"""Telegram Video Downloader Bot — Entry Point."""

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode

from config import BOT_TOKEN, TELEGRAM_API_URL
from handlers import message, callback
from services.logger import setup_logging

logger = setup_logging("bot")


async def main():
    """Initialize bot, register handlers, and start polling."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable is not set!")
        return

    # ponytail: MARKDOWN_V2 fijo. Si se necesita HTML o sin formato,
    # parametrizar en config.py.
    # Timeout 300s para subida de archivos grandes a Telegram.
    session_kwargs = {"timeout": 300}
    if TELEGRAM_API_URL:
        session_kwargs["api"] = TelegramAPIServer.from_base(TELEGRAM_API_URL)
        logger.info("Using local Bot API server: %s", TELEGRAM_API_URL)
    else:
        logger.info("Using Telegram Cloud API")

    session = AiohttpSession(**session_kwargs)
    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )
    dp = Dispatcher()

    dp.include_router(message.router)
    dp.include_router(callback.router)

    logger.info("Bot started! Send a video URL to test.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
