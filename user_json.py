import json
import os

# ファイル名
filename = 'user_status.json'

class UserStatus:
    def __init__(self, user_id, user_level=0, message_times=0):
        self.user_id = str(user_id)  # user_idを常に文字列として扱う
        self.user_level = user_level
        self.message_times = message_times

    def to_dict(self):
        # user_idをキーにしてuser_levelとmessage_timesを含む辞書を返す
        return {
            'user_level': self.user_level,
            'message_times': self.message_times
        }

    @staticmethod
    def from_dict(user_id, data):
        # user_idとデータからUserStatusオブジェクトを生成
        return UserStatus(user_id, data.get('user_level', 0), data.get('message_times', 0))

# データを保存する関数
def save_user_status(user_status):
    # 既存のデータを読み込む
    existing_data = load_all_user_status()
    # user_idをキーにしてユーザーデータを更新または追加
    existing_data[user_status.user_id] = user_status.to_dict()

    with open(filename, 'w') as file:
        json.dump(existing_data, file)

# データを読み取る関数
def load_all_user_status():
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

# 特定のuser_idのステータスを取得する関数
def load_user_status(user_id):
    existing_data = load_all_user_status()
    str_user_id = str(user_id)  # user_idを文字列に変換
    if str_user_id in existing_data:
        return UserStatus.from_dict(str_user_id, existing_data[str_user_id])
    # 存在しない場合、user_level=0とmessage_times=0でUserStatusを返す
    return UserStatus(str_user_id, user_level=0, message_times=0)

# ユーザーのレベルやメッセージ数を更新する
def update_user_status(user_id, new_level=None, add_message_times=0):
    user_status = load_user_status(user_id)

    # レベルとメッセージ数を更新
    if new_level is not None:
        user_status.user_level = new_level
    user_status.message_times += add_message_times
    if user_status.message_times < 0:
        user_status.message_times = 0

    # データを保存
    save_user_status(user_status)
    print(f"Status for User ID {user_id} updated and saved.")


def update_all_user_status(add_message_times=0):
    existing_data = load_all_user_status()
    for user_id in existing_data:
        update_user_status(user_id=user_id, add_message_times = add_message_times)