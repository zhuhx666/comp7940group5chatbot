from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import configparser
import logging
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def firebase():
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('chatbot-cf4ce-firebase-adminsdk-t6b1e-25d55c8560.json')

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://chatbot-cf4ce-default-rtdb.firebaseio.com/'
    })

    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('/')
    print(ref.get())
    return ref

# def increment_votes(current_value):
#     return current_value + 1 if current_value else 1

def main():
    # Load your token and create an Updater for your Bot
    
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    # updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    # dispatcher = updater.dispatcher
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", Hello_Kevin))


    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

times = firebase().child('times')
def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        print("aaa")
        # new__count = times.transaction(increment_votes(msg))
        try:
            i = times.get()[f'{msg}'] +1
            times.update({msg:i})
            print("eee")
        except:
            times.update({msg:1})
            i = times.get()[f'{msg}']
            print("ddd") 

        # redis1.incr(msg)
        # update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
        update.message.reply_text('You have said ' + msg +  ' for ' + str(i) + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def Hello_Kevin(update: Update, context: CallbackContext) -> None:
        name = context.args[0]
        update.message.reply_text('Good day, '+ name +'!.')



if __name__ == '__main__':
    main()