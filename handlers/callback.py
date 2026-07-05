import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.enums import ParseMode

from services.downloader import download, DownloadProgress
from services.file_manager import cleanup_file, is_within_limit, ensure_download_dir
from config import DOWNLOAD_DIR, MAX_FILE_SIZE
from services.logger import setup_logging

logger = setup_logging("handlers.callback")
router = Router()


@router.callback_query(F.data.startswith("dl|||"))
async def handle_quality_selection(callback: CallbackQuery):
    """Download the video with the selected quality and send it to the chat."""
    await callback.answer()
    # callback_data format: dl|||<format_id>|||<url>
    parts = callback.data.split("|||", 2)
    if len(parts) < 3:
        logger.warning("callback_data con formato invalido: %s", callback.data)
        return
    _, format_id, url = parts

    user_id = callback.from_user.id if callback.from_user else 0
    logger.info(
        "Descarga iniciada | user=%s chat=%s format=%s",
        user_id, callback.message.chat.id, format_id,
    )

    status_msg = await callback.message.edit_text(
        "\U0001F4E5 *Descargando\\.\\.\\.*",
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    try:
        await ensure_download_dir(DOWNLOAD_DIR)

        progress_msg = await status_msg.edit_text(
            "\U0001F4E5 *Descargando\\.\\.\\.* 0%",
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        last_progress: list[DownloadProgress] = []

        def on_progress(p: DownloadProgress):
            last_progress.clear()
            last_progress.append(p)

        async def poll_progress():
            while True:
                await asyncio.sleep(2)
                if last_progress:
                    p = last_progress[-1]
                    text = f"\U0001F4E5 *Descargando\\.\\.\\.* {p.percent:.0f}%"
                    if p.speed:
                        text += f" \u26A1{p.speed}"
                    try:
                        await progress_msg.edit_text(text, parse_mode=ParseMode.MARKDOWN_V2)
                    except Exception:
                        pass
                if last_progress and last_progress[-1].percent >= 99.0:
                    break
                await asyncio.sleep(0)

        poll_task = asyncio.create_task(poll_progress())

        try:
            output_path = await download(url, format_id, progress_callback=on_progress)
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            logger.info(
                "Descarga completada | user=%s size=%.1fMB",
                user_id, file_size_mb,
            )
        finally:
            poll_task.cancel()
            try:
                await poll_task
            except asyncio.CancelledError:
                pass

    except Exception as e:
        logger.error("Error en descarga | user=%s error=%s", user_id, e)
        await status_msg.edit_text(
            f"\u274c *Error al descargar:* {str(e)}",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    # Check file size against Telegram's 50MB limit
    file_size = output_path.stat().st_size
    if not is_within_limit(file_size, MAX_FILE_SIZE):
        logger.warning(
            "Archivo excede 50MB | user=%s size=%.1fMB",
            user_id, file_size / (1024 * 1024),
        )
        await cleanup_file(output_path)
        await status_msg.edit_text(
            "\u26A0\ufe0f El archivo supera los 50MB que permite Telegram\\.\n"
            "Intenta con *Solo audio* o *Mediana* calidad\\.",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    # Send file to user
    try:
        await status_msg.edit_text(
            "\U0001F4E4 *Subiendo a Telegram\\.\\.\\.*",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        input_file = FSInputFile(output_path)
        await callback.message.reply_video(input_file)
        logger.info("Video enviado | user=%s size=%.1fMB", user_id, file_size / (1024 * 1024))
        await status_msg.edit_text(
            "\u2705 *Listo\\!*",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    except Exception as e:
        logger.error("Error al enviar video | user=%s error=%s", user_id, e)
        await status_msg.edit_text(
            f"\u274c *Error al enviar:* {str(e)}",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    finally:
        await cleanup_file(output_path)
