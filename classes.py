import json
import requests
from config import my_keys

class ConvertionException(Exception):
    pass

class CryptoConvertor:
    @staticmethod
    def convertor_exception(crypto:str, currency:str, amount:str):
        if crypto == currency:  # искл - нельзя перевести биткоин в биткоин
            raise ConvertionException(f'невозможно {crypto} перевести в {currency}')
        try:
            crypto_ticker = my_keys[crypto]  # тикер - значения my_keys: 'BTC' или 'ATOM'
        except KeyError:
            raise ConvertionException('неправильно введено название криптовалюты')
        try:
            currency_ticker = my_keys[currency]
        except KeyError:
            raise ConvertionException('неправильно введено название валюты')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('количество переводимой валюты должно быть числом')
        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={crypto_ticker}&tsyms={currency_ticker}')  # делаем ссылку динамической - f {}
        crypto_price = json.loads(r.content)[currency_ticker]  # текущая цена 1 битка в долларах
        return crypto_price