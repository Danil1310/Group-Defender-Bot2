import telebot
import sqlite3 
from telebot import types
from time import time
bot = telebot.TeleBot('8241607493:AAEAf0mObVBxoV94Z8Ozmlewb6p5cKs1wlw')
import datetime as dt
import random
from datetime import timedelta
from telebot.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
ansnwers = ["Да", "Нет", "Затрудняюсь ответить"]
restricted_messages = set()
restricted_messages_text = None
restricted_flag = True
clear_flag = False
spam_flag = False
call_flag = False
date_flag = False
list_add_flag = False
list_del_flag = False
ban_flag = False
message_id = None
message_id2 = None
last_word = None
spam_flag_text = 0
count = 0
date = 900
call_admins_text = "Нету"
call_admins = []
all_messages_count = 0
bot_messages_count = 0
commands_messages_count = 0
other_messages_count = 0
user_all_messages_count = 0
user_commands_messages_count = 0
user_mute_count = 0
ban_count = 0
mute_count = 0
user_warn_count = 0
commands_list = ["/start@groups_defender_bot",  "/info@groups_defender_bot", "/ban@groups_defender_bot", "/unban@groups_defender_bot", "/mute@groups_defender_bot", "/unmute@groups_defender_bot", "/list_view@groups_defender_bot", "/spam_on@groups_defender_bot", "/spam_off@groups_defender_bot", "/cancel@groups_defender_bot", "/clear@groups_defender_bot", "/start_clear@groups_defender_bot", "/settings@groups_defender_bot", "/call@groups_defender_bot"]
connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups1 (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    list_words TEXT, 
    spam_flags BOOLEAN NOT NULL,
    clear_flags BOOLEAN NOT NULL,
    call_admins TEXT NOT NULL,
    mute_time INTEGER NOT NULL          
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups2 (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    all_messages_count INTEGER NOT NULL, 
    bot_messages_count INTEGER NOT NULL,
    other_messages_count INTEGER NOT NULL,
    commands_messages_count INTEGER NOT NULL,
    ban_count INTEGER NOT NULL,
    mute_count INTEGER NOT NULL          
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups3 (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    user_all_messages_count INTEGER NOT NULL, 
    user_commands_messages_count INTEGER NOT NULL,
    user_mute_count INTEGER NOT NULL 
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups4 (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    user_warn_count INTEGER NOT NULL
    )
''')
connect.commit()
connect.close()

@bot.message_handler(commands=['start'])
def info(message):
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global clear_flag
    chat_id = message.chat.id
    user_id = message.from_user.id
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups1 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        list_words TEXT, 
        spam_flags BOOLEAN NOT NULL,
        clear_flags BOOLEAN NOT NULL,
        call_admins TEXT NOT NULL,
        mute_time INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups2 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        all_messages_count INTEGER NOT NULL, 
        bot_messages_count INTEGER NOT NULL,
        other_messages_count INTEGER NOT NULL,
        commands_messages_count INTEGER NOT NULL,
        ban_count INTEGER NOT NULL,
        mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups3 (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        user_all_messages_count INTEGER NOT NULL, 
        user_commands_messages_count INTEGER NOT NULL,
        user_mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups4 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        user_warn_count INTEGER NOT NULL
        )
    ''')
    cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    all_messages_count = cursor.fetchone()
    if all_messages_count is not None:
        all_messages_count = all_messages_count[0]
    else:
        all_messages_count = 0
    cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    bot_messages_count = cursor.fetchone()
    if bot_messages_count is not None:
        bot_messages_count = bot_messages_count[0]
    else:
        bot_messages_count = 0
    cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    commands_messages_count = cursor.fetchone()
    if commands_messages_count is not None:
        commands_messages_count = commands_messages_count[0]
    else:
        commands_messages_count = 0
    cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    other_messages_count = cursor.fetchone()
    if other_messages_count is not None:
        other_messages_count = other_messages_count[0]
    else:
        other_messages_count = 0
    cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    ban_count = cursor.fetchone()
    if ban_count is not None:
        ban_count = ban_count[0]
    else:
        ban_count = 0
    cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    mute_count = cursor.fetchone()
    if mute_count is not None:
        mute_count = mute_count[0]
    else:
        mute_count = 0
    all_messages_count += 1
    other_messages_count += 1
    commands_messages_count += 1
    query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
    connect.commit()
    cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
    user_all_messages_count = cursor.fetchone()
    if user_all_messages_count is not None:
        user_all_messages_count = user_all_messages_count[0]
    else:
        user_all_messages_count = 0
    cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
    user_commands_messages_count = cursor.fetchone()
    if user_commands_messages_count is not None:
        user_commands_messages_count = user_commands_messages_count[0]
    else:
        user_commands_messages_count = 0
    cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
    user_mute_count = cursor.fetchone()
    if user_mute_count is not None:
        user_mute_count = user_mute_count[0]
    else:
        user_mute_count = 0
    connect.commit()
    user_commands_messages_count += 1
    user_all_messages_count += 1
    query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
    cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
    connect.commit()
    markup = types.InlineKeyboardMarkup(row_width=1)
    add_to_chat_url = f"https://t.me/groups_defender_bot?startgroup=True&admin=change_info+restrict_members+delete_messages+pin_messages+invite_users"
    invite_button = types.InlineKeyboardButton(text="Добавить бота в группу", url=add_to_chat_url)
    list_button = types.InlineKeyboardButton(text="Открыть список команд", url="https://teletype.in/@groups_defender_bot/commands")
    support_button = types.InlineKeyboardButton(text="Связаться с поддержкой", url="https://t.me/sup_groups_defender_bot")
    markup.add(invite_button, list_button, support_button)
    bot.send_message(message.chat.id, f"Приветствую!\nДля того, чтобы начать работу, добавьте меня в группу.\nТакже рекомендую прочитать подробный список команд, чтобы разобраться с ними.\n\n<i>ВНИМАНИЕ! Чтобы ваш бот отвечал на административные команды других пользователей, вы должны сделать их администраторами(также не забудьте сделать самого бота администратором и дать ему все права, чтобы все команды работали).</i>", parse_mode="HTML", reply_markup=markup)
    bot_messages_count += 1
    all_messages_count += 1
    query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
    connect.commit()
    connect.close()

@bot.message_handler(commands=['info'])
def info(message):
    global clear_flag
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    chat_id = message.chat.id 
    slovo = message.text
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        try:
            user_to_info = message.reply_to_message.from_user.id
            user_username = message.reply_to_message.from_user.username
            cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_to_info, chat_id,))
            user_all_messages_count = cursor.fetchone()
            if user_all_messages_count is not None:
                user_all_messages_count = user_all_messages_count[0]
            else:
                user_all_messages_count = 0
            cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_to_info, chat_id,))
            user_commands_messages_count = cursor.fetchone()
            if user_commands_messages_count is not None:
                user_commands_messages_count = user_commands_messages_count[0]
            else:
                user_commands_messages_count = 0
            cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_to_info, chat_id,))
            user_mute_count = cursor.fetchone()
            if user_mute_count is not None:
                user_mute_count = user_mute_count[0]
            else:
                user_mute_count = 0
            connect.commit()
            cursor.execute('SELECT user_warn_count FROM groups4 WHERE user_id = ? and group_id = ? ORDER BY id DESC', (user_to_info, chat_id,))
            user_warn_count = cursor.fetchone()
            if user_warn_count is not None:
                user_warn_count = user_warn_count[0]
            else:
                user_warn_count = 0
            user_all_messages_count += 1
            user_commands_messages_count += 1
            bot.reply_to(message, f"<b>Информация о пользователе </b>@{user_username}:\n<b>Всего сообщений: </b>{user_all_messages_count}.\n<b>Взаимодействий с ботом: </b>{user_commands_messages_count}.\n<b>Количество мутов: </b>{user_mute_count}.\n<b>Количество предупреждений: </b>{user_warn_count}/3.", parse_mode='HTML') 
            bot_messages_count += 1
            all_messages_count += 1
        except:
            bot.reply_to(message, f"Не удалось получить информацию о пользователе @{user_username}. Проверьте синтаксис команды.")
            bot_messages_count += 1 
            all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()

