import asyncio
import json
import os
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from aiokafka import AIOKafkaConsumer

# --- Конфигурация ---
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не задан!")

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPICS = ["partner_db_events.public_cards", "partner_db_events.public_sections"]
subscribers = set()


# --- Telegram handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subscribers.add(update.effective_chat.id)
    print(f"folowing subscribers: {update.effective_chat.id}")
    await update.message.reply_text("✅ Подписан на уведомления!")


def format_message(event: dict) -> str:
    table = event.get("table")
    action = event.get("action")
    data = event.get("data", {})
    old = event.get("dataOld", {})

    if table == "cards":
        title = data.get("title") or old.get("title") or "Без названия"
        if action == "INSERT":
            print(f"🆕 Карточка добавлена:\n<b>{title}</b>\n data: {data} \n old: {old}")
            return f"🆕 Карточка добавлена:\n<b>{title}</b>\n data: {data}"
        elif action == "DELETE":
            print(f"🗑 Карточка удалена:\n<b>{title}</b>\n data: {data} \n old: {old}")
            return f"🗑 Карточка удалена:\n<b>{title}</b>\n data: {data}"
        elif action == "UPDATE":
            print(f"Карточка обновлена:\n<b>{title}</b>\n data: {data} \n old: {old}")
            return f"Карточка обновлена:\n<b>{title}</b>\n data: {data}"
    elif table == "sections":
        title = data.get("title") or old.get("title") or "Без названия"
        if action == "INSERT":
            print(f"📁 Раздел добавлен:\n<b>{title}</b>\n data: {data} \n old: {old}")
            return f"📁 Раздел добавлен:\n<b>{title}</b>"
        elif action == "DELETE":
            print(f"🗑 Раздел удалён:\n<b>{title}</b>\n data: {data} \n old: {old}")
            return f"🗑 Раздел удалён:\n<b>{title}</b>"
        elif action == "UPDATE":
            print(f"Раздел обновлен:\n<b>{title}</b>\n data: {data} \n old: {old}")
            return f"Раздел обновлен:\n<b>{title}</b>"
    return f"🔔 {action} в {table}"


# --- Kafka consumer (асинхронный) ---
async def kafka_listener(application):
    consumer = AIOKafkaConsumer(
        *TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="telegram-notifier",
        auto_offset_reset="latest",
    )
    await consumer.start()
    print("✅ Kafka listener запущен")

    try:
        async for msg in consumer:
            try:
                event = json.loads(msg.value.decode("utf-8"))
                text = format_message(event)
            except Exception as e:
                print(f"⚠️ Ошибка: {e}")
                continue

            for chat_id in list(subscribers):
                try:
                    await application.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
                except Exception as e:
                    print(f"❌ Не отправлено в {chat_id}: {e}")
                    subscribers.discard(chat_id)
    finally:
        await consumer.stop()


# --- Запуск ---
def main():
    print("🚀 Запуск Telegram-бота...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Запускаем Kafka в отдельном потоке
    def run_kafka():
        asyncio.run(kafka_listener(application))

    threading.Thread(target=run_kafka, daemon=True).start()

    # Блокирующий запуск бота
    application.run_polling()


if __name__ == "__main__":
    main()
