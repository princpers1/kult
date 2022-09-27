import telebot
from telebot import types # для указание типов
from string import Template
import config

bot = telebot.TeleBot(config.token)

user_dict={}

class User:
    def __init__(self,city):
        self.city=city
        keys = ['name','Telephon','Menu']

        for key in keys:
            self.key=None
@bot.message_handler(commands=['start'])
def menus_1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/Оплата")
    btn2 = types.KeyboardButton("/Доставка")
    btn3 = types.KeyboardButton("/Меню")
    btn4 = types.KeyboardButton("/Вернуться в главное меню")
    markup.add(btn1, btn2, btn3,btn4)
    bot.send_message(message.chat.id,
                     text="Здравствуйте,я телеграмм бот приёма ваших заказов)".format(
                         message.from_user), reply_markup=markup)

@bot.message_handler(commands=['Оплата'])
def func(message):
        bot.send_message(message.chat.id, text="Только наличными")
@bot.message_handler(commands=['Доставка'])
def func(message):
        bot.send_message(message.chat.id, text="Доставки временно нету!Самовывоз, адресс:г.Лепель ул.Войкова 124А ")
@bot.message_handler(commands=['Вернуться в главное меню'])
def func_3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Способ оплаты")
    btn2 = types.KeyboardButton("Способ доставки")
    btn3 = types.KeyboardButton("Меню")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
@bot.message_handler(commands=['Меню'])
def user_reg(message):
    mgg=bot.send_message(message.chat.id,'Напишите ваш город')
    bot.register_next_step_handler(mgg,fio_step)
def fio_step(message):
    chat_id=message.chat.id
    user_dict[chat_id]=User(message.text)

    msg=bot.send_message(message.chat.id,'Введите Фамилию Имя получателя')
    bot.register_next_step_handler(msg,phone_step)
def phone_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.name = message.text

        msg2 = bot.send_message(message.chat.id, 'Введите телефон')
        bot.register_next_step_handler(msg2, men_1)
    except Exception as e:
        bot.reply_to(message, 'oooops!!')
def men_1(message):
    try:
       int(message.text)

       chat_id=message.chat.id
       user=user_dict[chat_id]
       user.Telephon=message.text

       img = open('kult211.jpg', 'rb')
       menus = bot.send_photo(message.chat.id, photo=img,
                              caption='Напишите ,что вы хотите заказать и количество. Пример'
                                      ':шефбургер-1шт,шаурма маленькая -2шт и т.п.')
       img.close()
       bot.register_next_step_handler(menus,men_2)
    except Exception as e:
        bot.reply_to(message,'ooops!!')
def men_2(message):
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.Menu = message.text
        bot.send_message(chat_id,getRegData(user,'Ваш заказ',message.from_user.first_name),parse_mode='Markdown')

        bot.send_message(config.GR_id,getRegData(user,'Заказ от бота',bot.get_me().username),parse_mode='Markdown')
def getRegData(user,title,name):
    t =Template(f'Ваши данные \nФИО:{user.name}\nТелефон:{user.Telephon}\nЗаказ:{user.Menu}\nСпасибо за заказ!'
                f'вам перезвонят для подтверждения заказа.\nДля повторного заказа введите команду/Start')

    return t.substitute({
        'title': title,
        'name': name,
        'names': user.name,
        'phone': user.Telephon,
        'menu': user.Menu
    })
@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Спасибо"):
        bot.send_message(message.chat.id,text="И вам спасибо, за заказ!")
    elif (message.text == "Спасибо!"):
        bot.send_message(message.chat.id,text="И вам спасибо, за заказ!")
    elif (message.text == "cпасибо"):
        bot.send_message(message.chat.id,text="И вам спасибо, за заказ!")
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

if __name__ == "__main__":
    bot.polling(none_stop=True)