import asyncio
import logging
import sys

from telegram import ReplyKeyboardMarkup, Update
from telegram.error import Conflict
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def make_label(icons: dict, translations: dict):
    """Фабрика label(key, suffix) для построения текста кнопок."""
    def label(key: str, suffix: str = '') -> str:
        return icons[key] + ' ' + translations[key] + suffix
    return label


def run_bot(token: str, chat_id: int, keyboard: ReplyKeyboardMarkup, commands: dict):
    """
    token    - Telegram bot token
    chat_id  - разрешённый chat id
    keyboard - ReplyKeyboardMarkup для отображения кнопок
    commands - dict {текст_кнопки: callable} - синхронные функции платформы
    """
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id != chat_id:
            return

        command = update.message.text

        if command == '/start':
            await update.message.reply_text('Добро пожаловать!', reply_markup=keyboard)
            return

        action = commands.get(command)
        if action is None:
            await update.message.reply_text('Используйте кнопки на клавиатуре.', reply_markup=keyboard)
            return

        await asyncio.to_thread(action)
        await update.message.reply_text('Команда: %s' % command, reply_markup=keyboard)

    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
        if isinstance(context.error, Conflict):
            logger.error('Конфликт: уже запущен другой экземпляр бота. Завершение.')
            sys.exit(1)
        logger.error('Ошибка: %s', context.error)

    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT, handle))
    app.add_error_handler(error_handler)
    app.run_polling()
