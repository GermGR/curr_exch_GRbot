import telebot
import requests
import json
from token_2 import TOKEN #Импортируем наш ТОКЕН из файла

bot = telebot.TeleBot(TOKEN)

# URL для получения списка валют
url = 'https://www.cbr-xml-daily.ru/daily_json.js'

# Отправка GET-запроса к API Центробанка
response = requests.get(url)

# Словарь для хранения данных о валютах
currency_dict = {}

# Проверка успешности запроса
if response.status_code == 200:
    # Получение данных в формате JSON
    data = response.json()

    # Извлечение информации о валютах
    currencies = data['Valute']

    # Заполнение словаря данными о валютах
    for currency_key, currency_value in currencies.items():
        name = currency_value['Name']
        currency_dict[currency_key] = name
    currencies_dict = (str(currency_dict).replace(', ',',\n '))
        
else:
    print("Ошибка при обращении к API Центробанка")

#Комманды Старт и Хэлп
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, версия 0.071, который показывает текущий курс валют по отношению к рублю.\n Напиши название валют для получения курса (Например 'USD').\n Посмотреть список доступных валют нажми /values.\n Данные получены с сайта Центробанка РФ.")
#Комманды Хэлп
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Напиши название валют для получения курса(Например 'USD'). \n Нужно написать именно мировую абривиатуру валюты. \n Посмотреть список доступных валют нажми /values.")

#Комманда Values показывает список доступных валют, которые мы взяли с сайта Центробанка
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    text = f"{currencies_dict}"
    bot.reply_to(message, text)

#Работа с запросом по конкретной валюте
@bot.message_handler(func=lambda message: message.text in currency_dict.keys())
def send_currency_rate(message):
    currency_key = message.text
    if currency_key in currency_dict:
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if currency_key in data['Valute']:
                currency_data = data['Valute'][currency_key]
                rate = currency_data['Value']
                text = f"Текущий курс {currency_data['Name']} к рублю: {rate} ₽"
                bot.reply_to(message, text)
            else:
                bot.reply_to(message, "Данные по выбранной валюте отсутствуют")
        else:
            bot.reply_to(message, "Ошибка при получении данных с сервера Центробанка")
    else:
        bot.reply_to(message, "Выбранная валюта недоступна")
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.reply_to(message, "Я не понимаю ваш запрос. Пожалуйста, используйте команду /help для получения информации о доступных командах.")

    
bot.polling(none_stop=True)