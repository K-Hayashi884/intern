import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Talk, CustomUser
from django.utils.timezone import localtime
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_path = self.scope['url_route']['kwargs']['room_path']
        self.room_group_name = 'chat_%s' % self.room_path

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        partner_id = text_data_json['partner_id']
        
        talk_id = await self.save_message(user_id, partner_id, message)
        username = await self.get_name(user_id)
        time = await self.get_time(talk_id)

        jst_recorded_time = localtime(time)
        now = localtime(timezone.now())
        if jst_recorded_time.date() == now.date():
            display_time_friend = f'{jst_recorded_time:%H:%M}'
        elif jst_recorded_time.year == now.year:
            display_time_friend = f'{jst_recorded_time:%m/%d}'
        else:
            display_time_friend = f'{jst_recorded_time:%m/%d/%Y}'

        display_time_talkRoom = f'{jst_recorded_time:%m/%d<br>%H:%M}'


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'time_talkRoom': display_time_talkRoom,
                'time_friend': display_time_friend,
                'user_id': user_id

            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        time_talkRoom = event['time_talkRoom']
        time_friend = event['time_friend']
        user_id = event['user_id']

        # Send message to Websocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time_talkRoom': time_talkRoom,
            'time_friend': time_friend,
            'user_id': user_id
        }))

    @database_sync_to_async
    def save_message(self, user_id, friend_id, message):
        """ データベースに保存し、そのidを返す """
        user = CustomUser.objects.get(id=int(user_id))
        friend = CustomUser.objects.get(id=int(friend_id))
        talk = Talk(talk_from=user, talk_to=friend, \
          content=message)
        talk.save()
        return talk.id
    
    @database_sync_to_async
    def get_name(self, user_id):
        """ usernameの取得 """
        return CustomUser.objects.get(id=int(user_id)).username
    
    @database_sync_to_async
    def get_time(self, talk_id):
        """ 送信時間の取得 """
        return Talk.objects.get(id=int(talk_id)).pub_date

    
