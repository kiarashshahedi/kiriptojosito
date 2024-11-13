import json
import asyncio
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer

class BinanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.symbols = ["1000SATSUSDT", "1INCHUSDT", "AAVEUSDT", "BTCUSDT", "ETHUSDT", "ADAUSDT", "XRPUSDT"] # Example list

        # Start receiving data from Binance WebSocket
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.fetch_binance_data())

    async def disconnect(self, close_code):
        self.loop.stop()

    async def fetch_binance_data(self):
        uri = "wss://stream.binance.com:9443/ws"
        symbols = [symbol.lower() + "@kline_1m" for symbol in self.symbols]
        async with websockets.connect(uri) as websocket:
            params = {
                "method": "SUBSCRIBE",
                "params": symbols,
                "id": 1
            }
            await websocket.send(json.dumps(params))

            while True:
                message = await websocket.recv()
                data = json.loads(message)

                if "k" in data:
                    kline = data['k']
                    symbol = kline['s']
                    close_price = float(kline['c'])
                    open_price = float(kline['o'])

                    # Calculate percentage decrease
                    if close_price < open_price:
                        decrease = ((open_price - close_price) / open_price) * 100
                        await self.send(text_data=json.dumps({
                            'symbol': symbol,
                            'percentage_decrease': round(decrease, 2)
                        }))
