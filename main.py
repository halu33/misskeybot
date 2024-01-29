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
api.token = os.getenv('TOKEN')

#ノート
#api.notes_create(text='Hello World') #test用

#message.csv読み込み
df = pd.read_csv("message.csv", header=None)

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