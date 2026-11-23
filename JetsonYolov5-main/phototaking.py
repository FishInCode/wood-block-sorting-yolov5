import cv2 as cv
import sys
import time

cap0 = cv.VideoCapture(0)
if not cap0.isOpened():
    print("无法打开摄像头0")
    sys.exit()


# flag_num = 0
# flag_show = 0
# cnt = 0
# type = ''
# num = 0

# 设置摄像头分辨率（可选）
cap0.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap0.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
num = 1
while True:
    # 处理摄像头0（实时检测）
    ret0, frame0 = cap0.read()
    # print(1)
    if not ret0:
        print("无法获取视频流")
        break
    # print(2)
    cv.imshow('abc',frame0)
    # 按'q'退出
    if cv.waitKey(1) & 0xFF == ord('q'):
        print(0)
        flag_num = 0
        flag_show = 0
        cnt = 0
        type = ''
        num = 0
        break
    if cv.waitKey(1) & 0xFF == ord('p'):
        cv.imwrite('/home/jetson/Desktop/pictures/'+str(num)+".jpg",frame0)
        print(num)
        print("success to save"+str(num)+".jpg")
        print("--------------------------")
        num += 1



cap0.release()
cv.destroyAllWindows()