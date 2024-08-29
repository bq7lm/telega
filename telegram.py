import telebot

from extensions import CurrencyConverter, CommandHandler

TOKEN = '7038685934:AAHFBC_TyPnE6LRSraUF9dY9EcOybaMHtNs'
bot = telebot.TeleBot(TOKEN)

if __name__ == "__main__":
    converter = CurrencyConverter()
    command_handler = CommandHandler(bot, converter)
    bot.polling(non_stop=True)
