import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/AnimatedSticker.tgs', 'rb')

    bot.send_sticker(message.chat.id, sti)

    mess = "Добро пожаловать, {0.first_name}! \nЯ - <b>{1.first_name}</b>, тестовый бот, созданный специально для обучения!."

    print(message.from_user)
    print(bot.get_me())

    bot.send_message(message.chat.id, mess.format(message.from_user, bot.get_me()), parse_mode="html")
    bot.send_message(message.chat.id, "<a href='/' style='max-height: 300px; padding: 10px 5px'> TEST </a>", parse_mode="html")

@bot.message_handler(content_types=['text'])
def echo_bot(message):
    bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=True)