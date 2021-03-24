import random, telebot, json, os
import commander
commander.help_menu().AddCommand(
    '/quote', 'отправляет цитату волка'
)
commander.help_menu().AddCommand(
    '/help', 'выводит список команд'
)
d = []
def log_saver(name, text):
    updater = {
        "name":name,
        "text":text
        }
    d.append(updater)
    with open('temp/activity.json', 'w', encoding = 'utf-8') as fs:
        json.dump(d, fs, ensure_ascii=False)
while True:
    try:
        with open('static/quotes.json', 'r', encoding = 'utf-8') as f:
            quotes = json.load(f)

        token = os.environ.get('tgtoken')
        bot = telebot.TeleBot(token)
        @bot.message_handler(commands=['help'])
        def help_manager(msg):
            bot.send_sticker(msg.chat.id, open('static/helper.webp', 'rb'))
            bot.send_message(
                msg.chat.id,
                '\n\n'.join(commander.help_menu().commands)
            )
        @bot.message_handler(commands=['quote'])
        def quote_generator(msg):
            bot.send_message(msg.chat.id,
                            f"<b>Волчья цитата для тебя</b> \n<i>{quotes[random.randint(1, len(quotes)) - 1]}</i>",
                            parse_mode='html'
                            )
            bot.send_message(
                    msg.chat.id, "Нажмите на кнопку для получения новой волчьей цитаты: ",
                    reply_markup = telebot.types.InlineKeyboardMarkup().add(
                        telebot.types.InlineKeyboardButton(text = "Получить новую цитату", callback_data = 'yes')
                    )
                )
        @bot.callback_query_handler(func = lambda call: True)
        def answerCatcher(call):
            bot.delete_message(call.message.chat.id)
            bot.send_message(call.message.chat.id,
                f"<b>Волчья цитата для тебя</b> \n<i>{quotes[random.randint(1, len(quotes)) - 1]}</i>",
                parse_mode='html'
                )
        @bot.message_handler(commands=['start'])
        def welcome(msg):
            bot.send_sticker(msg.chat.id, open('static/sticker.webp', 'rb'))
            bot.send_message(msg.chat.id, f'{msg.from_user.first_name }, cам дед сан')
        @bot.message_handler(content_types=['text'])
        def main(msg):
            bot.send_message(msg.chat.id, 
            "Неизвестная команда, введите /help.")
            log_saver(
                msg.from_user.username, msg.text
            )
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
