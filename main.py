from dotenv import load_dotenv
import os
import telebot
import openai

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение API ключей из переменных окружения
OPENAI_API_KEY = os.getenv('API_KEY_OPENAI')
TELEGRAM_BOT_TOKEN = os.getenv('API_KEY_TG')

# Инициализация бота и OpenAI клиента
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Отправляем запрос к модели ChatGPT
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "Вы помощник."},
                {"role": "user", "content": message.text}
            ]
        )
        # Получаем текст ответа
        reply = response['choices'][0]['message']['content']
        # Отправляем ответ пользователю
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Ошибка при обработке запроса: {str(e)}")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)