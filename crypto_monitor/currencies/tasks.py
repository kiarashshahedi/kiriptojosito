import os
from celery import shared_task
from binance.client import Client
from .models import Currency, CurrencyChange

client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET_KEY'))
currencies = ["1000SATSUSDT", "1INCHUSDT", "AAVEUSDT", "ACAUSDT", "ACEUSDT", "ACHUSDT", "ACMUSDT", "ADAUSDT"]

@shared_task
def check_price_changes():
    for symbol in currencies:
        try:
            ticker = client.get_ticker(symbol=symbol)
            price_change_percent = float(ticker['priceChangePercent'])

            if abs(price_change_percent) > 1.0:
                CurrencyChange.objects.create(
                    symbol=symbol,
                    price_change_percent=price_change_percent,
                    last_price=float(ticker['lastPrice'])
                )

        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
