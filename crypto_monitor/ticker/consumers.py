from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TickerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("tickers", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("tickers", self.channel_name)

    async def send_ticker(self, event):
        await self.send(text_data=json.dumps(event['data']))