@bot.message_handler(commands=['ban']) 
def ban_user(message): 
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global ban_flag
    global clear_flag
    slovo = message.text
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        chat_id = message.chat.id 
        user_id = message.from_user.id 
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if is_user_admin(chat_id, user_id): 
            user_username = message.reply_to_message.from_user.username 
            user_to_ban = message.reply_to_message.from_user.id 
            try: 
                message_list = slovo.split()
                reason = message_list[1::]
                bot.ban_chat_member(chat_id, user_to_ban) 
                ban_count += 1
                query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
                connect.commit()
                bot.reply_to(message, f"Пользователь @{user_username} забанен.\nПричина: {' '.join(reason)}.")
                all_messages_count += 1 
                bot_messages_count += 1
            except: 
                bot.reply_to(message, f"Не удалось забанить пользователя @{user_username}. Синтаксис команды: /ban + причина бана.") 
                all_messages_count += 1
                bot_messages_count += 1
        else: 
            bot.reply_to(message, "У вас нет прав для этой команды.")
            all_messages_count += 1
            bot_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()

@bot.message_handler(commands=['unban']) 
def unban_user(message): 
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global ban_flag
    global clear_flag
    slovo = message.text
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        chat_id = message.chat.id 
        user_id = message.from_user.id
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit() 
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if is_user_admin(chat_id, user_id): 
            user_username = message.reply_to_message.from_user.username
            user_to_unban = message.reply_to_message.from_user.id
            try: 
                bot.unban_chat_member(chat_id, user_to_unban) 
                bot.reply_to(message, f"Пользователь @{user_username} разбанен.") 
                bot_messages_count += 1
                all_messages_count += 1
            except: 
                bot.reply_to(message, f"Не удалось разбанить пользователя @{user_username}.") 
                bot_messages_count += 1
                all_messages_count += 1
        else: 
            bot.reply_to(message, "У вас нет прав для этой команды.") 
            bot_messages_count += 1
            all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()

