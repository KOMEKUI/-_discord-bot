import json
import os

# ファイル名
filename = 'channel_status.json'

class ChannelStatus:
    def __init__(self, channel_id, is_active):
        self.channel_id = str(channel_id)  # channel_idを常に文字列として扱う
        self.is_active = is_active

    def to_dict(self):
        return {self.channel_id: self.is_active}

# データを保存する関数
def save_channel_status(channel_status):
    existing_data = load_all_channel_status()
    existing_data[channel_status.channel_id] = channel_status.is_active  # 同じキーの場合は上書き

    print("Saving data:", existing_data)  # デバッグ: 書き込み内容を確認

    with open(filename, 'w') as file:
        json.dump(existing_data, file)

# データを読み取る関数
def load_all_channel_status():
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

# 特定のchannel_idのステータスを取得する関数
def load_channel_status(channel_id):
    existing_data = load_all_channel_status()
    str_channel_id = str(channel_id)  # channel_idを文字列に変換
    if str_channel_id in existing_data:
        return ChannelStatus(str_channel_id, existing_data[str_channel_id])
    return None

# ステータスが変更されたら保存する例
def update_channel_status(new_channel_id, new_is_active):
    current_status = load_channel_status(new_channel_id)

    if not current_status or current_status.is_active != new_is_active:
        new_status = ChannelStatus(new_channel_id, new_is_active)
        save_channel_status(new_status)
        print(f"Status for Channel ID {new_channel_id} updated and saved.")
    else:
        print(f"No changes detected for Channel ID {new_channel_id}.")