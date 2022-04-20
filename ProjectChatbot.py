from glob import glob
import time
from tokenize import String
from unicodedata import name
from webbrowser import get
from telegram import Update,InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext,CallbackQueryHandler
import random
import configparser
import logging
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def firebase():
    cred = credentials.Certificate('chatbot-cf4ce-firebase-adminsdk-t6b1e-25d55c8560.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://chatbot-cf4ce-default-rtdb.firebaseio.com/'
    })
    ref = db.reference('/')
    print(ref.get())
    return ref

def main():
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    # updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global hands
    hands = ['rock', 'paper', 'scissors','quit']
    global emoji
    emoji = {
    'rock': '👊',
    'paper': '✋',
    'scissors': '✌️',
    'quit': '❎'
            }
    
    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    dispatcher.add_handler(CommandHandler("start", start))   
    dispatcher.add_handler(CommandHandler('game', game))
    dispatcher.add_handler(CommandHandler('show', show))
    dispatcher.add_handler(CallbackQueryHandler(play))

    # To start the bot:
    updater.start_polling()
    updater.idle()

times = firebase().child('times')

def get_message(msg):
    wl = {'win':0, 'lose':0, 'draw':0}
    try:
        i = times.get()[f'{msg}']
        print(i['win'])
        print("eee")
    except:
        times.update({msg:wl})
        i = times.get()[f'{msg}']
        print(i['win'])
        print("ddd")
    return i
def start(update: Update, context: CallbackContext) -> None:
    global name
    name = context.args[0]
    get_message(name)
    message = 'Welcome to the bot. The game already start'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
def show(update: Update, context: CallbackContext) -> None:

    msg = context.args[0]

    i = get_message(msg)
    n = i['win']+ i['lose'] + i['draw']
    w = i['win']
    l = i['lose']
    d = i['draw']
    if w == 0:
        wr=0
    else:
        wr=w/(w+l)
        
        
    context.bot.send_message(chat_id=update.effective_chat.id, text='Player {} played the game {} times.Win {} ,lose {}, tie {}. Win rate is {}.'.format(msg,n,w,l,d,wr))

def game(update, bot):
    
    update.message.reply_text('Scissors, stone cloth！',
        reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(emoji, callback_data = hand) for hand, emoji in emoji.items()
            ]]))

def judge(mine, yours):
    
    if mine == yours:

        return 'Tie'
    elif (hands.index(mine) - hands.index(yours)) % 3 == 1:

        return 'You lost'
    else:

       
        return 'You win'

def play(update, context):
    print("yy")
    try:
        mine = random.choice(hands)
        while mine=='quit':
            mine = random.choice(hands)
    
        yours = update.callback_query.data

        if yours=='quit':
            return
        d = times.get()[f'{name}']["draw"]
        l = times.get()[f'{name}']["lose"]
        w = times.get()[f'{name}']["win"]
        if mine == yours:
            d = d+1
            times.update({name:{'win':w,'draw':d,'lose':l}})
        elif (hands.index(mine) - hands.index(yours)) % 3 == 1:
            l = l+1
            times.update({name:{'win':w,'draw':d,'lose':l}})
        else:
            w = w+1
            times.update({name:{'win':w,'draw':d,'lose':l}})
            
        
        update.callback_query.edit_message_text('Result:')
        context.bot.send_message(chat_id=update.effective_chat.id, text='{}！！！！！you are {}，I am{}'.format(judge(mine, yours),emoji[yours], emoji[mine] ))
        time.sleep(0.5)
        update.callback_query.edit_message_text('Scissors, stone cloth！',
            reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(emoji, callback_data = hand) for hand, emoji in emoji.items()
            ]]))
    except Exception as e:
        print(e)

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Attention: input /start Yourname to start game. input /game the game will begin. And /show Yourname for score of player.')

if __name__ == '__main__':
    main()
  
