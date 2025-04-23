import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

TELEGRAM_TOKEN = '7857576817:AAE-ub22uXfBRx-qEW2ri2oIEllOpF486F0'
LM_API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "gemma-3-4b-it-qat"

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Ты — профессиональный медицинский помощник, связанный с Высшим медицинским колледжем города Астана. "
        "Отвечай на медицинские вопросы чётко, вежливо и понятно для обычных людей. "
        "Если вопрос не по медицине — вежливо объясни, что ты можешь помочь только в рамках медицины."
    )
}

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    payload = {
        "model": MODEL_NAME,
        "messages": [
            SYSTEM_PROMPT,
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(LM_API_URL, json=payload)
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text(f"Ошибка API: {response.status_code}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка подключения: {str(e)}")

def start_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", lambda update, context: update.message.reply_text(
        "Привет! Я медицинский бот, связанный с Высшим медицинским колледжем Астаны. "
        "Задай вопрос по здоровью, и я постараюсь помочь."
    )))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    loop = asyncio.get_event_loop()
    loop.create_task(application.run_polling())

if __name__ == '__main__':
    start_bot()
    asyncio.get_event_loop().run_forever()
