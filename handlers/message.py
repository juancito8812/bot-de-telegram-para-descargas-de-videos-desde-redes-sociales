from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

from services.url_parser import parse_url, Platform
from services.downloader import list_formats, FormatOption
from services.logger import setup_logging

logger = setup_logging("handlers.message")
router = Router()

# ponytail: emojis inline en lugar de archivo de traduccion/i18n.
# Agregar sistema de idiomas si el bot se vuelve multi-usuario.
PLATFORM_EMOJIS = {
    Platform.YOUTUBE: "\u25B6\ufe0f",
    Platform.TIKTOK: "\U0001F3B5",
    Platform.INSTAGRAM: "\U0001F4F8",
    Platform.TWITTER: "\U0001F426",
    Platform.FACEBOOK: "\U0001F44D",
}


@router.message(F.text)
async def handle_message(message: Message):
    """Detect URLs in messages and offer quality selection."""
    text = message.text or ""
    platform = parse_url(text)
    if platform is None:
        return  # ignore messages without a supported URL

    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    logger.info("URL detectada | user=%s chat=%s platform=%s", user_id, chat_id, platform.value)

    emoji = PLATFORM_EMOJIS.get(platform, "\U0001F517")
    status_msg = await message.reply(
        f"{emoji} *Analizando enlace\\.\\.\\.*",
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    try:
        options = await list_formats(text)
        logger.info(
            "Formatos obtenidos | user=%s platform=%s count=%d",
            user_id, platform.value, len(options),
        )
    except Exception as e:
        logger.error(
            "Error al listar formatos | user=%s url=%.80s error=%s",
            user_id, text, e,
        )
        await status_msg.edit_text(
            f"\u274c *Error al analizar:* {str(e)}",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    if not options:
        logger.warning("Sin formatos disponibles | user=%s platform=%s", user_id, platform.value)
        await status_msg.edit_text(
            "\u274c No se encontraron formatos disponibles\\.",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=opt.label, callback_data=f"dl|||{opt.format_id}|||{text}")]
            for opt in options
        ]
    )

    await status_msg.edit_text(
        f"{emoji} *Selecciona calidad:*",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