@bot.message_handler(commands=['mute'])
def list_mute(message):
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global clear_flag
    slovo = message.text
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        chat_id = message.chat.id 
        user_id = message.from_user.id  
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if is_user_admin(chat_id, user_id): 
            user_username = message.reply_to_message.from_user.username
            try: 
                message_list = slovo.split()
                date = int(message_list[1])
                reason = message_list[2::]
                date1 = dt.timedelta(seconds=date) 
                date2 = dt.datetime.now() + date1
                date3 = date2.strftime("%d-%m-%Y %H:%M:%S")
                user_to_mute = message.reply_to_message.from_user.id 
                bot.restrict_chat_member(chat_id, user_to_mute, until_date=dt.datetime.now()+date1)
                mute_count += 1
                query = """INSERT INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
                connect.commit()
                cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_to_mute, chat_id,))
                user_all_messages_count = cursor.fetchone()
                if user_all_messages_count is not None:
                    user_all_messages_count = user_all_messages_count[0]
                else:
                    user_all_messages_count = 0
                cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_to_mute, chat_id,))
                user_commands_messages_count = cursor.fetchone()
                if user_commands_messages_count is not None:
                    user_commands_messages_count = user_commands_messages_count[0]
                else:
                    user_commands_messages_count = 0
                cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_to_mute, chat_id,))
                user_mute_count = cursor.fetchone()
                if user_mute_count is not None:
                    user_mute_count = user_mute_count[0]
                else:
                    user_mute_count = 0
                connect.commit()
                user_mute_count += 1
                query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
                cursor.execute(query, (chat_id, user_to_mute, user_all_messages_count, user_commands_messages_count, user_mute_count))
                connect.commit()
                if date > 30 and date < 31622400:
                    bot.reply_to(message, f"Пользователь @{user_username} замучен до {date3}.\nПричина: {' '.join(reason)}.")
                    bot_messages_count += 1
                    all_messages_count += 1
                else:
                    bot.reply_to(message, f"Пользователь @{user_username} замучен навсегда.")
                    bot_messages_count += 1
                    all_messages_count += 1
            except: 
                bot.reply_to(message, "Не удалось замутить пользователя. Синтаксис команды: /mute + время мута + причина мута.") 
                bot_messages_count += 1
                all_messages_count += 1
        else: 
            bot.reply_to(message, "У вас нет прав для этой команды.") 
            bot_messages_count += 1
            all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()
    
@bot.message_handler(commands=['unmute'])
def list_unmute(message):
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global clear_flag
    global user_mute_count
    slovo = message.text
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo: 
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        chat_id = message.chat.id 
        user_id = message.from_user.id  
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if is_user_admin(chat_id, user_id): 
            user_username = message.reply_to_message.from_user.username
            user_to_unmute = message.reply_to_message.from_user.id 
            try: 
                bot.restrict_chat_member(chat_id, user_to_unmute, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
                bot.reply_to(message, f"Пользователь @{user_username} размучен.")
                bot_messages_count += 1
                all_messages_count += 1
            except: 
                bot.reply_to(message, f"Не удалось размутить пользователя @{user_username}.")
                bot_messages_count += 1 
                all_messages_count += 1
        else: 
            bot.reply_to(message, "У вас нет прав для этой команды.") 
            bot_messages_count += 1
            all_messages_count += 1
            query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
            cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
            connect.commit()
            connect.close()

def is_user_admin(chat_id, user_id): 
    chat_member = bot.get_chat_member(chat_id, user_id) 
    return chat_member.status == "administrator" or chat_member.status == "creator" 

@bot.message_handler(commands=['list_view'])
def list_view(message):
    global message_id2
    global cursor
    global restricted_messages
    global restricted_messages_text
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global clear_flag
    slovo = message.text
    chat_id = message.chat.id
    user_id = message.from_user.id
    if clear_flag == True:
        bot.eete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        cursor.execute('SELECT list_words FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        words = cursor.fetchone()
        if words is not None:
            restricted_messages = set(words)
            if not "None" in str(restricted_messages):
                restricted_messages_text = ", ".join(restricted_messages)
            else:
                restricted_messages_text = None
                restricted_messages.clear()
        else:
            restricted_messages = set()
        connect.commit()
        markup = types.InlineKeyboardMarkup(row_width=1)
        callback_button1 = types.InlineKeyboardButton("Добавить слово", callback_data="list_add")
        callback_button2 = types.InlineKeyboardButton("Удалить слово", callback_data="list_del")
        callback_button3 = types.InlineKeyboardButton("Очистить список", callback_data="list_del_all")
        markup.add(callback_button1, callback_button2, callback_button3)
        if len(restricted_messages) >= 1 and not "None" in str(restricted_messages):
            msg = bot.send_message(message.chat.id, f"Список текущих запрещенных слов: {restricted_messages_text}.", reply_markup=markup)
            bot_messages_count += 1
            all_messages_count += 1
            message_id2 = msg.message_id
        else:
            msg = bot.send_message(message.chat.id, f"В списке отсутствуют слова.", reply_markup=markup)
            bot_messages_count += 1
            all_messages_count += 1
            message_id2 = msg.message_id
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()

@bot.callback_query_handler(func=lambda call: call.data == 'list_add')
def save_btn(call):
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global list_add_flag
    global message_id2
    list_add_flag = True
    message = call.message
    chat_id = message.chat.id
    user_id = message.from_user.id
    connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups1 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        list_words TEXT, 
        spam_flags BOOLEAN NOT NULL,
        clear_flags BOOLEAN NOT NULL,
        call_admins TEXT NOT NULL,
        mute_time INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups2 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        all_messages_count INTEGER NOT NULL, 
        bot_messages_count INTEGER NOT NULL,
        other_messages_count INTEGER NOT NULL,
        commands_messages_count INTEGER NOT NULL,
        ban_count INTEGER NOT NULL,
        mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups3 (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        user_all_messages_count INTEGER NOT NULL, 
        user_commands_messages_count INTEGER NOT NULL,
        user_mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups4 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        user_warn_count INTEGER NOT NULL
        )
    ''')
    if is_user_admin(chat_id, user_id): 
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id2, text=f'Введите слово, которое вы хотите добавить.')
        bot_messages_count += 1
        all_messages_count += 1
    else: 
        bot.reply_to(message, "У вас нет прав для этой команды.")
        bot_messages_count += 1
        all_messages_count += 1
    query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
    connect.commit()
    connect.close()

@bot.callback_query_handler(func=lambda call: call.data == 'list_del')
def save_btn(call):
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global list_del_flag
    global restricted_flag
    global message_id2
    list_del_flag = True
    restricted_flag = False
    message = call.message
    chat_id = message.chat.id
    user_id = message.from_user.id
    connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups1 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        list_words TEXT, 
        spam_flags BOOLEAN NOT NULL,
        clear_flags BOOLEAN NOT NULL,
        call_admins TEXT NOT NULL,
        mute_time INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups2 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        all_messages_count INTEGER NOT NULL, 
        bot_messages_count INTEGER NOT NULL,
        other_messages_count INTEGER NOT NULL,
        commands_messages_count INTEGER NOT NULL,
        ban_count INTEGER NOT NULL,
        mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups3 (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        user_all_messages_count INTEGER NOT NULL, 
        user_commands_messages_count INTEGER NOT NULL,
        user_mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups4 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        user_warn_count INTEGER NOT NULL
        )
    ''')
    if is_user_admin(chat_id, user_id): 
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id2, text=f'Введите слово, которое вы хотите удалить.')
        bot_messages_count += 1
        all_messages_count += 1
    else: 
        bot.reply_to(message, "У вас нет прав для этой команды.")
        bot_messages_count += 1
        all_messages_count += 1
    query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
    connect.commit()
    connect.close()

@bot.callback_query_handler(func=lambda call: call.data == 'list_del_all')
def save_btn(call):
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    message = call.message
    chat_id = message.chat.id 
    user_id = message.from_user.id
    connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups1 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        list_words TEXT, 
        spam_flags BOOLEAN NOT NULL,
        clear_flags BOOLEAN NOT NULL,
        call_admins TEXT NOT NULL,
        mute_time INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups2 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        all_messages_count INTEGER NOT NULL, 
        bot_messages_count INTEGER NOT NULL,
        other_messages_count INTEGER NOT NULL,
        commands_messages_count INTEGER NOT NULL,
        ban_count INTEGER NOT NULL,
        mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups3 (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        user_all_messages_count INTEGER NOT NULL, 
        user_commands_messages_count INTEGER NOT NULL,
        user_mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups4 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        user_warn_count INTEGER NOT NULL
        )
    ''')
    if is_user_admin(chat_id, user_id):
        restricted_messages.clear()
        restricted_messages_text = None
        cursor.execute('''INSERT OR REPLACE INTO groups1 (group_id, list_words, spam_flags, clear_flags, call_admins, mute_time) VALUES(?, ?, ?, ?, ?, ?)''', (chat_id, restricted_messages_text, spam_flag, clear_flag, call_admins_text, date))
        connect.commit()
        bot.send_message(message.chat.id, f"Список запрещенных слов успешно очищен.")
        bot_messages_count += 1
        all_messages_count += 1
    else:
        bot.send_message(message.chat.id, f"У вас нет прав для этой команды.") 
        all_messages_count += 1
        bot_messages_count += 1
    query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
    connect.commit()
    connect.close()

@bot.message_handler(commands=['server_clear_mode'])
def clear_text_messages(message):
    global clear_flag
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    slovo = message.text
    chat_id = message.chat.id 
    user_id = message.from_user.id
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if is_user_admin(chat_id, user_id):
            bot.send_message(message.chat.id, f"<b>ВНИМАНИЕ! Данная команда будет АВТОМАТИЧЕСКИ УДАЛЯТЬ ВСЕ НОВЫЕ СООБЩЕНИЯ УЧАСТНИКОВ СЕРВЕРА.</b>\n\nВведите /start_clear, чтобы запустить программу.", parse_mode="HTML")
            bot_messages_count += 1
            all_messages_count += 1
        else: 
            bot.reply_to(message, "У вас нет прав для этой команды.")
            all_messages_count += 1
            bot_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()

@bot.message_handler(commands=['start_clear'])
def delete_text_messages(message):
    global start
    global clear_flag 
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    slovo = message.text
    chat_id = message.chat.id 
    user_id = message.from_user.id
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if is_user_admin(chat_id, user_id):
            start = 1
            clear_flag = True
            bot.send_message(message.chat.id, f"Запущен процесс автоматического удаления сообщений.\nДля остановки используй команду /cancel.")
            bot_messages_count += 1
            all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()

@bot.message_handler(commands=['cancel'])
def cancel(message):
    global start
    global clear_flag
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    slovo = message.text
    chat_id = message.chat.id 
    user_id = message.from_user.id
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if is_user_admin(chat_id, user_id):
            clear_flag = False
            start = 0
            bot.send_message(message.chat.id, f"Команда отменена.")
            bot_messages_count += 1
            all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()

@bot.message_handler(commands=['spam_on'])
def spam_on(message):
    global clear_flag
    global spam_flag
    global restricted_messages_text
    global call_admins_text
    global date
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    slovo = message.text
    chat_id = message.chat.id
    user_id = message.from_user.id
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return     
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if is_user_admin(chat_id, user_id):
            spam_flag = True
            cursor.execute('SELECT mute_time FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            date = cursor.fetchone()
            if date is not None:
                date = int(date[0])
            else:
                date = 900
            cursor.execute('SELECT call_admins FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            call_admins = cursor.fetchone()
            if call_admins is not None and not "Нету" in call_admins:
                call_admins = call_admins
                call_admins_text = ", ".join(call_admins)
            else:
                call_admins = []
                call_admins_text = "Нету"
            cursor.execute('SELECT list_words FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            words = cursor.fetchone()
            if words is not None:
                restricted_messages = set(words)
                if not "None" in str(restricted_messages):
                    restricted_messages_text = ", ".join(restricted_messages)
                else:
                    restricted_messages_text = None
                    restricted_messages.clear()
            else:
                restricted_messages = set()
            cursor.execute('''INSERT OR REPLACE INTO groups1 (group_id, list_words, spam_flags, clear_flags, call_admins, mute_time) VALUES(?, ?, ?, ?, ?, ?)''', (chat_id, restricted_messages_text, spam_flag, clear_flag, call_admins_text, date))
            bot.send_message(message.chat.id, f"Включен спам фильтр.")
            bot_messages_count += 1
            all_messages_count += 1
            connect.commit()
        else: 
            bot.reply_to(message, "У вас нет прав для этой команды.")
            bot_messages_count += 1
            all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()

@bot.message_handler(commands=['spam_off'])
def spam_on(message):
    global clear_flag
    global spam_flag
    global restricted_messages_text
    global call_admins_text
    global date
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    user_id = message.from_user.id
    slovo = message.text
    chat_id = message.chat.id     
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        commands_messages_count += 1
        other_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if is_user_admin(chat_id, user_id):
            spam_flag = False
            cursor.execute('SELECT mute_time FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            date = cursor.fetchone()
            if date is not None:
                date = int(date[0])
            else:
                date = 900
            cursor.execute('SELECT call_admins FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            call_admins = cursor.fetchone()
            if call_admins is not None and not "Нету" in call_admins:
                call_admins = call_admins
                call_admins_text = ", ".join(call_admins)
            else:
                call_admins = []
                call_admins_text = "Нету"
            cursor.execute('SELECT list_words FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            words = cursor.fetchone()
            if words is not None:
                restricted_messages = set(words)
                if not "None" in str(restricted_messages):
                    restricted_messages_text = ", ".join(restricted_messages)
                else:
                    restricted_messages_text = None
                    restricted_messages.clear()
            else:
                restricted_messages = set()
            cursor.execute('''INSERT OR REPLACE INTO groups1 (group_id, list_words, spam_flags, clear_flags, call_admins, mute_time) VALUES(?, ?, ?, ?, ?, ?)''', (chat_id, restricted_messages_text, spam_flag, clear_flag, call_admins_text, date))
            bot.send_message(message.chat.id, f"Спам фильтр выключен.")
            bot_messages_count += 1
            all_messages_count += 1
            connect.commit()
        else: 
            bot.reply_to(message, "У вас нет прав для этой команды.")
            bot_messages_count += 1
            all_messages_count += 1
            query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
            cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
            connect.commit()
            connect.close()

@bot.message_handler(commands=['call'])
def call_admins_function(message):
    global call_admins
    global call_admins_text
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global clear_flag
    chat_id = message.chat.id 
    user_id = message.from_user.id
    user_name = message.from_user.username
    slovo = message.text
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if len(call_admins) != 0:
            cursor.execute('SELECT call_admins FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            call_admins = cursor.fetchone()
            if not "Нету" in call_admins[0]:
                call_admins = call_admins
                call_admins_text = ", ".join(call_admins)
            else:
                call_admins = []
                call_admins_text = "Нету"
            connect.commit()
            bot.send_message(message.chat.id, f"{call_admins_text}, вас вызывает @{user_name}.")
            bot_messages_count += 1
            all_messages_count += 1
        else:
            bot.send_message(message.chat.id, f"В чате нету агентов поддержки")
            bot_messages_count += 1
            all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()
        
@bot.message_handler(commands=['delete'])
def delete_messages(message):
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global clear_flag
    chat_id = message.chat.id 
    user_id = message.from_user.id
    user_name = message.from_user.username
    slovo = message.text
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        try:
            count = int(message.text.split()[1])
            if count <= 0:
                bot.reply_to(message, "Пожалуйста, укажите положительное число.")
                bot_messages_count += 1
                all_messages_count += 1
                return
            chat_id = message.chat.id
            message_id = message.reply_to_message.id
            for i in range(count):
                bot.delete_message(chat_id, message_id - i - 1)
            bot.reply_to(message, f'Удалено {count} сообщений.')
            bot_messages_count += 1
            all_messages_count += 1
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте команду в формате: /delete + число.")
            bot_messages_count += 1
            all_messages_count += 1
        except telebot.apihelper.ApiException as e:
            bot.reply_to(message, f"Ошибка при удалении сообщений.")
            bot_messages_count += 1
            all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()

@bot.message_handler(commands=['warn'])
def warn_function(message):
    global call_admins
    global call_admins_text
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global clear_flag
    user_id = message.from_user.id
    chat_id = message.chat.id 
    slovo = message.text
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if is_user_admin(chat_id, user_id):
            try:
                message_list = slovo.split()
                count = int(message_list[1])
                warn_reason = message_list[2::]
                if count <= 0 and count > 3:
                    bot.reply_to(message, "Пожалуйста, укажите число, которое больше 0 и меньше 4.")
                    bot_messages_count += 1
                    all_messages_count += 1
                    return
                if count == 1:
                    text = "предупреждение"
                else:
                    text = "предупреждения"
                user_to_info = message.reply_to_message.from_user.id
                user_username = message.reply_to_message.from_user.username
                cursor.execute('SELECT user_warn_count FROM groups4 WHERE user_id = ? and group_id = ? ORDER BY id DESC', (user_to_info, chat_id,))
                user_warn_count = cursor.fetchone()
                if user_warn_count is not None:
                    user_warn_count = user_warn_count[0]
                else:
                    user_warn_count = 0
                connect.commit()
                user_warn_count += count
                bot.reply_to(message, f"Пользователю @{user_username} было выдано {count} {text}.\nПричина: {' '.join(warn_reason)}.\nОбщее количество предупреждений: {user_warn_count}.")
                bot_messages_count += 1
                all_messages_count += 1
                query = """INSERT OR REPLACE INTO groups4 (group_id, user_id, user_warn_count) VALUES(?, ?, ?);"""
                cursor.execute(query, (chat_id, user_to_info, user_warn_count))
                connect.commit()
                if user_warn_count == 3:
                    try: 
                        bot.ban_chat_member(chat_id, user_to_info) 
                        ban_count += 1
                        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
                        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
                        connect.commit()
                        user_warn_count = 0
                        query = """INSERT OR REPLACE INTO groups4 (group_id, user_id, user_warn_count) VALUES(?, ?, ?);"""
                        cursor.execute(query, (chat_id, user_to_info, user_warn_count))
                        connect.commit()
                        bot.reply_to(message, f"Пользователь @{user_username} забанен.\nПричина: пользователь получил 3 предупреждения.")
                        all_messages_count += 1 
                        bot_messages_count += 1
                    except: 
                        bot.reply_to(message, f"Не удалось забанить пользователя @{user_username}. Синтаксис команды: /ban + причина бана.") 
                        all_messages_count += 1
                        bot_messages_count += 1
            except (IndexError, ValueError):
                bot.reply_to(message, "Используйте команду в формате: /warn + кол-во предупреждений(макс. 3) + причина.")
                bot_messages_count += 1
                all_messages_count += 1
            except telebot.apihelper.ApiException as e:
                bot.reply_to(message, f"Произошла ошибка при использовании команды. Возможно проблема в синтаксисе - правильный синтаксис: /warn + ответ на сообщение челоевка, которому хотите выдать предупреждение + кол-во предупреждений(макс. 3) + причина.")
                bot_messages_count += 1
                all_messages_count += 1
        else: 
            bot.reply_to(message, "У вас нет прав для этой команды.")
            all_messages_count += 1
            bot_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()

@bot.message_handler(commands=['warn_remove'])
def warn_remove_function(message):
    global call_admins
    global call_admins_text
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global clear_flag
    user_id = message.from_user.id
    chat_id = message.chat.id 
    slovo = message.text
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        if is_user_admin(chat_id, user_id):
            try:
                user_to_info = message.reply_to_message.from_user.id
                user_username = message.reply_to_message.from_user.username
                cursor.execute('SELECT user_warn_count FROM groups4 WHERE user_id = ? and group_id = ? ORDER BY id DESC', (user_to_info, chat_id,))
                user_warn_count = cursor.fetchone()
                if user_warn_count is not None:
                    user_warn_count = user_warn_count[0]
                else:
                    user_warn_count = 0
                connect.commit()
                user_warn_count = 0
                bot.reply_to(message, f"C пользователя @{user_username} сняты все предупреждения.")
                bot_messages_count += 1
                all_messages_count += 1
                query = """INSERT OR REPLACE INTO groups4 (group_id, user_id, user_warn_count) VALUES(?, ?, ?);"""
                cursor.execute(query, (chat_id, user_to_info, user_warn_count))
                connect.commit()
            except (IndexError, ValueError):
                bot.reply_to(message, "Используйте команду в формате: /warn_clear + ответ на сообщение человека, которому хотите снять все предупреждения.")
                bot_messages_count += 1
                all_messages_count += 1
            except telebot.apihelper.ApiException as e:
                bot.reply_to(message, f"Произошла ошибка при использовании команды. Возможно проблема в синтаксисе - правильный синтаксис: /warn_clear + ответ на сообщение челоевка, которому хотите снять все предупреждения.")
                bot_messages_count += 1
                all_messages_count += 1
        else: 
            bot.reply_to(message, "У вас нет прав для этой команды.")
            all_messages_count += 1
            bot_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()

@bot.message_handler(commands=['russian_roulette']) 
def russian_roulette_function(message): 
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    global ban_flag
    global clear_flag
    slovo = message.text
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        chat_id = message.chat.id 
        user_id = message.from_user.id 
        cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        all_messages_count = cursor.fetchone()
        if all_messages_count is not None:
            all_messages_count = all_messages_count[0]
        else:
            all_messages_count = 0
        cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        bot_messages_count = cursor.fetchone()
        if bot_messages_count is not None:
            bot_messages_count = bot_messages_count[0]
        else:
            bot_messages_count = 0
        cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        commands_messages_count = cursor.fetchone()
        if commands_messages_count is not None:
            commands_messages_count = commands_messages_count[0]
        else:
            commands_messages_count = 0
        cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        other_messages_count = cursor.fetchone()
        if other_messages_count is not None:
            other_messages_count = other_messages_count[0]
        else:
            other_messages_count = 0
        cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        ban_count = cursor.fetchone()
        if ban_count is not None:
            ban_count = ban_count[0]
        else:
            ban_count = 0
        cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
        mute_count = cursor.fetchone()
        if mute_count is not None:
            mute_count = mute_count[0]
        else:
            mute_count = 0
        all_messages_count += 1
        other_messages_count += 1
        commands_messages_count += 1
        query = """INSERT INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_all_messages_count = cursor.fetchone()
        if user_all_messages_count is not None:
            user_all_messages_count = user_all_messages_count[0]
        else:
            user_all_messages_count = 0
        cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_commands_messages_count = cursor.fetchone()
        if user_commands_messages_count is not None:
            user_commands_messages_count = user_commands_messages_count[0]
        else:
            user_commands_messages_count = 0
        cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
        user_mute_count = cursor.fetchone()
        if user_mute_count is not None:
            user_mute_count = user_mute_count[0]
        else:
            user_mute_count = 0
        connect.commit()
        user_commands_messages_count += 1
        user_all_messages_count += 1
        query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
        connect.commit()
        chislo = random.randint(0, 1)
        if chislo == 0:
            bot.reply_to(message, f"Удача, видимо, на вашей стороне! В этот раз вы остались в живых!")
            all_messages_count += 1
            bot_messages_count += 1
        elif chislo == 1:
            user_username = message.from_user.username 
            user_to_ban = message.from_user.id 
            try: 
                bot.ban_chat_member(chat_id, user_to_ban) 
                ban_count += 1
                query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
                connect.commit()
                bot.reply_to(message, f"Пользователь @{user_username} забанен.\nПричина: удача оказалась не на его стороне.")
                all_messages_count += 1 
                bot_messages_count += 1
            except: 
                bot.reply_to(message, f"Не удалось забанить пользователя @{user_username}.") 
                all_messages_count += 1
                bot_messages_count += 1
        query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
        connect.commit()
        connect.close()
    
