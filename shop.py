import telebot
from telebot import types
from telebot.types import LabeledPrice, ShippingOption

token = 'token' # @BotFather -> /newbot
provider_token = 'Payments toekn'  # @BotFather -> Bot Settings -> Payments
bot = telebot.TeleBot(token)

prices = [LabeledPrice(label='Цена', amount=10000), LabeledPrice('Комиссия', 0)]
@bot.message_handler(commands=['start'])
def start(message):
    menu = types.ReplyKeyboardMarkup(True,False)
    menu.row('Товары')
    menu.row('О боте')
    bot.send_message(message.chat.id,'Привет , {name} \nВыберите пункт меню :.'.format(name=message.chat.first_name),reply_markup = menu)
@bot.message_handler(content_types=['text'])
def body(message):
    if message.text == 'Товары':
        bot.send_message(message.chat.id,
                         "Сейчас вы получите счет."
                         " Используйте этот номер карты : `4242 4242 4242 4242`", parse_mode='Markdown')
        bot.send_invoice(
            chat_id=message.chat.id,
            title='Тест',
            description='Вы совершите тестовую транзакцию.',
            invoice_payload='true',
            provider_token=provider_token,
            start_parameter='true',
            currency='rub',
            prices=prices
        )
    elif message.text == 'О боте':
        bot.send_message(message.chat.id,'Это бот магазин с яндекс кассой.\nХотите себе такой же?\nМожете заказать его у нас @LifeCode_Bot ')
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Что-то пошло не так."
                                                " Повторите попытку позже.")
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Вы успешно сделали транзакцию на `{} {}`! '.format(message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')
bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
