import telebot
import db_connect
import time
from functions import get_text_select_day, get_text_all_day
import db_config

faculty = 0
group_class = 0
group_name = 0
select_day = 1

bot = telebot.TeleBot('token', threaded=False)


@bot.message_handler(commands=['start'])
def start_message(message):
    state = db_connect.get_current_state(message.chat.id)
    if state == db_config.States.S_FACULTY.value:
        bot.send_message(message.chat.id, 'Необходимо выбрать факультет')
        get_faculty(message)
    elif state == db_config.States.S_GROUP_CLASS.value:
        bot.send_message(message.chat.id, 'Необходимо выбрать курс')
        get_group_class(message)
    elif state == db_config.States.S_GROUP_NAME.value:
        bot.send_message(message.chat.id, 'Необходимо выбрать группу')
        get_group_name_from_user(message)
    elif state == db_config.States.S_START.value:
        db_connect.create_state(message.chat.id, db_config.States.S_FACULTY.value)
        bot.send_message(message.chat.id, 'Привет')
        get_faculty(message)


@bot.message_handler(commands=['restart'])
def restart_message(message):
    global select_day
    select_day = 1
    db_connect.update_state(message.chat.id, db_config.States.S_FACULTY.value)
    bot.send_message(message.chat.id, "Привет, снова")
    get_faculty(message)


@bot.message_handler(commands=['allsh'])
def send_all_schedule(message):
    global faculty, group_class, group_name
    for week in get_text_all_day(faculty, group_class, group_name):
        all_schedule_text = '\n---------------\n'.join(list(map(lambda x: '\n'.join(x), week)))
        bot.send_message(message.chat.id, text=all_schedule_text)


@bot.message_handler(
    func=lambda message: db_connect.get_current_state(message.chat.id) == db_config.States.S_FACULTY.value)
def get_faculty(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_aki = telebot.types.InlineKeyboardButton(text='АКИ', callback_data='facultАКИ')
    keyboard.add(key_aki)
    key_asf = telebot.types.InlineKeyboardButton(text='АСФ', callback_data='facultАСФ')
    keyboard.add(key_asf)
    key_vuts = telebot.types.InlineKeyboardButton(text='ВУЦ ОГУ', callback_data='facultВУЦ ОГУ')
    keyboard.add(key_vuts)
    key_imit = telebot.types.InlineKeyboardButton(text='ИМИТ', callback_data='facultИМИТ')
    keyboard.add(key_imit)
    key_imep = telebot.types.InlineKeyboardButton(text='ИМЭП', callback_data='facultИМЭП')
    keyboard.add(key_imep)
    key_inpo = telebot.types.InlineKeyboardButton(text='ИНПО', callback_data='facultИНПО')
    keyboard.add(key_inpo)
    key_inoz = telebot.types.InlineKeyboardButton(text='ИНоЗем', callback_data='facultИНоЗем')
    keyboard.add(key_inoz)
    key_isgn = telebot.types.InlineKeyboardButton(text='ИСГН', callback_data='facultИСГН')
    keyboard.add(key_isgn)
    key_iees = telebot.types.InlineKeyboardButton(text='ИЭЭС', callback_data='facultИЭЭС')
    keyboard.add(key_iees)
    key_iyak = telebot.types.InlineKeyboardButton(text='ИЯК', callback_data='facultИЯК')
    keyboard.add(key_iyak)
    key_tf = telebot.types.InlineKeyboardButton(text='ТФ', callback_data='facultТФ')
    keyboard.add(key_tf)
    key_fpbi = telebot.types.InlineKeyboardButton(text='ФПБИ', callback_data='facultФПБИ')
    keyboard.add(key_fpbi)
    key_fizf = telebot.types.InlineKeyboardButton(text='ФизФ', callback_data='facultФизФ')
    keyboard.add(key_fizf)
    key_hbf = telebot.types.InlineKeyboardButton(text='ХБФ', callback_data='facultХБФ')
    keyboard.add(key_hbf)
    key_uf = telebot.types.InlineKeyboardButton(text='ЮФ', callback_data='facultЮФ')
    keyboard.add(key_uf)
    bot.send_message(message.chat.id, text='Выбери свой факультет:', reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: db_connect.get_current_state(message.chat.id) == db_config.States.S_GROUP_CLASS.value)
def get_group_class(message):
    global group_class
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(1, 6):
        keyboard.add(telebot.types.InlineKeyboardButton(text=str(i), callback_data=f'gr_class{i}'))
    bot.send_message(message.chat.id, text='Твой курс:', reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: db_connect.get_current_state(message.chat.id) == db_config.States.S_GROUP_NAME.value)
def get_group_name_from_user(message):
    global group_class, faculty
    keyboard = telebot.types.InlineKeyboardMarkup()
    group_names = db_connect.get_group_name_from_db(faculty, group_class)
    for i in range(len(group_names)):
        keyboard.add(telebot.types.InlineKeyboardButton(text=f'{group_names[i][0]}',
                                                        callback_data=f'gr_name{group_names[i][0]}'))
    bot.send_message(message.chat.id, text='Выбери свою группу:', reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: db_connect.get_current_state(message.chat.id) == db_config.States.S_SCHEDULE.value)
def send_schedule(message):
    global faculty, group_class, group_name, select_day

    start_markup = telebot.types.InlineKeyboardMarkup()
    button_right = telebot.types.InlineKeyboardButton('->', callback_data='next')
    button_left = telebot.types.InlineKeyboardButton('<-', callback_data='prev')
    start_markup.row(button_left, button_right)
    bot.send_message(message.chat.id, text='\n'.join(get_text_select_day(faculty, group_class, group_name, select_day)),
                     reply_markup=start_markup)


@bot.callback_query_handler(func=lambda call: call.data[:6] == 'facult')
def callback_faculty(call):
    global faculty
    faculty = call.data[6:]
    db_connect.update_state(call.message.chat.id, db_config.States.S_GROUP_CLASS.value)
    get_group_class(call.message)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == 'gr_class')
