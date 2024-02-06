from pyzbar.pyzbar import decode
from PIL import Image
from tkinter import messagebox
import cv2
import numpy as np
import csv
import datetime
import pyperclip
import pyautogui
import tkinter

# カメラをキャプチャする
cam_id = 0
cap = cv2.VideoCapture(cam_id)

def open_camera(title):
    ## カメラをキャプチャする
    #cap = cv2.VideoCapture(cam_id)
    # 初期化
    initial_time = datetime.datetime.now()
    time_cnt = 30        # sec 初期値
    time_interval = 30  # sec 定期実行の時間間隔
    wstr = ""

    # メインループ
    while cap.isOpened():
        # 現在時間 sec
        current_time = (datetime.datetime.now() - initial_time).total_seconds()
        # time_interval毎に実行する
        if current_time >= time_cnt:
            # メッセージボックス（はい・いいえ） 
            ret = tkinter.messagebox.askyesno('確認', 'ウィンドウを閉じますか？')
            if ret == True:
                cv2.waitKey(1)
                break
            # 次回、定期実行する時刻 time_cntを更新
            time_cnt += time_interval

        # フレームを読み取る
        ret, frame = cap.read()
        if ret == True:
            # QRコードを認識する
            d = cv2.QRCodeDetector().detectAndDecode(frame)
            if d[0]:
                # デコードした内容を取得する
                sstr = d[0]
                # 前回と異なる場合
                if wstr != sstr:
                    # コンソールに出力する
                    print(sstr)
                    # 変数を更新する
                    wstr = sstr

                    # クリップボードにコピーする
                    pyperclip.copy(sstr + '\r\n')
                    # クリップボードからペーストする
                    pyautogui.hotkey('ctrl', 'v')

                    # メッセージボックス（はい・いいえ） 
                    ret = tkinter.messagebox.askyesno('認識しました', wstr + '\n\n' + 'ウィンドウを閉じますか？')
                    if ret == True:
                        cv2.waitKey(1)
                        break

                    # 次回、定期実行する時刻 time_cntを更新
                    time_cnt = (datetime.datetime.now() - initial_time).total_seconds() + time_interval

            # ウィンドウに表示する
            cv2.imshow(title, frame) 

            # ウィンドウの表示位置を(100, 200)に設定
            cv2.moveWindow(title, 100, 200)

        # Qキーを押すと終了する
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # カメラを解放する
    cap.release()
    # ウィンドウを閉じる
    cv2.destroyAllWindows()

# カメラを閉じるための関数を定義する
def close_camera():
    # カメラを解放する
    cap.release()
    # ウィンドウを閉じる
    cv2.destroyAllWindows()

    
# メインウィンドウを作成する
root = tkinter.Tk()
root.title("Tkinterでカメラを表示する")
root.geometry("300x100")

# ボタンを作成する
button = tkinter.Button(root, text="カメラを開く", command=lambda: open_camera("Scan the QR Code"))
button1 = tkinter.Button(root, text="カメラを閉じる", command=close_camera)
button.pack()
button1.pack()

# メインループを開始する
root.mainloop()

