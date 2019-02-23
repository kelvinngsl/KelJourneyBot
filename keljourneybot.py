import os, requests, re

from configparser import ConfigParser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from busarrival import Bus
import geolocation


config = ConfigParser()
config.read('config.ini')

token = config.get('API','TELE_KEY')
PORT = int(os.environ.get('PORT', '8443'))

def start(bot,update):
    chat_id = update.message.chat_id
    update.message.reply_text('Hi there! \U0001F60A')
    update.message.reply_text('Start by selecting your bus stop by /set <busstopcode>')
    update.message.reply_text('For Example: /set 65191')
    update.message.reply_text('Or send your location to me! \U0001F609')

    
def set_up(bot,update):
    global busstop
    busstop = update.message.text.split()[1]
    bus = Bus(busstop)

    if bus.check_legit(): 

        bus_list = sorted(bus.get_bus_List())
        keyboard = []

        keyboard = []
        for i in range(0,len(bus_list),4):
            if (i+4 > len(bus_list)-1) and len(bus_list) % 4 == 2:
                keyboard = keyboard + [[InlineKeyboardButton(text = bus_list[i], callback_data = 'B'+bus_list[i]), InlineKeyboardButton(text = bus_list[i+1], callback_data = 'B'+bus_list[i+1])]]
            elif (i+4 > len(bus_list)-1) and len(bus_list) % 4 == 1:
                keyboard = keyboard + [[InlineKeyboardButton(text = bus_list[i], callback_data = 'B'+bus_list[i])]]
            elif (i+4 > len(bus_list)-1) and len(bus_list) % 4 == 3:
                keyboard = keyboard + [[InlineKeyboardButton(text = bus_list[i], callback_data = 'B'+bus_list[i]), InlineKeyboardButton(text = bus_list[i+1], callback_data = 'B'+bus_list[i+1]), InlineKeyboardButton(text = bus_list[i+2], callback_data = 'B'+bus_list[i+2])]]
            else:
                keyboard = keyboard + [[InlineKeyboardButton(text = bus_list[i], callback_data = 'B'+bus_list[i]), InlineKeyboardButton(text = bus_list[i+1], callback_data = 'B'+bus_list[i+1]), InlineKeyboardButton(text = bus_list[i+2], callback_data = 'B'+bus_list[i+2]), InlineKeyboardButton(text = bus_list[i+3], callback_data = 'B'+bus_list[i+3])]]
        
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    

        update.message.reply_text(reply_markup=reply_markup, text = 'Please select the bus \U0001F68C:')
    
    else:
        update.message.reply_text('Invalid Bus Stop Number! \U0000274C. Please repeat')

