import os
import telebot
from transforms import rotate_image, detect_face

token = os.environ['TOKEN']
bot = telebot.TeleBot(f'{token}')

def get_photo(message):   
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("telegram_bot/input_photo/image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.send_message(message.from_user.id, 'Фото получено')

def send_photo(message):
    detect_face('telegram_bot/input_photo/', 'telegram_bot/output_photo/')
    photo = open('telegram_bot/output_photo/image.jpg', 'rb')
    bot.send_photo(message.from_user.id, photo)

    bot.send_message(message.from_user.id, 'Фото отправлено')

def get_text(message):
    name = message.text
    bot.send_message(message.from_user.id, 'Сообщение получено')

@bot.message_handler(content_types=['text', 'photo'])
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Вызови /send что бы отправить фото")
    elif message.text == "/send":
        bot.send_message(message.from_user.id, "Отправляй фото")
        # bot.register_next_step_handler(message, get_text)
        bot.register_next_step_handler(message, get_photo)
        bot.register_next_step_handler(message, send_photo)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
