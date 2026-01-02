#!/usr/bin/env python3
"""
🤖 Menta Telegram Bot - Рабочая версия для старых библиотек
"""

import os
import sys
import logging
import random
import string

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

print("=" * 50)
print("🚀 Запуск Menta Code Bot...")
print("👨‍💻 Создатель: Г. Марк")
print("🏢 Команда: NexusMind2026")
print("📢 Канал: @nexusmind20_26")
print("=" * 50)

# Токен бота
TOKEN = "8228472308:AAFarC-gKzt3ZTaaafo5-wQLv03zXz6ZKMg"

# Импорт для старой версии
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
    print("✅ Библиотеки успешно импортированы")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("📦 Устанавливаем правильную версию...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==13.15"])
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Функция генерации кода
def generate_code(prefix="BOT"):
    chars = string.ascii_uppercase + string.digits
    code = f"{prefix}-{''.join(random.choices(chars, k=6))}"
    return code

# Обработчики команд
def start(update: Update, context: CallbackContext):
    """Обработчик /start"""
    user = update.message.from_user
    
    keyboard = [
        [InlineKeyboardButton("🎫 Код проверки", callback_data="verify")],
        [InlineKeyboardButton("📱 Код регистрации", callback_data="register")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"""
    🚀 *Привет, {user.first_name}!*
    
    🤖 *Menta Code Bot* - выдача кодов
    
    👨‍💻 *Создатель:* Г. Марк
    🏢 *Команда:* NexusMind2026
    📢 *Канал:* @nexusmind20_26
    
    Выберите действие:
    """
    
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

def button_handler(update: Update, context: CallbackContext):
    """Обработчик кнопок"""
    query = update.callback_query
    query.answer()
    
    user = query.from_user
    
    if query.data == "verify":
        code = generate_code("BOT")
        response = f"""
        ✅ *Код проверки:*
        
        📝 `{code}`
        👤 Для: {user.first_name}
        ⏰ Срок: 24 часа
        🎯 Для проверки ботов
        
        🏢 NexusMind2026
        """
        query.edit_message_text(response, parse_mode='Markdown')
    
    elif query.data == "register":
        code = generate_code("REG")
        response = f"""
        ✅ *Код регистрации:*
        
        📝 `{code}`
        👤 Для: {user.first_name}
        ⏰ Срок: 7 дней
        🎯 Для регистрации в Menta
        
        🏢 NexusMind2026
        """
        query.edit_message_text(response, parse_mode='Markdown')
    
    elif query.data == "help":
        help_text = """
        ℹ️ *Помощь по боту*
        
        *Как использовать:*
        • Нажмите "🎫 Код проверки" для тестирования
        • Нажмите "📱 Код регистрации" для приложения
        
        *Информация:*
        👨‍💻 Создатель: Г. Марк
        🏢 Команда: NexusMind2026
        📢 Канал: @nexusmind20_26
        
        *Поддержка:*
        По вопросам: @nexusmind20_26
        """
        query.edit_message_text(help_text, parse_mode='Markdown')

def help_command(update: Update, context: CallbackContext):
    """Команда /help"""
    update.message.reply_text("Используйте /start для начала работы")

def error_handler(update: Update, context: CallbackContext):
    """Обработчик ошибок"""
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    """Основная функция"""
    try:
        # Создаем Updater
        updater = Updater(TOKEN, use_context=True)
        
        # Получаем диспетчер
        dp = updater.dispatcher
        
        # Добавляем обработчики
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(CallbackQueryHandler(button_handler))
        
        # Добавляем обработчик ошибок
        dp.add_error_handler(error_handler)
        
        # Запускаем бота
        print("✅ Бот инициализирован")
        print("⏳ Начинаем polling...")
        
        updater.start_polling()
        
        print("🤖 Бот запущен и работает!")
        print("⏰ Ожидание сообщений...")
        
        # Бот работает до принудительной остановки
        updater.idle()
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
