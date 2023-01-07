import requests

# функция запрашивает список валют и возвращает стоимость заданной
def get_currency_value_from_api(rate):

    rates = requests.get('https://www.cbr-xml-daily.ru/latest.js').json()['rates']
    return rates[rate]

# функция расчета стоимости заданной валюты в заданном количестве в рублях
def get_total_currency_value(rate, count, discount):
    if discount < 1:
        raise ValueError("Отрицательная комиссия")

    currency_value = get_currency_value_from_api(rate)
    currency_total = currency_value * count - discount

    return currency_total

rates = requests.get('https://www.cbr-xml-daily.ru/latest.js').json()['rates']
print(rates)
print(get_currency_value_from_api('GBP'))
print(get_currency_value_from_api('BYN')*100_000-100)