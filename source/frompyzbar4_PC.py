from pyzbar.pyzbar import decode
# from PIL import Image
# from tkinter import messagebox
import cv2
import numpy as np
# import csv
# import datetime
import pyperclip
import pyautogui
# import win32gui
# import win32con

#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
# QRCodeDetectorを生成
#detector = cv2.QRCodeDetector()
wstr = ""
lst = []

# コメント化 2024/02/06
# initial_time = datetime.datetime.now()
# time_cnt = 30        # sec 初期値
# time_interval = 30  # sec 定期実行の時間間隔
title = 'Scan the QR Code'
cam_Status = True

# コメント化 2023/11/24
# def foreground():
#     hwnd = win32gui.FindWindow(None, title)
#     win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM,0,0,0,0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )

while cap.isOpened():
    # コメント化 2024/02/06
    # #現在時間 sec
    # current_time = (datetime.datetime.now() - initial_time).total_seconds()
    # # time_interval毎に実行する
    # if current_time >= time_cnt:
    #     # メッセージボックス（はい・いいえ） 
    #     ret = messagebox.askyesno('確認', 'ウィンドウを閉じますか？')
    #     if ret == True:
    #        cv2.waitKey(1)
    #        break
    #     # 次回、定期実行する時刻 time_cntを更新
    #     time_cnt += time_interval

    ret,frame = cap.read()
    if ret == True:
        d = decode(frame)
        if d:
            #print(d)
            sstr = d[0][0].decode('utf-8', 'ignore')
            #frame = cv2.putText(frame, sstr,(10,50),font,1,(0,255,255),2,cv2.LINE_AA)
            if wstr != sstr:
                #print(sstr)
                wstr = sstr
                # lst.append([sstr, ""])

                # クリップボードにコピー 2023/11/22
                #pyperclip.copy(sstr + '\n')    # 2024/02/05 コメント化
                pyperclip.copy(sstr + '\r\n')   # 2024/02/05 ターミナルにキャリッジリターン＋ラインフィード
                #pyperclip.copy(sstr + '\r')    # 2024/02/05 ターミナルにキャリッジリターン
                #pyperclip.copy(sstr)           # 2024/02/05 ターミナルなし
                # クリップボードからペースト 2023/11/22
                pyautogui.hotkey('ctrl', 'v')
                
                #pyperclip.copy('\r\n')
                #pyautogui.hotkey('ctrl', 'v')
                
                # コメント化 2024/02/06
                # # メッセージボックス（はい・いいえ） 
                # ret = messagebox.askyesno('認識しました', wstr + '\n\n' + 'ウィンドウを閉じますか？')
                # if ret == True:
                #     cv2.waitKey(1)
                #     break

                # コメント化 2024/02/06
                # # 次回、定期実行する時刻 time_cntを更新
                # time_cnt = (datetime.datetime.now() - initial_time).total_seconds() + time_interval

        cv2.imshow(title, np.array(frame)) 

        if cam_Status == True:
            # 開始時はウィンドウの表示位置を(10, 20)に設定
            cv2.moveWindow(title, 10, 20)
            cam_Status = False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
# コメント化 2023/11/22
# #print(lst)
# f = open('C:\QrDecodeSample\OUT\out3.csv', 'w', newline="")
# writer = csv.writer(f)
# writer.writerows(lst)
# f.close()
cv2.destroyAllWindows()