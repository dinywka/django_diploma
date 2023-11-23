# import telebot
#
# bot = telebot.TeleBot('6481369847:AAGh4KSCeGFhZbW0Ny041ZGP_9_ygS-Rjjk')
# ERROR_TEXT = "Произошла ошибка, попробуйте ещё раз или обратитесь к администратору"
# DEBUG = False  # TODO debug == true - идёт разработка
#
# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, "Welcome! You are now registered.")
#
# if __name__ == "__main__":
#     print("bot started...")
#     bot.infinity_polling()
# bot.py
import os
import sys
import telebot
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_settings.settings')
# application = get_wsgi_application()
# call_command('runserver', '0.0.0.0:8000')
# import django
# django.setup()


# from backend.django_app.views import send_product_list
sys.path.insert(0, 'backend/django_app/views')
# from views import send_product_list
import views
# Set up the bot
bot = telebot.TeleBot('6481369847:AAGh4KSCeGFhZbW0Ny041ZGP_9_ygS-Rjjk')

# Your existing handle_start function
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    views.send_product_list(chat_id)
    bot.send_message(chat_id, "Welcome! You are now registered.")

if __name__ == "__main__":
    print("bot started...")
    bot.infinity_polling()
