import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import datetime
import channel_json
import user_json
import Gemini_api

# 決まり文句
intents = discord.Intents.default()
intents.message_content=True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ファイル読み取り
load_dotenv(dotenv_path="token.env")
load_dotenv(dotenv_path="image-url.env")

# Botのトークン
TOKEN = os.getenv("BOT_TOKEN")

# Bot開始時にスラッシュコマンドの同期
@client.event
async def on_ready():
    await tree.sync()
    print(f"スラッシュコマンドの同期をしました")

# スラッシュコマンド同期させるデータ作成
@tree.command(name="start_watch", description="寝ない子悪い子の監視を開始します")
# スラッシュコマンド start_watchの処理内容
async def start_watch(interaction: discord.Interaction):
    # channel_id を取得
    this_channel_id = interaction.channel_id
    status = channel_json.load_channel_status(f"{this_channel_id}")
    print(status.is_active)
    try:
        is_active = status.is_active
    except:
        is_active = False
    if is_active != True:
        # 表示される文章
        embed = discord.Embed(
            title="監視開始",
            description="このチャンネルで寝ない悪い子を探し出します",
            color=0x0000ff
            )
        embed.set_thumbnail(url=os.getenv("namahage_aka_img"))
        # チャンネルのステータスを更新する例
        channel_json.update_channel_status(f"{this_channel_id}", True)
        await interaction.response.send_message(embed=embed) # 送信
        return
    await interaction.response.send_message(content="すでに開始しています", ephemeral=True,delete_after=20)

# スラッシュコマンド同期させるデータ作成
@tree.command(name="end_watch", description="寝ない子悪い子の監視を終了します")
# スラッシュコマンド end_watch の処理内容
async def end_watch(interaction: discord.Interaction):
    # channel_id を取得
    this_channel_id = interaction.channel_id
    status = channel_json.load_channel_status(f"{this_channel_id}")
    print(status.is_active)
    try:
        is_active = status.is_active
    except:
        is_active = False
    if is_active != False:
        # 表示される文章
        embed = discord.Embed(
            title="監視終了",
            description="このチャンネルで寝ない悪い子を探すのを辞め、家に帰ります",
            color=0x0000ff
            )
        embed.set_thumbnail(url=os.getenv("home_img"))
        # チャンネルのステータスを更新する例
        channel_json.update_channel_status(f"{this_channel_id}", False)
        await interaction.response.send_message(embed=embed) # 送信
        return
    await interaction.response.send_message(content="すでに終了しています", ephemeral=True,delete_after=20)

# スラッシュコマンド同期させるデータ作成
@tree.command(name="show_level", description="あなたのレベルを表示します")
# スラッシュコマンド end_watch の処理内容
async def show_level(interaction: discord.Interaction):
    embed = await create_level_embed(interaction=interaction)
    await interaction.response.send_message(embed=embed)

@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    this_channel_id = message.channel.id
    status = channel_json.load_channel_status(f"{this_channel_id}")
    if status.is_active:
            dt_now = datetime.datetime.now()
            now_hour = dt_now.hour
            if now_hour > 1 and now_hour < 6:
                this_user_id = message.author.id
                user_json.update_user_status(this_user_id,add_message_times=1)
                this_user_status = user_json.load_user_status(this_user_id)
                if check_user_level(this_user_status.user_level,this_user_status.message_times):
                    now_user_level = this_user_status.user_level + 1
                    user_json.update_user_status(this_user_id,new_level=now_user_level)
                    embed = await create_level_embed(message = message)
                    await message.channel.send(embed=embed)
                if (this_user_status.message_times % 4) == 0:
                    send_message = Gemini_api.create_message(message.content)
                    await message.channel.send(f"<@{this_user_id}>\n{send_message}")

async def create_level_embed(message=None,interaction=None):
    if message:
        this_user_id = message.author.id
        this_guild = message.guild
        member = await this_guild.fetch_member(this_user_id)
        level_up_msg = "にあがりました"
    if interaction:
        this_user_id = interaction.user.id
        this_guild = interaction.guild
        member = await this_guild.fetch_member(this_user_id)
        level_up_msg = ""
    this_user_status = user_json.load_user_status(this_user_id)
    now_user_level = this_user_status.user_level
    if now_user_level == 0:
        Alias = "## よい子"
    if now_user_level == 1:
        Alias = "## よい子？"
    if now_user_level == 2:
        Alias = "## 怪しい子"
    if now_user_level == 3:
        Alias = "## 夜なめ子🍄‍🟫"
    if now_user_level == 4:
        Alias = "## 夜の警備員💂"
    if now_user_level == 5:
        Alias = "## 悪い子 👊確定！"
    embed = discord.Embed( # Embedを定義する
                        title=f"**夜更かしレベル{now_user_level}**{level_up_msg}", # 夜更かしレベル
                        color=0xffff00, # フレーム色指定(今回は緑)
                        description=Alias # 二つ名的な？
                        )
    embed.set_author(name=member.display_name, # ユーザー表示名
                    icon_url=member.display_avatar.url # ユーザーアイコン
                    )
    return embed

def check_user_level(now_user_level,now_exp):
    if now_exp >= 0:
        user_level = 0
    if now_exp >= 10:
        user_level = 1
    if now_exp >= 22:
        user_level = 2
    if now_exp >= 43:
        user_level = 3
    if now_exp >= 83:
        user_level = 4
    if now_exp >= 101:
        user_level = 5
    if now_user_level < user_level:
        return True
    return False

client.run(TOKEN)