import requests
import telebot
import json
import os

from config import telegram_bot_token, stock_token

#constances

"""
description to all new feachers can be simply added to subcommand_list

"""

bot = telebot.TeleBot(telegram_bot_token)

commands_list = ("/start", "/help")

subcommands_list = ("To find security, start your massage with 'Find' like 'Find apple'",
                    "To get last price of the security, start your massage with 'Price' and add symbol of the security like 'Price AAPL'",
                    #"To get chart of security, start your massage with 'Chart' and add symbol of the security and timeseries like 'Chart AAPL day'. Chart can be daily(day), weekly(week) and monthly(month)"
                    )

start_message = "Hey, im stock viewer bot\n\nHere is list of all commands:\n{0}\n\n{1}".format('  '.join(commands_list),'\n\n'.join(subcommands_list))

help_message = "Here is list of all commands: {0}\n\n{1}".format(' '.join(commands_list), '\n\n'.join(subcommands_list))

error_message = "Something get wrong.\nTry /help"

#commands

@bot.message_handler(commands = ["start","help"])
def main_response(message):
    
    if message.text == "/start":
        bot.send_message(message.chat.id, start_message)
        
    if message.text == "/help":
        bot.send_message(message.chat.id, help_message)
        
#finder

@bot.message_handler(regexp="^[Ff]ind [A-Za-z0-9\\.]+$")
def response_security(message):

    request_word = message.text.split()[1]
    response = requester(function = "SYMBOL_SEARCH", keywords = request_word)
    
    if "Error Message" in response.keys():
        bot.reply_to(message, error_message)
        
    elif  "bestMatches" in response.keys():
        
        if response["bestMatches"] == []:
            bot.reply_to(message, "I found nothing")
            
        if response["bestMatches"] != []:
            bot.reply_to(message, "I found this:")
            for i in response["bestMatches"]:
                bot.send_message(message.chat.id, format_answer_telegram(i))
                
    else:
         bot.reply_to(message, error_message)

#simple price

@bot.message_handler(regexp="^[Pp]rice [A-Za-z0-9\\.]+$")
def response_security(message):
    
    response = requester(function  = "GLOBAL_QUOTE", symbol = message.text.split()[1])
    
    if response["Global Quote"] == {} or ("Error Message" in response.keys()):
        bot.reply_to(message, error_message)

    if response["Global Quote"] != {}:
        bot.send_message(message.chat.id, format_answer_telegram(response["Global Quote"]))


#chart

@bot.message_handler(regexp="^[Cc]hart [A-Za-z0-9\\.]+ [A-Za-z0-9]+ [A-Za-z0-9]+$")
def response_security(message):
    pass

#ununderstood

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "Sorry, I did not understand.\nTry /help")

#modules

def format_answer_telegram(row_data):
    row_answer = []
    
    unimportant_stats = ("5. marketOpen", "6. marketClose", "9. matchScore") #to skip some param in answer, add his key here
    
    for i in row_data.keys():
        if i in unimportant_stats:
            continue
        else:
            row_answer.append(f"{i.split()[1].capitalize()}: {row_data[i]}")
    answer = "\n".join(row_answer)
    return answer

def requester(**kwargs):
    link = "https://www.alphavantage.co/query?"
    for key, value in kwargs.items():
        link += "{0}={1}&".format(key, value)
    link += f"apikey={stock_token}"
    req = requests.get(link).json()
    return req

#def get_currency(request_currency):
#    currency = requester(function = "SYMBOL_SEARCH", keywords = request_currency)
    

def main():
    bot.infinity_polling()

if __name__ == "__main__":
    main()

"""         
class link_creator:
    def __init__(self, function = function_list[1], symbol):
        self.function = function
        self.symbol = symbol
        self.interval = interval
        
    def create_link_stock_api(**kwargs):
        link = "https://www.alphavantage.co/query?"
        for key, value in kwargs.items():
        link += "{0}={1}&".format(key, value)
        link += f"apikey={stock_token}"
        return link
     
        
function_list = ["TIME_SERIES_DAILY_ADJUSTED", "TIME_SERIES_WEEKLY_ADJUSTED", "TIME_SERIES_MONTHLY_ADJUSTED"]
#function_list = ["TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY", "TIME_SERIES_DAILY_ADJUSTED", "TIME_SERIES_WEEKLY", "TIME_SERIES_WEEKLY_ADJUSTED", "TIME_SERIES_MONTHLY", "TIME_SERIES_MONTHLY_ADJUSTED"]
#interval_list = ["1min","5min","15min","30min","60min"]

"""
