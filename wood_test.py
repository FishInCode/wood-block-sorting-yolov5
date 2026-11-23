import sys
import cv2 
import numpy as np
import time
import uart
import imutils
from yoloDet import YoloTRT1,YoloTRT2,YoloTRT

# cnt = 0 #count the number of fractures wood
t = 0
# 初始化YOLO模型
# # model of wood
model = YoloTRT(
    library="wcc/build/libmyplugins.so",
    engine="wcc/build/wcc.engine",
    conf=0.8,
    yolo_ver="v5"
)

# model1 = YoloTRT1(
#     library="woodself/build/libmyplugins.so",
#     engine="woodself/build/woodself.engine",
#     conf=0.8,
#     yolo_ver="v5"
# )
#
# # model of fractures
# model2 = YoloTRT2(
#     library="wood/build/libmyplugins.so",
#     engine="wood/build/woodbest.engine",
#     conf=0.5,
#     yolo_ver="v5"
# )

# 使用摄像头（0代表默认摄像头）
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("无法打开摄像头")
    sys.exit()

# 设置摄像头分辨率（可选）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法获取视频流")
        break
    
    # 调整帧大小以加速处理
    frame = imutils.resize(frame, width=600)
    frame = frame[80:340,200:400]
    frame = imutils.resize(frame,width=520,height = 400)
    # 执行目标检测
    detections, t = model.Inference(frame)
    
    # 在帧上绘制检测结果
    for obj in detections:
        className = obj['class']
        print(className)
        if className == "wood":
            uart.Serial_Send(0x01,
                             0x0B)  # send message to let stm32 delays certain ms that makes wood stop right below. [stop csd message]
            box = obj['box']
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])

            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # time.sleep(0.2)
            wood_frame = frame[int(y1):int(y2), int(x1):int(x2)]
            cv2.imshow("wood region", wood_frame)
        if className == "knot" or className == "knot" or className == "knot":
            uart.Serial_Send(0x02, 0x0C)  # send message to grab the fractured wood
            box = obj['box']
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            print("has fractures!")
            time.sleep(0.2)
            break

        # if className == 0:
        #     uart.Serial_Send(0x01,
        #                      0x0B)  # send message to let stm32 delays certain ms that makes wood stop right below. [stop csd message]
        #     box = obj['box']
        #     x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        #
        #     # 绘制边界框
        #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #     # time.sleep(0.2)
        #     wood_frame = frame[int(y1):int(y2), int(x1):int(x2)]
        #     cv2.imshow("wood region", wood_frame)
        # if className == 1 or className == 2 or className == 3:
        #     uart.Serial_Send(0x02, 0x0C)  # send message to grab the fractured wood
        #     box = obj['box']
        #     x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        #     print("has fractures!")
        #     time.sleep(0.2)
        #     break

    # 计算并显示FPS
    fps = 1.0 / t
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # 显示结果
    cv2.imshow("Camera Detection", frame)
    t = 0
    # t1 = t2 = 0
    # 按'q'退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        # uart.Serial_Send(0x01,0x0B)    #send message to let stm32 delays certain ms that makes wood stop right below. [stop csd message]
        # box1 = obj1['box']
        # x1, y1, x2, y2 = int(box1[0]), int(box1[1]), int(box1[2]), int(box1[3])
        #
        # # 绘制边界框
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # # time.sleep(0.2)
        #
        # wood_frame = frame[int(y1):int(y2),int(x1):int(x2)]
        #
        # cv2.imshow("wood region",wood_frame)
        # # detections_2, t2 =model2.Inference(wood_frame)
        # for obj2 in detections_2:
        #     if obj2 != None:
        #         cnt += 1
        #         box2 = obj2['box']
        #         x1, y1, x2, y2 = int(box2[0]), int(box2[1]), int(box2[2]), int(box2[3])
        #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #
        #         # 显示类别和置信度
        #         label = f"{obj2['class']} {obj2['conf']:.2f}"
        #         cv2.putText(frame, label, (x1, y1-10),
        #                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        #         cv2.putText(frame, label, (x1, y1-10),
        #                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        #
        # if cnt != 0:
        #     cnt = 0
        #     uart.Serial_Send(0x02,0x0C)    #send message to grab the fractured wood
        #     print("has fractures!")
        #     time.sleep(0.2)
        #     break

# t1 = t2 = 0
t = 0
cap.release()
cv2.destroyAllWindows()