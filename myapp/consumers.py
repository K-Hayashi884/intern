from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'talk_%s' % self.room_name
        # print(self.scope)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = text_data_json['sender']
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender, 
                'message': message
            }
        )

    def chat_message(self, event):
        sender = event['sender']
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'sender': sender,
            'message': message,
        }))
        