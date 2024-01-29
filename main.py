import asyncio
import json
import websockets
import os
import time
import datetime
import random
import pandas as pd
from misskey import Misskey
from dotenv import load_dotenv

#環境変数
load_dotenv()

#初期化
api = Misskey('misskey.io')
TOKEN = os.getenv('TOKEN')
api.token = os.getenv('TOKEN')
WS_URL = 'wss://misskey.io/streaming?i=' + TOKEN

#ノート
#api.notes_create(text='Hello World') #test用

#message.csv読み込み
df = pd.read_csv("message.csv", header=None)

#通知受け取り
async def runner():
    try:
        async with websockets.connect(WS_URL) as ws:
            await ws.send(json.dumps({
                "type": "connect",
                "body": {
                    "channel": "main",
                    "id": "test"
                }
            }))

            while True:
                data = json.loads(await ws.recv())
                if data['type'] == 'channel' and data['body']['type'] == 'notification':
                    notification = data['body']['body']

                    if notification['type'] == 'mention':
                        mention_note = notification['note']
                        random_message = df.iloc[random.randint(0, len(df) - 1), 1]
                        api.notes_create(text=random_message, replyId=mention_note['id'])

    except websockets.ConnectionClosedError as e:
        print(f"WebSocket接続が切断されました: {e}")

asyncio.run(runner())

#同じ内容の投稿を連続で行わないための変数
x = 100000

while True:
    # ランダムでノート
    y = random.randint(0, df.shape[0] - 1)
    if x != y:
        api.notes_create(text=df.iloc[y, 1])
        print(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
        print("-------------------------------")
        print(df.iloc[y, 1])
        print()
        x = y
    #600秒待機
    time.sleep(600)