# @bot.message_handler(commands=['banvote'])
# def start_ban_vote(message):
#     user_username = message.reply_to_message.from_user.username 
#     user_to_ban = message.reply_to_message.from_user.id 
#     bot.send_poll(chat_id=message.chat.id, question=f"Хотите ли вы забанить пользователя @{user_username}?", options=ansnwers, is_anonymous=False)
#     msg = bot.poll_answer_handler
#     if msg is not None:
#         bot.send_message(message.chat.id, msg)

# @bot.callback_query_handler(func=lambda call: True)
# def handle_poll_answer(call):
#     if call.poll:
#         # Получаем идентификатор опроса
#         poll_id = call.poll.id
#         # Получаем результаты голосования
#         poll_options = call.poll.options

#         # Словарь для хранения количества голосов для каждого варианта
#         votes_count = {option.text: option.votes for option in poll_options}

#         # Находим вариант с максимальным количеством голосов
#         max_votes = max(votes_count.values())
#         winners = [name for name, votes in votes_count.items() if votes == max_votes]

#         # Предположим, что имя пользователя хранится в сообщении
#         user_id = call.from_user.id
#         user_name = call.from_user.username or call.from_user.first_name

#         result_message = f"Пользователь {user_name} (ID: {user_id}) проголосовал за: {', '.join(winners)} с количеством голосов: {max_votes}."
        