def callback_group_class(call):
    global group_name, faculty, group_class
    group_class = call.data[-1]
    db_connect.update_state(call.message.chat.id, db_config.States.S_GROUP_NAME.value)
    get_group_name_from_user(call.message)


@bot.callback_query_handler(func=lambda call: call.data[:7] == 'gr_name')
def callback_group_name(call):
    global group_name, faculty, group_class
    group_name = call.data[7:]
    db_connect.update_state(call.message.chat.id, db_config.States.S_SCHEDULE.value)
    send_schedule(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'next')
def callback_next_day(call):
    global faculty, group_class, group_name, select_day
    if get_text_select_day(faculty, group_class, group_name, select_day)[0][11:-1] != 'суббота':
        select_day += 1
        start_markup = telebot.types.InlineKeyboardMarkup()
        button_right = telebot.types.InlineKeyboardButton('->', callback_data='next')
        button_left = telebot.types.InlineKeyboardButton('<-', callback_data='prev')
        start_markup.row(button_left, button_right)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='\n'.join(get_text_select_day(faculty, group_class, group_name, select_day)),
                              reply_markup=start_markup)
    else:
        bot.send_message(call.message.chat.id, text='Нет расписания на выбранную дату')


@bot.callback_query_handler(func=lambda call: call.data == 'prev')
def callback_prev_day(call):
    global faculty, group_class, group_name, select_day
    if get_text_select_day(faculty, group_class, group_name, select_day)[0][11:-1] != 'понедельник' and select_day >= 2:
        get_text_select_day(faculty, group_class, group_name, select_day)
        select_day -= 1
        start_markup = telebot.types.InlineKeyboardMarkup()
        button_right = telebot.types.InlineKeyboardButton('->', callback_data='next')
        button_left = telebot.types.InlineKeyboardButton('<-', callback_data='prev')
        start_markup.row(button_left, button_right)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='\n'.join(get_text_select_day(faculty, group_class, group_name, select_day)),
                              reply_markup=start_markup)
    else:
        bot.send_message(call.message.chat.id, 'Нет расписания на выбранную дату')


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(10)
