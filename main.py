# discord.py
import configparser
import datetime
import os

import discord

# 起動
print('起動しました')

# コンフィグ
config = configparser.ConfigParser()
config.read('config.ini', encoding='UTF-8')

ss_channel = int(config['VC']['CHANNEL'])

# 起動
print(f"設定を読み込みました: channel={ss_channel}")


# 接続に必要なオブジェクトを生成
bot = discord.Client()


# 起動時に動作する処理
@bot.event
async def on_ready():
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

    # 指定チャンネルから抜けた時
    if before.channel is None or before.channel.id != ss_channel:
        return

    # 関係ないチャンネル
    if after.channel is not None and after.channel == after.channel.guild.afk_channel:
        return

    # ミュート解除
    await member.edit(mute=False)


# 初期化
print('初期化しました')

# Botの起動とDiscordサーバーへの接続
bot.run(os.environ["DISCORD_TOKEN"])