#         # Отправляем сообщение с результатами голосования
#         bot.send_message(call.message.chat.id, result_message)
    

# @bot.callback_query_handler(func=lambda call: True)
# def handle_poll_answer(call):
#     if call.data in :
#         poll_id = call.message.poll.id
#         poll_results = call.message.poll.options
#         max_votes = 0
#         player_to_ban = None
#         for option in poll_results:
#             if option.votes > max_votes:
#                 max_votes = option.votes
#                 player_to_ban = option.text
#         if player_to_ban:
#             bot.send_message(call.chat.id, "тест")



@bot.message_handler(commands=['settings'])
def bot_settings(message):
    global start
    global clear_flag
    global call_admins
    global date
    global restricted_messages
    global restricted_messages_text
    global message_id
    global spam_flag
    global spam_flag_text
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    slovo = message.text
    chat_id = message.chat.id 
    user_id = message.from_user.id
    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)
        return
    if "@groups_defender_bot" in slovo:
        connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups1 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            list_words TEXT, 
            spam_flags BOOLEAN NOT NULL,
            clear_flags BOOLEAN NOT NULL,
            call_admins TEXT NOT NULL,
            mute_time INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups2 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            all_messages_count INTEGER NOT NULL, 
            bot_messages_count INTEGER NOT NULL,
            other_messages_count INTEGER NOT NULL,
            commands_messages_count INTEGER NOT NULL,
            ban_count INTEGER NOT NULL,
            mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups3 (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            user_all_messages_count INTEGER NOT NULL, 
            user_commands_messages_count INTEGER NOT NULL,
            user_mute_count INTEGER NOT NULL          
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups4 (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_warn_count INTEGER NOT NULL
            )
        ''')
        if is_user_admin(chat_id, user_id):
            cursor.execute('SELECT spam_flags FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            spam_flag = cursor.fetchone()
            if not "None" in str(spam_flag) and spam_flag[0] == 1:
                spam_flag = True
                spam_flag_text = 1
            else:
                spam_flag = False
                spam_flag_text = 0
            cursor.execute('SELECT mute_time FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            date = cursor.fetchone()
            if date is not None:
                date = int(date[0])
            else:
                date = 900
            cursor.execute('SELECT call_admins FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            call_admins = cursor.fetchone()
            if call_admins is not None and not "Нету" in call_admins:
                call_admins = call_admins
                call_admins_text = ", ".join(call_admins)
            else:
                call_admins = []
                call_admins_text = "Нету"
            cursor.execute('SELECT list_words FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            words = cursor.fetchone()
            if words is not None:
                restricted_messages = set(words)
                if not "None" in str(restricted_messages):
                    restricted_messages_text = ", ".join(restricted_messages)
                else:
                    restricted_messages_text = None
                    restricted_messages.clear()
            else:
                restricted_messages = set()
            cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            all_messages_count = cursor.fetchone()
            if all_messages_count is not None:
                all_messages_count = all_messages_count[0]
            else:
                all_messages_count = 0
            cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            bot_messages_count = cursor.fetchone()
            if bot_messages_count is not None:
                bot_messages_count = bot_messages_count[0]
            else:
                bot_messages_count = 0
            cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            commands_messages_count = cursor.fetchone()
            if commands_messages_count is not None:
                commands_messages_count = commands_messages_count[0]
            else:
                commands_messages_count = 0
            cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            other_messages_count = cursor.fetchone()
            if other_messages_count is not None:
                other_messages_count = other_messages_count[0]
            else:
                other_messages_count = 0
            cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            ban_count = cursor.fetchone()
            if ban_count is not None:
                ban_count = ban_count[0]
            else:
                ban_count = 0
            cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
            mute_count = cursor.fetchone()
            if mute_count is not None:
                mute_count = mute_count[0]
            else:
                mute_count = 0
            all_messages_count += 1
            commands_messages_count += 1
            other_messages_count += 1
            query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
            cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
            connect.commit()
            cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
            user_all_messages_count = cursor.fetchone()
            if user_all_messages_count is not None:
                user_all_messages_count = user_all_messages_count[0]
            else:
                user_all_messages_count = 0
            cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
            user_commands_messages_count = cursor.fetchone()
            if user_commands_messages_count is not None:
                user_commands_messages_count = user_commands_messages_count[0]
            else:
                user_commands_messages_count = 0
            cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
            user_mute_count = cursor.fetchone()
            if user_mute_count is not None:
                user_mute_count = user_mute_count[0]
            else:
                user_mute_count = 0
            connect.commit()
            user_commands_messages_count += 1
            user_all_messages_count += 1
            query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
            cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
            connect.commit()
            markup = types.InlineKeyboardMarkup(row_width=1)
            callback_button1 = types.InlineKeyboardButton("Изменить агентов поддержки", callback_data="admins_settings")
            callback_button2 = types.InlineKeyboardButton("Изменить время мута", callback_data="date_settings")
            markup.add(callback_button1, callback_button2)
            bot_messages_count += 1
            all_messages_count += 1
            msg = bot.send_message(message.chat.id, f"<b>Настройки и статус бота.</b>\n<i>True - Включен.\nFalse - Выключен.</i>\n<b>Статистика:</b>\n<i>Всего сообщений: </i>{all_messages_count}.\n\t\t<i>Сообщения от участников: </i>{other_messages_count}.\n\t\t\t\t<i>В том числе сообщения с командами: </i>{commands_messages_count}.\n\t\t<i>Сообщения от бота: </i>{bot_messages_count}.\n<i>Забанено участников ботом: </i>{ban_count}.\n<i>Замучено участников ботом: </i>{mute_count}.\n<b>Статус функций бота:</b>\n<b>Антиспам-фильтр: </b>{spam_flag}.\n<b>Агенты поддержки(call-админы): </b>{call_admins_text}.\n<b>Время мута: </b>{date}.", reply_markup=markup, parse_mode="HTML")
            query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
            cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
            connect.commit()
            message_id = msg.message_id
            query = """INSERT OR REPLACE INTO groups1 (group_id, list_words, spam_flags, clear_flags, call_admins, mute_time) VALUES(?, ?, ?, ?, ?, ?);"""
            cursor.execute(query, (chat_id, restricted_messages_text, spam_flag_text, clear_flag, call_admins_text, date))
            connect.commit()
            connect.close()
        else: 
            bot.reply_to(message, "У вас нет прав для этой команды.")
            all_messages_count += 1
            bot_messages_count += 1

        
# @bot.message_handler(commands=['test']) 
# def server_isolation(message): 
#     chat_id = message.chat.id 
#     user_id = message.from_user.id 
#     if is_user_admin(chat_id, user_id):
#         markup = types.InlineKeyboardMarkup()
#         callback_button1 = types.InlineKeyboardButton("Да", callback_data="start")
#         callback_button2 = types.InlineKeyboardButton("Нет", callback_data="stop")
#         markup.row(callback_button1, callback_button2)
#         bot.send_message(message.chat.id, f"<b>ВНИМАНИЕ! Данная команда будет АВТОМАТИЧЕСКИ БАНИТЬ ВСЕХ НОВЫХ УЧАСТНИКОВ СЕРВЕРА.</b>\n\nВы точно хотите начать?", reply_markup=markup, parse_mode="HTML")
#     else: 
#         bot.reply_to(message, "У вас нет прав для этой команды.")

@bot.callback_query_handler(func=lambda call: call.data == 'admins_settings')
def save_btn(call):
    global call_flag
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    message = call.message
    chat_id = message.chat.id
    user_id = message.from_user.id
    call_flag = True
    connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups1 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        list_words TEXT, 
        spam_flags BOOLEAN NOT NULL,
        clear_flags BOOLEAN NOT NULL,
        call_admins TEXT NOT NULL,
        mute_time INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups2 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        all_messages_count INTEGER NOT NULL, 
        bot_messages_count INTEGER NOT NULL,
        other_messages_count INTEGER NOT NULL,
        commands_messages_count INTEGER NOT NULL,
        ban_count INTEGER NOT NULL,
        mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups3 (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        user_all_messages_count INTEGER NOT NULL, 
        user_commands_messages_count INTEGER NOT NULL,
        user_mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups4 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        user_warn_count INTEGER NOT NULL
        )
    ''')
    if is_user_admin(chat_id, user_id): 
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text='Введите имена новых агентов поддержки через запятую с пробелом и без других посторонних знаков.')
        bot_messages_count += 1
        all_messages_count += 1
    else: 
        bot.send_message(chat_id, "У вас нет прав для этой команды.")
        bot_messages_count += 1
        all_messages_count += 1
    query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
    connect.commit()
    connect.close()

