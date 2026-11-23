import sys
import cv2 
import imutils
# import uart
import time
import math
from yoloDet import YoloTRT

# 撞后要减小y的值，撞前要增大y的值。
# 撞左要减小x的值，撞右要增大x的值。
###    小





### y：大
### x：小                       大

flag_judge_box = 1
flag_turnbox = 1
flag_first_start = 1
flag_start = 0
flag_armfrt_start = 0
flag_boxgo_start = 0
flag_dp_dw = 1
flag_csd_dw = 1
flag_csd_stop = 1
flag_armfrt_dw = 1
flag_box_dw = 1
flag_boxgo_dw = 1
flag_boxblank = 0
flag_receive_turnbox = 1
flag_receive_blankbox_start = 1
flag_receive_blankbox = 1
flag_box_dynamic = 1
flag_box_dynamic_start = 1
count_csd = 1
count_armfrt = 1
count_boxgo = 1
count_turnbox = 1
count_box_put = 1
count_box_dynamic = 1
count_start = 1
direction_csd=1
direciton_box=1
num_front = 1
num_box = 1
num_csd = 0
model_now = ''

# 初始化YOLO模型
model = YoloTRT(
    library="final/build/libmyplugins.so",
    engine="final/build/final.engine",
    conf=0.80,
    yolo_ver="v5"
)

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
        
    # 执行目标检测
    detections , t = model.Inference(frame)
    
    cv2.line(frame,(300,0),(300,480),(100,100,100),2)
    cv2.line(frame,(200,0),(200,480),(100,100,100),2)
    cv2.line(frame,(400,0),(400,480),(100,100,100),2)
    cv2.line(frame,(0,237),(640,237),(100,100,100),2)

    # 在帧上绘制检测结果
    for obj in detections:
        if (obj['class']=='Hexagonal' or obj['class']=='trapezium' or obj['class']=='triangle') and count_start==0 and flag_first_start==0:
            # uart.Serial_Send(0x02,0x04)
            print(1)
            count_start = 1
            flag_first_start = 1
        if obj['class']!='Hexagonal' and obj['class']!='trapezium' and obj['class']!='triangle':
            box = obj['box']
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            
            if obj['conf'] > 0.8:
            # 绘制边界框
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                if flag_csd_stop == 0 and abs((x1+x2)/2-300) < 260 :
                    flag_csd_stop = 1 
                    # uart.Serial_Send(0x02,0x00)
                    print(1)
                    time.sleep(0.2)

                if -25<(x1+x2)/2-300<25 and flag_armfrt_start == 1 and flag_csd_stop == 1:
                    flag_csd_dw = 1
                    flag_first_start = 1
                    # uart.Serial_Send(0x02,0x02)
                    print(1)
                    time.sleep(0.4)

                    # uart.Serial_Send(0x03,0x00)
                    print(1)
                    time.sleep(0.2)
                    flag_armfrt_start = 0

                if  flag_start == 1 and flag_armfrt_start == 0:
                    if abs((y1+y2)/2-237) < 3:
                        flag_armfrt_dw = 1
                        time.sleep(0.2)
                        # uart.Serial_Send(0x03,0x02)
                        print(1)
                        time.sleep(0.4)
                        if obj['class']=='triangle':
                            # uart.Serial_Send(0x01,0x00)
                            print(1)
                            flag_start = 0
                            num_front = 212
                            num_box = 297
                        elif obj['class']=='circle':
                            # uart.Serial_Send(0x01,0x01)
                            print(1)
                            flag_start = 0
                            num_front = 230                          # num_front撞后要增大y的值，撞前要减小y的值。 num_box撞左要减小x的值，撞右要增大x的值。
                            num_box = 301.5
                            model_now = 'circle'
                        elif obj['class']=='trapezium':
                            # uart.Serial_Send(0x01,0x02)
                            print(1)
                            flag_start = 0
                            num_front = 212
                            num_box = 297
                        elif obj['class']=='rectangle':
                            # uart.Serial_Send(0x01,0x03)
                            print(1)
                            flag_start = 0
                            num_front = 220.5
                            num_box = 301.5
                            model_now = 'rectangle'
                    else:
                        if (y1+y2)/2-237 < 0:
                            direction_csd=1
                        else:
                            direction_csd=2
                        
                
                if abs((x1+x2)/2-320) < 100 and flag_box_dynamic == 1 and flag_boxgo_dw == 0 and flag_boxgo_start == 0 and (model_now in obj['class']):
                    if abs((y1+y2)/2-num_front) <= 0.6:
                        flag_boxgo_dw = 1
                        # uart.Serial_Send(0x04,0x02)
                        print(1)
                        time.sleep(0.4)
                    else:
                        if (y1+y2)/2-num_front < 0:
                            direciton_box = 1
                        else:
                            direciton_box = 2

                if flag_boxgo_dw ==1 and flag_dp_dw == 0 and abs((x1+x2)/2-300) < 100:
                    if (x1+x2)/2-num_box <= 0:
                        # uart.Serial_Send(0x05,0x02)
                        print(1)
                    elif (x1+x2)/2-num_box > 0:
                        # uart.Serial_Send(0x05,0x01)
                        print(1)
                    flag_dp_dw = 1
                    time.sleep(0.4)
                    # uart.Serial_Send(0x01,0x05)
                    print(1)

                if flag_box_dw == 0 and flag_start == 0:
                    if flag_turnbox == 1:
                        if abs((x1+x2)/2-300) < 100 and count_turnbox == 0:
                            if obj['class'] == 'redcircle' or obj['class'] == 'bluecircle' or obj['class'] == 'circle':
                                # uart.Serial_Send(0x06,0x00)
                                print(1)
                            elif obj['class'] == 'redtrapezium' or obj['class'] == 'bluetrapezium' or obj['class'] == 'trapezium':
                                # uart.Serial_Send(0x06,0x01)
                                print(1)
                            elif obj['class'] == 'redtriangle' or obj['class'] == 'bluetriangle' or obj['class'] == 'triangle':
                                # uart.Serial_Send(0x06,0x02)
                                print(1)
                            elif obj['class'] == 'redrectangle' or obj['class'] == 'bluerectangle' or obj['class'] == 'rectangle':
                                # uart.Serial_Send(0x06,0x03)
                                print(1)
                            count_turnbox = 1
                            flag_receive_turnbox = 1
                            time.sleep(0.4)
                            flag_turnbox = 0
                            flag_box_dw = 1
                if flag_receive_turnbox == 1 and flag_receive_blankbox == 0:
                    if flag_receive_blankbox_start == 1 :
                        flag_receive_blankbox_start = 1
                        if abs((x1+x2)/2-300) < 100:
                            if obj['class'] == model_now:
                                flag_boxblank = 0
                            else:
                                flag_boxblank = 1
                            if flag_boxblank == 0:
                                # uart.Serial_Send(0x07,0x00)
                                print(1)
                                time.sleep(0.2)
                            flag_receive_blankbox = 1
                            flag_receive_blankbox_start = 0
                    # if uart.Serial_Receive() == b'\xFF\x05\x01\xFE' or flag_receive_blankbox_start == 1 :
                    #     flag_receive_blankbox_start = 1
                    #     if abs((x1+x2)/2-300) < 100:
                    #         if obj['class'] == model_now:
                    #             flag_boxblank = 0
                    #         else:
                    #             flag_boxblank = 1
                    #         if flag_boxblank == 0:
                    #             # uart.Serial_Send(0x07,0x00)
                    #             print(1)
                    #             time.sleep(0.2)
                    #         flag_receive_blankbox = 1
                    #         flag_receive_blankbox_start = 0

                if flag_box_dynamic_start == 1 and flag_box_dynamic == 0 and abs((x1+x2)/2-300) < 100 and (model_now in obj['class']):
                    if abs((x1+x2)/2-num_box) < 1.5:
                        # uart.Serial_Send(0x08,0x03)
                        print(1)
                        time.sleep(0.2)
                        flag_box_dynamic = 1
                    else:
                        if count_box_dynamic == 0:
                            if (x1+x2)/2-num_box > 0:
                                # uart.Serial_Send(0x08,0x01)
                                print(1)
                            else:
                                # uart.Serial_Send(0x08,0x02)
                                print(1)
                            count_box_dynamic = 1
                        # if uart.Serial_Receive() == b'\xFF\x05\x02\xFE':
                        #     if (x1+x2)/2-num_box > 0:
                        #         # uart.Serial_Send(0x08,0x04)
                        #         print(1)
                        #         time.sleep(0.3)
                        #         # uart.Serial_Send(0x08,0x01)
                        #         print(1)
                        #     else:
                        #         # uart.Serial_Send(0x08,0x04)
                        #         print(1)
                        #         time.sleep(0.3)
                        #         # uart.Serial_Send(0x08,0x02)
                        #         print(1)
                        
            # 显示类别和置信度
                label = f"{obj['class']} {obj['conf']:.2f}"
                cv2.putText(frame, label, (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # 显示结果
    cv2.imshow("Camera Detection", frame)

    if flag_armfrt_dw == 1 and flag_turnbox == 0 and flag_judge_box ==  0:
        print(2)
        # if uart.Serial_Receive() == b'\xFF\x00\x01\xFE':
        #     flag_turnbox = 1
        #     flag_judge_box = 1


    if flag_receive_blankbox == 1 and flag_box_dynamic_start == 0:
        print(2)
        # if uart.Serial_Receive() == b'\xFF\x05\x01\xFE' or flag_boxblank == 1:
        #     # uart.Serial_Send(0x08,0x00)
        #     print(1)
        #     time.sleep(0.2)
        #     flag_box_dynamic_start = 1

    if flag_box_dynamic == 1 and flag_boxgo_start == 1:
        print(2)
        # if uart.Serial_Receive() == b'\xFF\x05\x01\xFE' :
        #     # uart.Serial_Send(0x08,0x05)
        #     print(1)
        #     time.sleep(0.2)
        #     # uart.Serial_Send(0x04,0x00)
        #     print(1)
        #     time.sleep(0.4)
        #     flag_boxgo_start = 0

    if flag_csd_stop == 1 and flag_csd_dw == 0:
        if num_csd >= 20:
            flag_csd_stop = 0
            num_csd = 0
            count_csd = 0
        if count_csd == 0:
            # uart.Serial_Send(0x02,0x01)
            print(1)
            count_csd = 1
        print(2)
        # if uart.Serial_Receive() == b'\xFF\x02\x01\xFE':
        #     num_csd += 1
        #     # uart.Serial_Send(0x02,0x03)
        #     print(1)
        #     time.sleep(0.2)
        #     # uart.Serial_Send(0x02,0x01)
        #     print(1)

    if flag_armfrt_start == 0 and flag_armfrt_dw == 0:
        if  count_armfrt == 0:
            if direction_csd == 1:
                # uart.Serial_Send(0x03,0x01)
                print(1)
            elif direction_csd == 2:
                # uart.Serial_Send(0x03,0x04)
                print(1)
            count_armfrt = 1
        print(2)
        # if uart.Serial_Receive() == b'\xFF\x03\x01\xFE':
        #     # uart.Serial_Send(0x03,0x03)
        #     print(1)
        #     time.sleep(0.2)
        #     if direction_csd == 1:
        #         # uart.Serial_Send(0x03,0x01)
        #         print(1)
        #     elif direction_csd == 2:
        #         # uart.Serial_Send(0x03,0x04)
        #         print(1)

    if flag_boxgo_start == 0 and flag_boxgo_dw == 0:
        if count_boxgo == 0:
            # uart.Serial_Send(0x04,0x01)
            print(1)
            count_boxgo = 1
        print(2)
        # if uart.Serial_Receive() == b'\xFF\x04\x01\xFE':
        #     # uart.Serial_Send(0x04,0x03)
        #     print(1)
        #     time.sleep(0.2)
        #     if direciton_box == 1 or direciton_box == 0:
        #         # uart.Serial_Send(0x04,0x01)
        #         print(1)
        #     elif direciton_box == 2:
        #         # uart.Serial_Send(0x04,0x04)
        #         print(1)

    if flag_dp_dw == 1:
        print(2)
        # if uart.Serial_Receive() == b'\xFF\x01\x02\xFE':
        #     flag_judge_box = 0
        #     flag_turnbox = 0
        #     flag_start = 1
        #     flag_armfrt_start = 1
        #     flag_boxgo_start = 1
        #     flag_armfrt_dw = 0
        #     flag_box_dw = 0
        #     flag_boxgo_dw = 0
        #     flag_csd_dw = 0
        #     flag_dp_dw = 0
        #     flag_csd_stop = 0
        #     flag_receive_blankbox = 0
        #     flag_receive_blankbox_start = 0
        #     flag_receive_turnbox = 0
        #     flag_box_dynamic = 0
        #     flag_box_dynamic_start = 0
        #     count_turnbox = 0
        #     count_csd = 0
        #     count_armfrt = 0
        #     count_boxgo = 0
        #     count_box_put = 0
        #     count_box_dynamic = 0
        #     count_start = 0
        #     direction_csd=0
        #     direciton_box=0
        #     num_front = 0
        #     num_box = 0
        #     num_csd = 0
        #     flag_first_start = 0
 


    # 按'q'退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
 
