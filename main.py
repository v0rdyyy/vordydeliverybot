import telebot
from telebot import types
import telebot.apihelper

TOKEN = '6801349127:AAFhqsgCDhmj7fgnCZrO2xpk_fA6CFIGStI'
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рассчитать стоимость")
    item2 = types.KeyboardButton("Ответы на вопросы")
    item3 = types.KeyboardButton("Сделать заказ")
    markup.add(item1, item2, item3)
    return markup

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я чат-бот VORDY Delivery. Как я могу вам помочь?", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        if message.text == "Рассчитать стоимость":
            bot.send_message(message.chat.id, "Введите цену в юанях:")
            bot.register_next_step_handler(message, calculate_cost)
        elif message.text == "Ответы на вопросы":
            response_text = "Ответы на основные вопросы:\n\n<b>Q. Товар который я закажу с Poizon будет оригинальным?</b>\n<i>A. Да, товары купленные с Poizon проходят строгую проверку на оригинальность.</i>\n\n<b>Q. Как долго будет ехать товар до меня?</b>\n<i>A. Доставка со склада Китая в Москву занимает от 10-15 дней.</i>\n\n<b>Q. Товар прибыл в Москву, что дальше?</i>\n<i>A. После прибытия товара в Москву, вы оплачиваете доставку из Китая в Москву и доставку CDEK, далее товар едет вам в город ТК CDEK</i>"
            bot.send_message(message.chat.id, response_text, reply_markup=main_menu())
        elif message.text == "Сделать заказ":
            bot.send_message(message.chat.id, "Переход на аккаунт менеджера...")
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, "https://t.me/ManagerVordy", reply_markup=main_menu())
        else:
            bot.send_message(message.chat.id, "Извините, я не понимаю ваш запрос. Попробуйте еще раз.")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error: {e}")
        pass

def calculate_cost(message):
    try:
        price = float(message.text)
        total_cost = price * 13.5
        total_cost1 = total_cost + (total_cost*0.1)
        bot.send_message(message.chat.id, f"Стоимость товара: {total_cost1:.2f} рублей + стоимость доставки (зависит от способа)", reply_markup=main_menu())
        bot.register_next_step_handler(message, handle_messages)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
        bot.register_next_step_handler(message, calculate_cost)

bot.polling(none_stop=True)
