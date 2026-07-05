#!/usr/bin/env python3
"""Telegram Video Downloader Bot — Entry Point."""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import message, callback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Initialize bot, register handlers, and start polling."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable is not set!")
        return

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )
    dp = Dispatcher()

    dp.include_router(message.router)
    dp.include_router(callback.router)

    logger.info("Bot started! Send a video URL to test.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
