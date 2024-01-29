import asyncio
import json
import websockets
import random
import pandas as pd
from misskey import Misskey
import os
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()

TOKEN = os.getenv('TOKEN')
msk = Misskey('misskey.io', i=TOKEN)
WS_URL = 'wss://misskey.io/streaming?i=' + TOKEN

# message.csvを読み込む
df = pd.read_csv("message.csv", header=None)

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

                    # メンションの場合、ランダムなメッセージで応答
                    if notification['type'] == 'mention':
                        mention_note = notification['note']
                        random_message = df.iloc[random.randint(0, len(df) - 1), 1]  # ランダムなメッセージを選択
                        msk.notes_create(text=random_message, replyId=mention_note['id'])

    except websockets.ConnectionClosedError as e:
        print(f"WebSocket接続が切断されました: {e}")

asyncio.run(runner())
