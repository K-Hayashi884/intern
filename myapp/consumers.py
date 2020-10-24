import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['name']
        self.room_group_name = 'chat_%s' % self.room_name

        #join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        #leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    #receive message from websocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data) #loads : デコード（エンコードされた方をもとに戻す）
        message = text_data_json['message']
        send_from = self.scope["user"].username
        send_to = self.room_name

        #send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'send_to': send_to,
                'send_from': send_from,
            }
        )

    #receive message from room group
    def chat_message(self, event):
        message = event["message"]
        Message.objects.create(
            message=event["message"],
            send_from=User.objects.get(username=event["send_from"]),
            send_to=User.objects.get(username=event["send_to"]),
        )

        #send message to websocket
        self.send(text_data=json.dumps({ #dumps関数：データをJSON形式にエンコード（変換）
            'message': message,
        }))
