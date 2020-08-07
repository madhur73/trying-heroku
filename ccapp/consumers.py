from channels.generic.websocket import WebsocketConsumer
import json

from django.core.cache import cache


class TickerConsumer(WebsocketConsumer):

    def connect(self):
        cryptocoin = self.scope['url_route']['kwargs']['cryptocoin']
        source = self.scope['url_route']['kwargs']['source']
        self.ticker_code = cryptocoin + source
        super().connect()
        self.send(text_data=json.dumps({
            'message': f'connected'
        }))
        self.price_update({
            'price': cache.get(self.ticker_code)
        })
        

    def price_update(self, event):
        price = event['price']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'price': price,
        }))