@bot.callback_query_handler(func=lambda call: call.data == 'date_settings')
def save_btn(call):
    global date_flag
    global message_id
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_messages_count
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    message = call.message
    chat_id = message.chat.id
    user_id = message.from_user.id
    date_flag = True
    connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups1 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        list_words TEXT, 
        spam_flags BOOLEAN NOT NULL,
        clear_flags BOOLEAN NOT NULL,
        call_admins TEXT NOT NULL,
        mute_time INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups2 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        all_messages_count INTEGER NOT NULL, 
        bot_messages_count INTEGER NOT NULL,
        other_messages_count INTEGER NOT NULL,
        commands_messages_count INTEGER NOT NULL,
        ban_count INTEGER NOT NULL,
        mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups3 (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        user_all_messages_count INTEGER NOT NULL, 
        user_commands_messages_count INTEGER NOT NULL,
        user_mute_count INTEGER NOT NULL          
        )
    ''')        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups4 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        user_warn_count INTEGER NOT NULL
        )
    ''')
    if is_user_admin(chat_id, user_id): 
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text= f'Введите новое время мута в секундах.')
        bot_messages_count += 1
        all_messages_count += 1
    else: 
        bot.send_message(chat_id, "У вас нет прав для этой команды.")
        bot_messages_count += 1
        all_messages_count += 1
    query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
    connect.commit()
    connect.close()

