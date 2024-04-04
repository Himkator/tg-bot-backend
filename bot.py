import telebot
import sqlite3

bot=telebot.TeleBot('6796259858:AAE9eYe-L0GhOmjcC_ysPK5zYypyBKwcfDM')

@bot.message_handler(commands=['start'])
def start(message):
    conn=sqlite3.connect('tasks.sql')
    cur=conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, username varchar(100), chat_id text, tasks varchar(100));')
    conn.commit()

    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, '+message.from_user.first_name+' я твой личный бот для менеджмента твоих дел.\nЕсли хочешь написать задачу напиши /add_task\nЕсли вы хотите увидеть все задачи напишите /all_task.\nЕсли хотите удалить напишите /delete_task')

@bot.message_handler(commands=['add_task'])
def add(message):

    bot.send_message(message.chat.id, 'Напишите пожалуйста вашу задачу')
    bot.register_next_step_handler(message, add_task)
@bot.message_handler(commands=['all_task'])
def all(message):
    bot.send_message(message.chat.id, all_tasks(message))
@bot.message_handler(commands=['delete_task'])
def delete(message):
    bot.send_message(message.chat.id, "Напишите номер задание которого элемента которого хотите удалить\n"+all_tasks(message))
    bot.register_next_step_handler(message, delete_task)


def add_task(message):
    conn=sqlite3.connect('tasks.sql')
    cur=conn.cursor()


    cur.execute("INSERT INTO users(username, chat_id, tasks) VALUES('%s', '%s', '%s');" % (message.from_user.first_name,str(message.chat.id), message.text))
    conn.commit()

    cur.close()
    conn.close()

    markup=telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список задач', callback_data='tasks'))
    bot.send_message(message.chat.id, "Задача была сохранена", reply_markup=markup)

def delete_task(message):
    i=message.text
    info=all_tasks(message).split('\n')
    infos=info[int(i)-1].split(" ")
    
    conn=sqlite3.connect('tasks.sql')
    cur=conn.cursor()


    cur.execute("Delete from users where chat_id=='%s' and tasks=='%s'"%(message.chat.id, infos[1]))
    conn.commit()

    cur.close()
    conn.close()
    bot.send_message(message.chat.id, "Задача была удалена")
    all(message)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data=='tasks':
            bot.send_message(call.message.chat.id, all_tasks(call.message))

def all_tasks(message):
    conn=sqlite3.connect('tasks.sql')
    cur=conn.cursor()


    cur.execute("Select * from users where chat_id=='%s'"%(message.chat.id))
    users=cur.fetchall()

    info=''
    i=1
    for el in users:
        info+=f'{i}. {el[3]}\n'
        i+=1

    cur.close()
    conn.close()
    return info

bot.polling(non_stop=True)