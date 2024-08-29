import requests
import json
class CurrencyConverter:
    def __init__(self):
        self.keys = {
            'биткоин': 'BTC',
            'рубль': 'RUB',
            'доллар': 'USD',
            'евро': 'EUR',
        }

    def convert(self, quote, base, amount):
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={self.keys[quote]}&tsyms={self.keys[base]}')
        if r.status_code != 200:
            raise Exception("Ошибка при получении данных от API.")
        
        price = json.loads(r.content)[self.keys[base]]
        total_cost = price * amount
        return total_cost

class CommandHandler:
    def __init__(self, bot, converter):
        self.bot = bot
        self.converter = converter
        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.start_command(message)
            
        @self.bot.message_handler(commands=['report'])
        def report(message):
            self.report_command(message)

        @self.bot.message_handler(commands=['help'])
        def help_command(message):
            self.help_command(message)

        @self.bot.message_handler(commands=['values'])
        def values_command(message):
            self.values_command(message)

        @self.bot.message_handler(content_types=["text"])
        def convert_command(message):
            self.convert_command(message)
    
    def start_command(self, message):
        self.bot.send_message(message.chat.id, 'Приветствую. Чем могу помочь?')
    def report_command(self, message):
        self.bot.send_message(message.chat.id, 'По всем вопросам @bq7lm')
    def help_command(self, message):
        self.bot.send_message(message.chat.id, 'Чтобы начать работу введите команду в формате:\n<валюта> <переводимая валюта> <кол-во переводимой валюты>\nПримеры:\n▪️ рубль доллар 100\n▪️ биткоин евро 2')

    def values_command(self, message):
        text = 'Доступные валюты:'
        for key in self.converter.keys.keys():
            text += f'\n▪️ {key}'
        self.bot.send_message(message.chat.id, text)

    def convert_command(self, message):
        try:
            quote, base, amount = message.text.lower().split(' ')
            amount = float(amount)

            total_cost = self.converter.convert(quote, base, amount)
            self.bot.send_message(message.chat.id, f'Цена {amount} {quote} в {base}: {total_cost}')
        
        except (ValueError, KeyError):
            self.bot.send_message(message.chat.id, 'Неверный формат команды. Используйте: <валюта> <переводимая валюта> <кол-во переводимой валюты>')
