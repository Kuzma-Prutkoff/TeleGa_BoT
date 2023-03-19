import telebot
from config import my_keys, TOKEN
from TeleGa_BoT.classes import ConvertionException, CryptoConvertor


bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = '1)Правила ввода команд БОТУ в формате:\n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>. \
\n<2)Увидеть все доступные пары валют можно командой: /values >' # /values это еще и гиперссылка
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'доступные валюты:'
    for key in my_keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:                                        # блок о том а если ошибка от сервера или от юзера
        values = message.text.split(' ')
        if len(values) != 3:  # искл - неправильное количество введенных значений
            raise ConvertionException('неверное количество  параметров, а надо 3')
        crypto, currency, amount = values  # строка ввода пользователя типа: биток бакс 1. Надо сначала распарсить сообщение от юзера
        crypto_price = CryptoConvertor.convertor_exception(crypto, currency, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'ошибка ввода пользователя. \n{e}')
    except Exception as e:                           # любая ошибка кроме ошибок от ручного ввода юзера
        bot.reply_to(message, f'не удалось обработать команду. \n{e}')
    else:
        text = f'Цена {amount} {crypto} = {float(crypto_price)*int(amount)} {currency}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)


