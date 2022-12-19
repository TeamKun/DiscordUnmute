# discord.py
import configparser
import os
import discord

# 起動
print('起動しました')

# コンフィグ
config = configparser.ConfigParser()
config.read('config.ini', encoding='UTF-8')

# チャンネル
ss_channel = int(config['VC']['CHANNEL'])
channel = None

# 接続時ミュートモード
join_mute_enabled = config['VC.JOIN_MUTE']['ENABLED'] == 'True'
join_mute_ignore_users = [int(x) for x in config['VC.JOIN_MUTE']['IGNORED_USERS'].split(',')] 

# 起動
print(f"設定を読み込みました: channel={ss_channel}")


# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
bot = discord.Client(intents=intents)


# 起動時に動作する処理
@bot.event
async def on_ready():
    global channel
    channel = bot.get_channel(ss_channel)
    if channel is None:
        print('チャンネルが見つかりません')
        return

    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')


# VCのメンバー移動時の処理
@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # 移動していない
    if before.channel == after.channel:
        return

    # 指定チャンネルから他のチャンネルに移動したとき (VCから抜けたときはミュート解除できないので無視)
    if before.channel is not None and before.channel.id == ss_channel and after.channel is not None:
        # 関係ないチャンネル
        if after.channel is not None and after.channel == after.channel.guild.afk_channel:
            return

        # ミュート解除
        await member.edit(mute=False)

    # 指定チャンネルに入った時 && 発言権限を持っているとき
    elif join_mute_enabled and after.channel is not None and after.channel.id == ss_channel:
        # 除外ユーザーは無視
        if member.id in join_mute_ignore_users:
            return

        # 発言権限を持っていない場合は無視
        if not channel.permissions_for(member).speak:
            return

        # ミュート
        await member.edit(mute=True)


# 初期化
print('初期化しました')

# Botの起動とDiscordサーバーへの接続
bot.run(os.environ["DISCORD_TOKEN"])
