import sys
import cv2 
import imutils
import time  # 新增time模块
from yoloDet import YoloTRT
import uart
import random

flag_show = 1
cnt = 0
flag_num = 1
object1 = ''
num = 0
type = ''


# 初始化YOLO模型
model = YoloTRT(
    library="wcc/build/libmyplugins.so",
    engine="wcc/build/wcc.engine",
    conf=0.2,
    yolo_ver="v5"
)

# 使用摄像头（0代表默认摄像头）
cap0 = cv2.VideoCapture(0)

if not cap0.isOpened():
    print("无法打开摄像头0")
    sys.exit()

# 设置摄像头分辨率（可选）
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 初始化摄像头1的计时器和FPS
last_time_cam1 = 0
last_fps1 = 0

while True:
    # 处理摄像头0（实时检测）
    ret0, frame0 = cap0.read()
    if not ret0:
        print("无法获取视频流")
        break
    
    detections0, t0 = model.Inference(frame0)

    if flag_show == 1 and flag_num == 0:
        if cnt >= 50:
            if object1 == 'eaten' and flag_num == 0:
                flag_num = 1
                num = random.randint(600,800)
                type = 'worm-eaten hard'
                
            elif object1 == 'scar' and flag_num == 0:
                flag_num = 1
                num = random.randint(800,1100)
                type = 'scar mid'
            
            elif object1 != 'eaten' and flag_num == 0 and object1 != 'scar':
                flag_num = 1
                type = 'good'
                num = random.randint(1100,2000)
        else:
            cnt += 1

    # 绘制检测结果
    for obj in detections0:Serial_Receive()
        box = obj['box']
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        if (200<=(x1+x2)/2<=400) and flag_show != 1:
            uart.Serial_Send(0x01,0x01)
            object1 = obj['class']
            flag_show = 1
        
        cv2.rectangle(frame0, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{obj['class']} {obj['conf']:.2f}"
        cv2.putText(frame0, label, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        if flag_show == 0:
            uart.Serial_Send(0x01,0x01)
            object1 = 'good'
            flag_show = 1

    # 显示实时FPS
    fps0 = 1.0 / t0
    if flag_show == 1 and cnt>=50:
        cv2.putText(frame0, f"{num}", (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame0, type, (20,110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame0, f"FPS: {fps0:.2f}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Camera0 Detection", frame0)

    # 按'q'退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        flag_num = 0
        flag_show = 0
        cnt = 0
        type = ''
        num = 0

cap0.release()
cv2.destroyAllWindows()