import asyncio
import json
from django.core.management.base import BaseCommand
from aiohttp import ClientSession
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from ticker.models import Ticker

class Command(BaseCommand):
    help = 'Starts the Binance WebSocket client'
    running = True  

    def handle(self, *args, **options):
        asyncio.run(self.start_binance_client())

    async def start_binance_client(self):
        channel_layer = get_channel_layer()
        if channel_layer is None:
            self.stdout.write("Error: channel_layer is None")
            return

        symbols = ['btcusdt', 'ethusdt']
        streams = [f"{symbol}@trade" for symbol in symbols]
        url = f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"

        latest_prices = {}

        async def save_latest_prices():
            while self.running:
                await asyncio.sleep(60)
                for symbol, price in latest_prices.items():
                    await sync_to_async(Ticker.objects.create)(
                        symbol=symbol.upper(),
                        price=price
                    )

        asyncio.create_task(save_latest_prices())

        async with ClientSession() as session:
            while self.running:  
                try:
                    async with session.ws_connect(url) as ws:
                        async for msg in ws:
                            if not self.running: 
                                break
                            if msg.type == 1:  
                                data = json.loads(msg.data)
                                trade_data = data['data']
                                symbol = trade_data['s'].lower()
                                price = trade_data['p']
                                latest_prices[symbol] = price
                                await channel_layer.group_send(
                                    "tickers",
                                    {
                                        "type": "send.ticker",
                                        "data": {
                                            "symbol": symbol,
                                            "price": price,
                                            "timestamp": trade_data['T'],
                                        }
                                    }
                                )
                except Exception as e:
                    self.stdout.write(f"Error: {e}, reconnecting...")
                    await asyncio.sleep(5)
