# Telegram bot notificator

This system is composed by two parts:

## Telegram bot
This is a class that stablish the communication with telegram, receiving the commands and sending the responses to the people.
It will open an internal port where it will be listening for intern commands or messages and forward them to the user through telegram.

### Usage

#### Configuration
Fill the options at the file config.py.
The config file has 4 arguments:
- api_key: the api key the bot you have previously created through BotFather
- ids: this is used to restrict the users that can communicate with the bot. If its empty `[]`, every user will be able to send and receive messages to/from the bot.
- socket_path: the file used for IPC between the bot process and who sends the notifications
- db_name: name of the database. This database is to keep a track of the users that had "logged in" and are allowed to receive notifications.
```python
config = {'api_key':'your_api_key',
          'ids':[],
          'socket_path':'/tmp/socket_com',
          'db_name':'chats_ids'
}
```
#### Run the bot
`Usage: bot.py config.py`

> Once the bot is running, the users that will recieve the notifications, needs to text first to the bot, in order to be registered at the database.

## Auxiliar class

This class will be included in those programs that the programmer wants to send messages through telegram in an easy way.
The auxiliar clase will be invoked with only an argument, the port where it should be listening.

### Usage:
Import the class and invoque the function `send_msg(user, message)` with the user who will receive the message.
> The user needs to be previously registered to receive the message
> `config.py` file needs to be in the same folder
```python
from auxiliar_class import BotInfoSender
sender = BotInfoSender()
b.send_msg(user, message)
```