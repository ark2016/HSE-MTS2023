import time

import telebot
import telegram
from telebot import types
from bot_info import chat_creators,token

chat_creators=chat_creators
token=token
bot = telebot.TeleBot(token)


def make_message_markup():
    menu=types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1=types.KeyboardButton("Начать работу")
    but3 = types.KeyboardButton("Что ты можешь?")
    but2=types.KeyboardButton("Дополнительно")
    menu.add(but1)
    menu.add(but3)
    menu.add(but2)
    return menu

def da():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Да")
    but3 = types.KeyboardButton("Нет")
    menu.add(but1)
    menu.add(but3)
    return menu

def after_start():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Вернуться")
    but3 = types.KeyboardButton("Проанализировать пост")
    but2 = types.KeyboardButton("Инструкция")
    menu.add(but1)
    menu.add(but3)
    menu.add(but2)
    return menu

def post_markup():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Вернуться")
    but2 = types.KeyboardButton("Прислать пост")
    menu.add(but2)
    menu.add(but1)
    return menu

@bot.message_handler(commands=['start'],chat_types=['private'])
def start(message):
    bot.send_message(message.chat.id,"Здравствуй,"+message.from_user.first_name +"! Я Advert Bot, чат-бот команды Greedy Algoritm, чем могу помочь?", reply_markup=make_message_markup())

@bot.message_handler(commands=['help'],chat_types=['private'])
def help(message):
    bot.send_message(message.chat.id,"Очень жаль, что вы столкнулись с какой-то проблемой...\nНо вы всегда можете связаться с моими разработчиками или перезапустить меня командой /start")

global start_work
global first
global instruction
instruction="""Для начала работы с ботом вам нужно **добавить его в свою группу** и **выдать права администратора** для доступа к сообщениям. Далее предлагаю попробовать оценить успешность поста на основе анализа данных из вашего канала.

Инструкция:

Мои разработчики создали алгоритм и обучили нейронную сеть. Благодаря этому я могу спрогнозировать вероятную оценку пользователями вашего будущего поста. Составляя прогноз, я ориентируюсь на реакцию подписчиков исключительно в вашем канале. Таким образом, я подстраиваюсь под ваш канал и его аудиторию.

Для наилучших результатов необходимо:

1. **Добавить данного бота в группу**, привязанную к вашему Telegram-каналу;
2. Назначить его администратором и **разрешить чтение сообщений;**
3. **Дождаться анализа вашего канала.** По окончании процесса вы получите статистику в красивой визуализации;
4. Пользуясь полученными результатами, **продумать свой пост и отправить его боту** на анализ;
5. В результате вы получите **приблизительные данные** о количестве просмотров, комментариев и реакций на будущий пост.

**Примечание:** На данный момент каждый пользователь может привязать только одну группу с привязанным к ней каналом."""

start_work=0
first=0

@bot.message_handler(content_types=['text'],chat_types=['private'])
def text_message(message):
    if message.text.lower()=="что ты можешь?":
        text="Я помогу спрогнозировать вероятную оценку твоего будущего поста другими пользователями, которые будут его просматривать." \
             "При составлении оценки я ориентируюсь на то, как пользователи реагируют на информацию исключительно в твоем канале -" \
             "тем самым я подстраиваюсь под тебя."
        bot.send_message(message.chat.id,text)
    elif message.text.lower() == "дополнительно":
        bot.send_message(message.chat.id,"Сейчас я тебе кратко расскажу")
    elif message.text.lower()=="начать работу":
        if first==0:
            text="Прежде чем начать, хочу спросить: осведомлен ли ты о том, как я работаю?"
            msg=bot.send_message(message.chat.id,text,reply_markup=da())
            bot.register_next_step_handler(msg,da_or_net)
        else:
            text = "Выбери действие в меню"
            bot.send_message(message.chat.id, text, reply_markup=after_start())
    elif message.text.lower()=="вернуться":
        text = "Выбери действие в меню"
        bot.send_message(message.chat.id, text, reply_markup=make_message_markup())
    elif message.text.lower()=="проанализировать пост":
        text="Покажи мне, что ты хочешь скинуть"
        msg=bot.send_message(message.chat.id,text,reply_markup=post_markup())
        bot.register_next_step_handler(msg,want_post)
    elif message.text.lower() == "инструкция":
        bot.send_message(message.chat.id, instruction)

def want_post(message):
    text=message.text
    if text.lower()=="вернуться":
        text = "Выбери действие в меню"
        bot.send_message(message.chat.id, text, reply_markup=make_message_markup())
    elif text.lower()=="прислать пост":
        text1 = "Пришли пост в следующем сообщении"
        msg = bot.send_message(message.chat.id, text1, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, send_post)

def send_post(message):
    id=message.id
    bot.send_message(message.chat.id,"Я проанализировал, думаю вам понравится",reply_markup=make_message_markup())

def da_or_net(message):
    if message.content_type!='text':
        msg=bot.send_message(message.chat.id,"Пожалуйста, выбери варианты из меню",reply_markup=da())
        bot.register_next_step_handler(msg,da_or_net)
        return
    text=message.text
    if text.lower()=="да":
        global first
        first=1
        text = "Выбери действие в меню"
        bot.send_message(message.chat.id, text, reply_markup=make_message_markup())
    elif text.lower()=="нет":
        global instruction
        menu=types.ReplyKeyboardMarkup()
        menu.add(types.KeyboardButton("Так точно!"))
        bot.send_message(message.chat.id, instruction,parse_mode=telegram.ParseMode.MARKDOWN_V2,reply_markup=make_message_markup())

while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(e)
        time.sleep(5)
