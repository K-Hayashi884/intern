import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from django.utils.timezone import localtime

from .models import Talk, CustomUser
from .utils import (
    create_room_path,
    create_room_path_list,
    get_display_message,
    get_display_time,
    process_message,
)


class ChatConsumer(AsyncWebsocketConsumer):
    """ チャット関係のコンシューマー、トークルームとフレンド欄で使用"""

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
        raw_message = text_data_json['message']
        user_id = int(text_data_json['user_id'])
        partner_id = int(text_data_json['partner_id'])
        # メッセージに改行処理
        message = process_message(raw_message)
        
        # データベースに保存、各種値の取得
        user = await self.get_user(user_id)
        partner = await self.get_user(partner_id)
        talk = await self.save_message(user, partner, raw_message)
        username = user.username
        time = talk.pub_date

        # 表示系処理(時間をトークルーム、フレンド欄に分けて)
        jst_recorded_time = localtime(time)
        now = localtime(timezone.now())

        display_time_friend, display_time_talkRoom = \
            get_display_time(now, time, jst_recorded_time)

        # フレンドに表示するトークメッセージ
        display_message = get_display_message(raw_message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'display_message': display_message,
                'username': username,
                'time_talkRoom': display_time_talkRoom,
                'time_friend': display_time_friend,
                'user_id': str(user_id),
                'room_path': self.room_path
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        display_message = event['display_message']
        username = event['username']
        time_talkRoom = event['time_talkRoom']
        time_friend = event['time_friend']
        user_id = event['user_id']
        room_path = event['room_path']
        # Send message to Websocket
        await self.send(text_data=json.dumps({
            'message': message,
            'display_message': display_message,
            'username': username,
            'time_talkRoom': time_talkRoom,
            'time_friend': time_friend,
            'user_id': user_id,
            'room_path': room_path
        }))

    @database_sync_to_async
    def save_message(self, user, friend, message):
        """ データベースに保存し、そのidを返す """
        talk = Talk.objects.create(talk_from=user, talk_to=friend, content=message)
        return talk
    
    @database_sync_to_async
    def get_user(self, user_id:int):
        """ userの取得 """
        return CustomUser.objects.get(id=user_id)


class SearchConsumer(AsyncWebsocketConsumer):
    """ 検索文のコンシューマー
    検索文を受け取りリアルタイムでデータベースを参照"""
    async def connect(self):
        self.user = self.scope['user']
        await self.accept()

    async def disconnect(self, close_code):
        pass

    # Receive search context from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        search = text_data_json['search']
        info = await self._get_friends_info(search)
        # Send search context to room group
        await self.send(
            text_data=json.dumps({'info': info})
        )

    @database_sync_to_async
    def _get_friends_info(self, search):
        """検索文からデータベースを参照、ルームパスのリストを返す"""
        user_id = self.user.id
        friends = CustomUser.objects.exclude(id=user_id)
        if not search:
            friends_id = friends.values_list("id", flat=True)
        else:
            friends_id = (
                friends
                .filter(username__icontains=str(search))
                .values_list("id", flat=True)
            )
        info = create_room_path_list(user_id, friends_id)
        return info
