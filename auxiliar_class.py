import socket
from config import config

class BotInfoSender():
    def __init__(self):
        self.path = config['socket_path']
        self.sock_fd = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        
    def send_msg(self, user, text):
        final_msg = '{}:{}~'.format(user,text).encode('utf-8')
        self.sock_fd.connect(self.path)
        self.sock_fd.send(final_msg)
        self.sock_fd.close()
        print('Message sent {}'.format(final_msg))
