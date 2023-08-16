#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import time
import streamlit as st
from PIL import Image
from datetime import datetime, timezone, timedelta


# 録画開始時刻
START_REC_TIME = {"H":8, "M":30, "S":0, "ms":0}
# 録画終了時刻
END_REC_TIME = {"H":9, "M":00, "S":0, "ms":0}
# 動画保存先
VIDEO_DIR = "video"


st.title("Camera Application")
datetime_loc = st.empty()
# カメラデバイス設定
device = user_input = st.text_input("input your video/camera device", "0")
if device.isnumeric():
    # e.g. "0" -> 0
    device = int(device)
image_loc = st.empty()

d_today = datetime.now()
strtime = d_today.strftime('%Y%m%d_%H:%M:%S')
strday = d_today.strftime('%Y%m%d')

save_path = "./{}/{}".format(VIDEO_DIR, strday)
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 動画ファイル保存用の設定
cap = cv2.VideoCapture(device)
fps = int(cap.get(cv2.CAP_PROP_FPS))                        # カメラのFPSを取得
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))                  # カメラの横幅を取得
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))                 # カメラの縦幅を取得
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')         # 動画保存時のfourcc設定（mp4用）
video = cv2.VideoWriter('{}/{}.mp4'.format(save_path, strtime), fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）

while cap.isOpened:
    # 時刻表示設定    
    now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y/%m/%d %H:%M:%S")
    datetime_loc.text(now)
    # 録画時刻設定
    current_time = datetime.now()
    at6am = current_time.replace(hour=START_REC_TIME["H"],
                                 minute=START_REC_TIME["M"],
                                 second=START_REC_TIME["S"],
                                 microsecond=START_REC_TIME["ms"]
                                 )
    at6pm = current_time.replace(hour=END_REC_TIME["H"],
                                 minute=END_REC_TIME["M"],
                                 second=END_REC_TIME["S"],
                                 microsecond=END_REC_TIME["ms"]
                                 )
    # 映像取得
    ret, img = cap.read()
    if ret:
        # テキスト描写
        cv2.putText(img,
            text=str(now),
            org=(10, 30),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.7,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_AA)
        
        # 録画開始/終了条件確認
        if((current_time >= at6am) and (current_time <= at6pm)):
            # 録画処理
            video.write(img)
            cv2.putText(img,
                text="REC",
                org=(570, 30),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.7,
                color=(0, 255, 0),
                thickness=2,
                lineType=cv2.LINE_AA)
            
        # 映像表示設定        
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        image_loc.image(img)

    time.sleep(0.01)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()