# @bot.message_handler(content_types=['new_chat_members'])
# def welcome_new_member(message):
#     global user_join_date
#     global user_all_messages_count
#     global user_commands_messages_count
#     global user_mute_count
#     for new_member in message.new_chat_members:
#         user_join_date = dt.now().strftime('%d-%m-%Y %H:%M:%S')
#         chat_id = message.chat.id
#         user_to_info = new_member.id
#         query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_join_date, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?, ?);"""
#         cursor.execute(query, (chat_id, user_to_info, user_join_date, user_all_messages_count, user_commands_messages_count, user_mute_count))
#         connect.commit()

# @bot.message_handler(content_types=['new_chat_members'])
# def welcome_new_member(message):
#     for new_member in message.new_chat_members:
#         bot.send_message(message.chat.id, f"Привет, {new_member.first_name}!")

@bot.message_handler(content_types=['text', 'sticker'])
def text_functions(message):
    global clear_flag
    global spam_flag 
    global count
    global date
    global date_flag
    global call_flag
    global call_admins
    global call_admins_text
    global message_id
    global list_add_flag
    global list_del_flag
    global restricted_flag
    global restricted_messages
    global restricted_messages_text
    global last_word
    global all_messages_count
    global bot_messages_count
    global ban_count
    global mute_count
    global other_messages_count
    global commands_list
    global commands_messages_count
    global user_all_messages_count
    global user_commands_messages_count
    global user_mute_count
    chat_id = message.chat.id 
    user_id = message.from_user.id
    message_id = message.message_id
    user_username = message.from_user.username 
    spisok = []
    connect = sqlite3.connect('group_defender_database.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups1 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        list_words TEXT, 
        spam_flags BOOLEAN NOT NULL,
        clear_flags BOOLEAN NOT NULL,
        call_admins TEXT NOT NULL,
        mute_time INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups2 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        all_messages_count INTEGER NOT NULL, 
        bot_messages_count INTEGER NOT NULL,
        other_messages_count INTEGER NOT NULL,
        commands_messages_count INTEGER NOT NULL,
        ban_count INTEGER NOT NULL,
        mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups3 (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        user_all_messages_count INTEGER NOT NULL, 
        user_commands_messages_count INTEGER NOT NULL,
        user_mute_count INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups4 (
        id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        user_warn_count INTEGER NOT NULL
        )
    ''')
    cursor.execute('SELECT all_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    all_messages_count = cursor.fetchone()
    if all_messages_count is not None:
        all_messages_count = all_messages_count[0]
    else:
        all_messages_count = 0
    cursor.execute('SELECT bot_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    bot_messages_count = cursor.fetchone()
    if bot_messages_count is not None:
        bot_messages_count = bot_messages_count[0]
    else:
        bot_messages_count = 0
    cursor.execute('SELECT commands_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    commands_messages_count = cursor.fetchone()
    if commands_messages_count is not None:
        commands_messages_count = commands_messages_count[0]
    else:
        commands_messages_count = 0
    cursor.execute('SELECT other_messages_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    other_messages_count = cursor.fetchone()
    if other_messages_count is not None:
        other_messages_count = other_messages_count[0]
    else:
        other_messages_count = 0
    cursor.execute('SELECT ban_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    ban_count = cursor.fetchone()
    if ban_count is not None:
        ban_count = ban_count[0]
    else:
        ban_count = 0
    cursor.execute('SELECT mute_count FROM groups2 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    mute_count = cursor.fetchone()
    if mute_count is not None:
        mute_count = mute_count[0]
    else:
        mute_count = 0
    all_messages_count += 1
    other_messages_count += 1
    query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
    connect.commit()
    cursor.execute('SELECT user_all_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
    user_all_messages_count = cursor.fetchone()
    if user_all_messages_count is not None:
        user_all_messages_count = user_all_messages_count[0]
    else:
        user_all_messages_count = 0
    cursor.execute('SELECT user_commands_messages_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
    user_commands_messages_count = cursor.fetchone()
    if user_commands_messages_count is not None:
        user_commands_messages_count = user_commands_messages_count[0]
    else:
        user_commands_messages_count = 0
    cursor.execute('SELECT user_mute_count FROM groups3 WHERE user_id = ? AND group_id = ? ORDER BY id DESC', (user_id, chat_id,))
    user_mute_count = cursor.fetchone()
    if user_mute_count is not None:
        user_mute_count = user_mute_count[0]
    else:
        user_mute_count = 0
    connect.commit()
    user_all_messages_count += 1
    query = """INSERT OR REPLACE INTO groups3 (group_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count) VALUES(?, ?, ?, ?, ?);"""
    cursor.execute(query, (chat_id, user_id, user_all_messages_count, user_commands_messages_count, user_mute_count))
    connect.commit()
    cursor.execute('SELECT spam_flags FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    spam_flag = cursor.fetchone()
    if not "None" in str(spam_flag) and spam_flag[0] == 1:
        spam_flag = True
        spam_flag_text = 1
    else:
        spam_flag = False
        spam_flag_text = 0
    cursor.execute('SELECT mute_time FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    date = cursor.fetchone()
    if date is not None:
        date = int(date[0])
    else:
        date = 900
    cursor.execute('SELECT call_admins FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    call_admins = cursor.fetchone()
    if call_admins is not None and not "Нету" in call_admins:
        call_admins = call_admins
        call_admins_text = ", ".join(call_admins)
    else:
        call_admins = []
        call_admins_text = "Нету"
    cursor.execute('SELECT list_words FROM groups1 WHERE group_id = ? ORDER BY id DESC', (chat_id,))
    words = cursor.fetchone()
    if words is not None:
        restricted_messages = set(words)
        if not "None" in str(restricted_messages):
            restricted_messages_text = ", ".join(restricted_messages)
        else:
            restricted_messages_text = None
            restricted_messages.clear()
    else:
        restricted_messages = set()
    for i in restricted_messages:
        if i in message.text.lower() and restricted_flag == True: 
            try:
                user_to_mute = message.from_user.id
                bot.delete_message(chat_id, message.message_id) 
                date1 = dt.timedelta(seconds=date) 
                date2 = dt.datetime.now() + date1
                date3 = date2.strftime("%d-%m-%Y %H:%M:%S")
                bot.restrict_chat_member(chat_id, user_to_mute, until_date=dt.datetime.now()+date1)
                mute_count += 1
                query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
                connect.commit()
                if date > 30 and date < 31622400:
                    bot.send_message(chat_id, f"Пользователь @{user_username} замучен до {date3}. Причина: использование запрещенных слов в чвте.")
                    all_messages_count += 1
                    bot_messages_count += 1
                else:
                    bot.send_message(chat_id, f"Пользователь @{user_username} замучен навсегда.")
                    all_messages_count += 1
                    bot_messages_count += 1
            except: 
                    bot.send_message(chat_id, f"Не удалось замутить пользователя.") 
                    all_messages_count += 1
                    bot_messages_count += 1

    if clear_flag == True:
        bot.delete_message(message.chat.id, message.message_id)

    if spam_flag == True:
        if count < 1:
            if message.content_type == 'text':
                try:
                    for entity in message.entities:
                        if entity.type in ["url", "text_link"]: 
                            bot.delete_message(message.chat.id, message.message_id)
                except:
                    pass
                if last_word is not None and last_word in message.text.lower():
                    count += 1
                else:
                    last_word = message.text.lower()
                    count = 0
                    count += 1
            elif message.content_type == 'sticker':
                count += 1
        else:
                date1 = dt.timedelta(seconds=date) 
                date2 = dt.datetime.now() + date1
                date3 = date2.strftime("%Y-%m-%d %H:%M:%S")
                user_to_mute = message.from_user.id
                for i in range(count):
                    try:
                        bot.delete_message(chat_id, message_id - i - 1)
                    except:
                        bot.send_message(chat_id, f"Ошибка при удалении сообщений.")
                        bot_messages_count += 1
                        all_messages_count += 1
                try: 
                    bot.restrict_chat_member(chat_id, user_to_mute, until_date=dt.datetime.now()+date1)
                    if date > 30 and date < 31622400:
                        bot.send_message(chat_id, f"Пользователь @{user_username} замучен до {date3}. Причина: спам.")
                        all_messages_count += 1
                        bot_messages_count += 1
                    else:
                        bot.send_message(chat_id, f"Пользователь @{user_username} замучен навсегда.")
                        all_messages_count += 1
                        bot_messages_count += 1
                    count = 0
                except: 
                    bot.send_message(chat_id, f"Не удалось замутить пользователя.")
                    all_messages_count += 1
                    bot_messages_count += 1
                    count = 0

    if date_flag == True:
        if is_user_admin(chat_id, user_id):
            try:
                date = int(message.text)
                cursor.execute('''INSERT OR REPLACE INTO groups1 (group_id, list_words, spam_flags, clear_flags, call_admins, mute_time) VALUES(?, ?, ?, ?, ?, ?)''', (chat_id, restricted_messages_text, spam_flag, clear_flag, call_admins_text, date))
                bot.send_message(message.chat.id, f'Время мута было успешно изменено. Используйте команду /settings, чтобы вернуться на страницу настроек.')  
                connect.commit()
                date_flag = False 
            except:
                bot.send_message(message.chat.id, f"Произошло ошибка. Попробуйте еще раз.")  
                bot_messages_count += 1
                all_messages_count += 1
        else:
            bot.reply_to(message, "У вас нет прав для этой команды.") 
            bot_messages_count += 1
            all_messages_count += 1

    if call_flag == True:
        if is_user_admin(chat_id, user_id):
            try:
                call_admins = message.text.split(", ")
                call_admins_text = ", ".join(call_admins)
                cursor.execute('''INSERT OR REPLACE INTO groups1 (group_id, list_words, spam_flags, clear_flags, call_admins, mute_time) VALUES(?, ?, ?, ?, ?, ?)''', (chat_id, restricted_messages_text, spam_flag, clear_flag, call_admins_text, date))
                connect.commit()
                bot.send_message(chat_id, f'Агенты поддержки были успешно добавлены. Используйте команду /settings, чтобы вернуться на страницу настроек.')
                bot_messages_count += 1
                all_messages_count += 1
                call_flag = False
            except:
                bot.send_message(message.chat.id, f"Произошло ошибка. Попробуйте еще раз.")
                bot_messages_count += 1
                all_messages_count += 1
        else:
            bot.reply_to(message, "У вас нет прав для этой команды.")
            bot_messages_count += 1
            all_messages_count += 1

    if list_add_flag == True:
        if is_user_admin(chat_id, user_id):
            restricted_messages.add(str(message.text.lower()))
            restricted_messages_text = ", ".join(restricted_messages)
            cursor.execute('''INSERT OR REPLACE INTO groups1 (group_id, list_words, spam_flags, clear_flags, call_admins, mute_time) VALUES(?, ?, ?, ?, ?, ?)''', (chat_id, restricted_messages_text, spam_flag, clear_flag, call_admins_text, date))
            bot.send_message(message.chat.id, f"Слово успешно добавлено.")
            bot_messages_count += 1
            all_messages_count += 1
            connect.commit()
            list_add_flag = False
        else:
            bot.send_message(message.chat.id, f"У вас нет прав для этой команды.")
            bot_messages_count += 1
            all_messages_count += 1
            list_add_flag = False

    if list_del_flag == True:
        if is_user_admin(chat_id, user_id):
            try:
                restricted_messages = str(*restricted_messages).split(", ")
                restricted_messages.remove(str(message.text.lower()))
                restricted_messages_text = None
                cursor.execute('''INSERT OR REPLACE INTO groups1 (group_id, list_words, spam_flags, clear_flags, call_admins, mute_time) VALUES(?, ?, ?, ?, ?, ?)''', (chat_id, restricted_messages_text, spam_flag, clear_flag, call_admins_text, date))
                bot.send_message(message.chat.id, f"Слово успешно удалено.")
                bot_messages_count += 1
                all_messages_count += 1
                connect.commit()
                list_del_flag = False
                restricted_flag = True
            except:
                bot.send_message(message.chat.id, f"В списке нету слова, которое вы пытаетесь удалить.")
                bot_messages_count += 1
                all_messages_count += 1
                restricted_flag = True
                list_del_flag = False
        else:
            bot.send_message(message.chat.id, f"У вас нет прав для этой команды.")
            bot_messages_count += 1
            all_messages_count += 1
            restricted_flag = True
            list_del_flag = False
    query = """INSERT OR REPLACE INTO groups2 (group_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count) VALUES(?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(query, (chat_id, all_messages_count, bot_messages_count, other_messages_count, commands_messages_count, ban_count, mute_count))
    connect.commit()
    connect.close()



bot.polling(none_stop=True, interval=0)
