from typing import List


def create_room_path(user1_id:int, user2_id:int) -> int:
    """userを渡すと一意のroom_pathを生成する"""
    return f'{min(user1_id, user2_id)}-{max(user1_id, user2_id)}'


def create_room_path_list(user_id:int, friends_id:List[int]) -> List[int]:
    """ルームパスからリストを作成"""
    info = [create_room_path(user_id, friend_id) for friend_id in friends_id]
    return info


def process_message(message:str):
    """ 長いメッセージに改行処理 """
    letter_oneline = 20
    processed_message = ''
    message = message.replace('<br>', '').replace('\n', '')
    while message:
        if len(message) <= letter_oneline:
            processed_message += message
            message = False
        else:
            processed_message += message[:letter_oneline] + '<br>'
            message = message[letter_oneline:]
    
    return processed_message


def get_display_message(raw_message, max_len=35):
    if len(raw_message) > max_len:
        display_message = raw_message[:max_len] + '...'
    else:
        display_message = raw_message

    return display_message


def get_display_time(now, send_time, jst_recorded_time):
    if jst_recorded_time.date() == now.date():
        display_time_friend = f'{jst_recorded_time:%H:%M}'
    elif jst_recorded_time.year == now.year:
        display_time_friend = f'{jst_recorded_time:%m/%d}'
    else:
        display_time_friend = f'{jst_recorded_time:%m/%d/%Y}'

    display_time_talkRoom = f'{jst_recorded_time:%m/%d<br>%H:%M}'

    return display_time_friend, display_time_talkRoom