def button(bot,update):
    global busstop
    query = update.callback_query
    
    if query.data[0] == "B":
        query = update.callback_query
        query.edit_message_text(text="Selected Bus: {}".format(query.data[1:]))
        global busno
        busno = query.data[1:]
        
        keyboard = [[InlineKeyboardButton("<=8", callback_data='C1'),
                    InlineKeyboardButton(">8", callback_data='C2')
                    ]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(reply_markup=reply_markup, text = 'Please select the walking duration to bus stop (mins) \U0001F6B6')


    elif query.data[0] == "C":
        query = update.callback_query
        if query.data == "C1":
            keyboard = [[InlineKeyboardButton("1", callback_data='1'),
                        InlineKeyboardButton("2", callback_data='2'),
                        InlineKeyboardButton("3", callback_data='3'),
                        InlineKeyboardButton("4", callback_data='4'),
                        InlineKeyboardButton("5", callback_data='5'),
                        InlineKeyboardButton("6", callback_data='6'),
                        InlineKeyboardButton("7", callback_data='7'),
                        InlineKeyboardButton("8", callback_data='8')
                        ]]
        else:
            keyboard = [[InlineKeyboardButton("9", callback_data='9'),
                        InlineKeyboardButton("10", callback_data='10'),
                        InlineKeyboardButton("11", callback_data='11'),
                        InlineKeyboardButton("12", callback_data='12'),
                        InlineKeyboardButton("13", callback_data='13'),
                        InlineKeyboardButton("14", callback_data='14'),
                        InlineKeyboardButton("15", callback_data='15'),
                        InlineKeyboardButton("16", callback_data='16')
                        ]]

            
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(reply_markup=reply_markup, text = 'Please select the walking duration to the bus stop (mins) \U0001F6B6')
    
    elif query.data[0] == "S":

        query = update.callback_query
        query.edit_message_text(text="Selected Bus Stop: {}".format(query.data[1:]))

        busstop = query.data[1:]
        bus = Bus(busstop)

        bus_list = sorted(bus.get_bus_List())

        keyboard = []
        for i in range(0,len(bus_list),4):
            if (i+4 > len(bus_list)-1) and len(bus_list) % 4 == 2:
                keyboard = keyboard + [[InlineKeyboardButton(text = bus_list[i], callback_data = 'B'+bus_list[i]), InlineKeyboardButton(text = bus_list[i+1], callback_data = 'B'+bus_list[i+1])]]
            elif (i+4 > len(bus_list)-1) and len(bus_list) % 4 == 1:
                keyboard = keyboard + [[InlineKeyboardButton(text = bus_list[i], callback_data = 'B'+bus_list[i])]]
            elif (i+4 > len(bus_list)-1) and len(bus_list) % 4 == 3:
                keyboard = keyboard + [[InlineKeyboardButton(text = bus_list[i], callback_data = 'B'+bus_list[i]), InlineKeyboardButton(text = bus_list[i+1], callback_data = 'B'+bus_list[i+1]), InlineKeyboardButton(text = bus_list[i+2], callback_data = 'B'+bus_list[i+2])]]
            else:
                keyboard = keyboard + [[InlineKeyboardButton(text = bus_list[i], callback_data = 'B'+bus_list[i]), InlineKeyboardButton(text = bus_list[i+1], callback_data = 'B'+bus_list[i+1]), InlineKeyboardButton(text = bus_list[i+2], callback_data = 'B'+bus_list[i+2]), InlineKeyboardButton(text = bus_list[i+3], callback_data = 'B'+bus_list[i+3])]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
        query.edit_message_text(reply_markup=reply_markup, text = 'Please select the bus \U0001F68C:')

        
  
    else:
        query.edit_message_text(text="Selected Duration: {}".format(query.data))
        global duration
        duration = int(query.data)

        bus = Bus(busstop)
        
        confirmation_reply = "<b>Bus: {}\nBus Stop: {}\nWalking duration: {} mins</b>.".format(busno,busstop,duration)
        query.edit_message_text(text=confirmation_reply+ "\n\n" + bus.get_time(busno,duration),parse_mode='HTML')


def get_nearby(bot,update):
    lat = str(update.message.location.latitude)
    long = str(update.message.location.longitude)
    
    bus = Bus('')
    bus_list = bus.get_busstop()
    nearby = geolocation.get_nearby(lat,long)

    matched_list = []

    for item in nearby:
        for bus in bus_list:
            if item[2] == bus["Description"]:
                matched_list.append((bus['Description'],bus['BusStopCode']))
                break
    if len(matched_list) == 0:
        update.message.reply_text('There are no nearby bus stops! \U0001F68F')
    else:


        keyboard = [[InlineKeyboardButton(match[0] + " - " + match[1], callback_data= 'S' + match[1])] for match in matched_list[:8]]
    
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please select the bus stop \U0001F68F:', reply_markup=reply_markup)


def main():
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=token)
    
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('set',set_up))
    dp.add_handler(MessageHandler(Filters.location, get_nearby))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.bot.set_webhook("https://kjb2.herokuapp.com/" + token)
    updater.idle()

if __name__ == '__main__':
    print ('Bot is running')
    main()
    print ('Bot ending')
