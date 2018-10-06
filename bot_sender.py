import argparse
import telebot
from config import config
import threading
import socket
from os.path import exists
from os import remove
import sqlite3

#thread class
class Listener(threading.Thread):
    def __init__(self, bot):
        threading.Thread.__init__(self)
        con = sqlite3.connect(db_name)
        cursor_thread = con.cursor()
        self.bot = bot
        
        self.socket_fd = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if exists(config['socket_path']): #check if the socket file exixts
            remove(config['socket_path'])
            
        self.socket_fd.bind(config['socket_path'])
        self.socket_fd.listen(1)
        return

    def send_message(self, user, msg):
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        cursor.execute(select_chat_statement, (user,))

        try:
            chat_id = cursor.fetchone()[0]
            con.close()
            print(chat_id)
            if chat_id > 0:
                self.bot.send_message(chat_id, msg[:-1])
        except:
            print('This user is not registered in the database. Message not sent')
        
    def run(self):
        while 1:
            #listen on specified port
            conn, addr = self.socket_fd.accept()
            while 1:
                data = conn.recv(200)
                #print(data)
                if end_symbol in data.decode('utf-8'):
                    conn.close()
                    print(data)
                    res = data.decode('utf-8').split(separate_simbol)
                    print(res[0], res[1])
                    self.send_message(res[0], res[1])
                    break
                
def create_database(db_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE chats (user TEXT, chat_id INTEGER)''')
    con.commit()
    con.close()

#init
global chat_id
insertion_statement = 'INSERT INTO chats VALUES(?,?)'
select_chat_statement = 'SELECT chat_id FROM chats WHERE user=?'
api_key = config['api_key']
ids = config['ids']
db_name = config['db_name']
end_symbol = '~'
separate_simbol = ':'
if not exists(db_name):
    create_database(db_name)
    
bot = telebot.TeleBot(api_key)

@bot.message_handler(func=lambda m: True)
def register_user(m):
    global chat_id
    user = m.from_user.username
    chat_id = m.chat.id
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    cursor.execute(select_chat_statement, (user,))
    if not cursor.fetchone():
        cursor.execute(insertion_statement, [user, chat_id]) #insert if not exists
    con.commit()
    con.close()
    bot.reply_to(m, '[bot]> You have been added to the users list')
    if user not in ids and ids != []:
        bot.reply_to(m, '[bot]> You aren\'t an administrator. Close the door when leaving.')
        return
            
print('Running')

thread = Listener(bot)
thread.start()
bot.polling()
