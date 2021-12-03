import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Talk, CustomUser
from django.utils.timezone import localtime
from django.utils import timezone

from .views import create_room_path, process_message



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
        user_id = text_data_json['user_id']
        partner_id = text_data_json['partner_id']
        # メッセージに改行処理
        message = process_message(raw_message)
        
        # データベースに保存、各種値の取得
        talk_id = await self.save_message(user_id, partner_id, raw_message)
        username = await self.get_name(user_id)
        time = await self.get_time(talk_id)

        # 表示系処理(時間をトークルーム、フレンド欄に分けて)
        jst_recorded_time = localtime(time)
        now = localtime(timezone.now())
        if jst_recorded_time.date() == now.date():
            display_time_friend = f'{jst_recorded_time:%H:%M}'
        elif jst_recorded_time.year == now.year:
            display_time_friend = f'{jst_recorded_time:%m/%d}'
        else:
            display_time_friend = f'{jst_recorded_time:%m/%d/%Y}'

        display_time_talkRoom = f'{jst_recorded_time:%m/%d<br>%H:%M}'

        # フレンドに表示するトークメッセージ
        cut_length = 25
        if len(raw_message) > cut_length:
            display_message = raw_message[:cut_length] + '...'
        else:
            display_message = raw_message
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


class SearchConsumer(AsyncWebsocketConsumer):
    """ 検索文のコンシューマー
    検索文を受け取りリアルタイムでデータベースを参照"""
    async def connect(self):
        self.user = self.scope['user']
        print(1)
        await self.accept()

    async def disconnect(self, close_code):
        pass

     # Receive search context from WebSocket
    async def receive(self, text_data):
        print(2)
        text_data_json = json.loads(text_data)
        search = text_data_json['search']
        print(self.user)
        info = await self.get_friends_info(search)
        print(info)   
         # Send search context to room group
        await self.send(text_data=json.dumps({
            'info': info
        })
        )

    @database_sync_to_async
    def get_friends_info(self, search):
        """検索文からデータベースを参照、ルームパスのリストを返す"""
        print(5)
        friends = CustomUser.objects.exclude(id=self.user.id).filter(username__icontains=str(search))
        all_friends =  CustomUser.objects.all().exclude(id=self.user.id)
        print(friends)
        if search == '':
            info = create_room_path_list(self.user, all_friends)
        if friends:
            info = create_room_path_list(self.user, friends)
        else:
            info = []
        
        print(7)
        return info

# ルームパスからリストを作成
def create_room_path_list(user, friends):
    info = []
    for friend in friends:
        room_path = create_room_path(user, friend)
        info.append(room_path)

    return info



