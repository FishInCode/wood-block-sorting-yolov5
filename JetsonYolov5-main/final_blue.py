import sys
import cv2 
import imutils
import time  # 新增time模块
import uart
from yoloDet import YoloTRT

model_x1 = 326
model_x2 = 409
model_y1 = 196
model_y2 = 313

model_box_location = [[283,375,185,254],[215,304,162,223],[136,227,166,235],[60,149,204,273],[24,138,260,352],[112,230,321,437],[240,370,293,407]]

model_box = ["redcircle","bluetrapezium","bluetriangle","redrectangle","bluecircle","redtrapezium","redtriangle","bluerectangle"]
model_judge = ['','']   ###1代表当前，0代表前一个
triangle_box = []
trapezium_box = []


num_front = 0.0
flag_first = 0
flag_csd_start = 0
flag_turn = 0
flag_turn_back = 0
flag_csd_stop = 0
flag_csd_dw = 0
flag_first_start = 0
flag_first_detection = 0
flag_interrupt = 0
flag_priority = 0
flag_priority_next = 0
flag_box_init = 0
flag_catch = 0
flag_model_front = 0
flag_model_frstart = 0
flag_arm_frstart = 0
flag_arm_front = 0
flag_box_frstart = 0
flag_box_front = 0
num_csd = 0
count_model_front = 0
count_box_front = 0
count_arm_front = 0
count_csd = 0
count_start = 0
count_judge = 0
count_catch = 0
model_now = ''
model_last = ''
model_site = 0
model_task = ''
task_color = 'blue'
task_process = 1
model_task_box = ''
model_catch = ''
model_catch_next = ''
triangle_site = 0
trapezium_site = 0

# 初始化YOLO模型
model = YoloTRT(
    library="final/build/libmyplugins.so",
    engine="final/build/final.engine",
    conf=0.8,
    yolo_ver="v5"
)

# 使用摄像头（0代表默认摄像头）
cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

if not cap0.isOpened():
    print("无法打开摄像头0")
    sys.exit()

if not cap1.isOpened():
    print("无法打开摄像头1")
    sys.exit()

# 设置摄像头分辨率（可选）
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 初始化摄像头1的计时器和FPS
last_time_cam1 = 0

while True:
    # 处理摄像头0（实时检测）
    ret0, frame0 = cap0.read()

    if not ret0:
        print("无法获取视频流")
        break
    
    frame0 = imutils.resize(frame0, width=600)

    detections0, t0 = model.Inference(frame0)

    cv2.line(frame0,(300,0),(300,480),(100,100,100),2)
    cv2.line(frame0,(0,225),(600,225),(100,100,100),2)
    
    # 绘制检测结果
    for obj in detections0:
        if (obj['class']=='Hexagonal' or obj['class']=='trapezium' or obj['class']=='triangle') and count_start==0 and flag_first_start==0 and task_process == 0:
            uart.Serial_Send(0x02,0x04)
            count_start = 1
            flag_first_start = 1
        if obj['class']!='Hexagonal':
            box = obj['box']
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            cv2.rectangle(frame0, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if flag_csd_stop == 0 and abs((x1+x2)/2-300) < 240 and flag_csd_start == 0 and obj['class']!='triangle'and obj['class']!='trapezium' and task_process == 0:
                flag_csd_stop = 1 
                uart.Serial_Send(0x02,0x00)
                task_process = 1
                flag_first_start = 1
                time.sleep(0.4)

            if -25<(x1+x2)/2-300<25 and flag_csd_dw == 0 and flag_csd_stop == 1 and obj['class']!='triangle'and obj['class']!='trapezium':
                flag_csd_dw = 1
                model_task = obj['class']
                if model_task == 'circle':
                    num_front = 230
                elif model_task == 'rectangle':
                    num_front = 220.5
                model_task_box = task_color + model_task
                uart.Serial_Send(0x02,0x02)
                num_csd = 0
                task_process = 0
                time.sleep(0.2)

            if flag_turn_back == 1 and task_process == 0 and flag_priority == 2 and flag_model_frstart == 0 and obj['class'] == model_catch and abs((x1+x2)/2-300) < 100:
                flag_model_frstart = 1
                task_process = 1
                uart.Serial_Send(0x04,0x00)
                flag_model_front = 1
                            
            if flag_arm_frstart == 1 and flag_arm_front == 0 and flag_priority == 1:
                if abs((y1+y2)/2-237) < 3:
                    uart.Serial_Send(0x03,0x02)
                    flag_arm_front = 1
                
                else:
                    if count_arm_front == 0:
                        count_arm_front = 1
                        if (y1+y2)/2-237 <= 0:
                            uart.Serial_Send(0x03,0x01)
                        else:
                            uart.Serial_Send(0x03,0x04)
                    else:
                        if uart.Serial_Receive() == b'\xFF\x03\x01\xFE':
                            uart.Serial_Send(0x03,0x03)
                            time.sleep(0.2)
                            if (y1+y2)/2-237 <= 0:
                                uart.Serial_Send(0x03,0x01)
                            else:
                                uart.Serial_Send(0x03,0x04)

            if flag_arm_front == 1 and flag_box_frstart == 0:
                if uart.Serial_Receive() == b'\xFF\x01\x04\xFE':
                    flag_box_frstart = 1

            if flag_box_frstart == 1 and flag_box_front == 0 and obj['class'] == model_task_box and abs((x1+x2)/2-300) < 100:
                flag_box_front = 1
                uart.Serial_Send(0x05,0x00)
               
            label = f"{obj['class']} {obj['conf']:.2f}"
            cv2.putText(frame0, label, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow("Camera0 Detection", frame0)

    if flag_csd_stop == 1 and flag_csd_dw == 0:
        if num_csd >= 19:
            flag_csd_stop = 0
            num_csd = 0
            count_csd = 0
        if count_csd == 0:
            uart.Serial_Send(0x02,0x01)
            count_csd = 1
        if uart.Serial_Receive() == b'\xFF\x02\x01\xFE':
            num_csd += 1
            uart.Serial_Send(0x02,0x03)
            time.sleep(0.2)
            uart.Serial_Send(0x02,0x01)


    if flag_model_front == 1:
        if uart.Serial_Receive() == b'\xFF\x01\x03\xFE':
            uart.Serial_Send(0x01,0x01)
            ###放到回去后再次清零
            task_process = 0 
            if flag_priority_next == 0:
                flag_priority = 0
                model_catch = ''
                flag_catch = 0
            elif flag_priority_next == 2:
                flag_priority = 2
                flag_priority_next = 0
                model_catch = model_catch_next
                model_catch_next = ''
                count_catch = 0
            elif flag_priority_next == 1:
                flag_priority = 1
                flag_priority_next = 0
            count_model_front = 0
            flag_csd_start = 0
            flag_turn = 0
            flag_turn_back = 0
            flag_model_frstart = 0
            flag_model_front = 0
    
    if flag_box_front == 1:
        if uart.Serial_Receive() == b'\xFF\x01\x02\xFE':
            uart.Serial_Send(0x01,0x02)

            task_process = 0
            if flag_priority_next == 0:
                flag_priority = 0
            else:
                flag_catch = 1
                flag_priority = 2
                flag_priority_next = 0
                model_catch = model_catch_next
                model_catch_next = ''
                count_catch = 0
            flag_arm_frstart = 0
            flag_arm_front = 0
            flag_box_front = 0
            flag_box_frstart = 0
            flag_csd_start = 0
            flag_csd_dw = 0
            count_csd = 0
            flag_csd_stop = 0
            count_box_front = 0
            count_arm_front = 0
            model_task_box = ''

    # 处理摄像头1（间隔检测）
    ret1, frame1 = cap1.read()

    if not ret1:
        print("无法获取视频流")
        break
    
    frame1 = imutils.resize(frame1, width=600)

###    for i in range(7):
###        cv2.line(frame1,(i*100,0),(i*100,450),(100,100,100),2)
###    for i in range(6):
###        cv2.line(frame1,(0,i*90),(600,i*90),(100,100,100),2)
  
###    cv2.rectangle(frame1,(model_x1,model_y1),(model_x2,model_y2),(0,0,0),2)

    current_time = time.time()
    
    # 每2秒检测一次
    if (current_time - last_time_cam1 >= 0.75) and (flag_arm_frstart == 1 and flag_arm_front == 0)==0:
        detections1, t1 = model.Inference(frame1)
        for i in range(7):
            cv2.line(frame1,(i*100,0),(i*100,450),(100,100,100),2)
        for i in range(6):
           cv2.line(frame1,(0,i*90),(600,i*90),(100,100,100),2)
        cv2.rectangle(frame1,(model_x1,model_y1),(model_x2,model_y2),(0,0,0),2)
        for i in range(7):
            cv2.rectangle(frame1,(model_box_location[i][0],model_box_location[i][2]),(model_box_location[i][1],model_box_location[i][3]),(0,0,0),2)

        last_time_cam1 = current_time  # 更新最后检测时间
        
        # 绘制检测结果
        for obj in detections1:
            box = obj['box']
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            cv2.rectangle(frame1, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if model_x1 < x1 and x2 <model_x2 and model_y1 <y1 and y2 < model_y2:
                model_now = obj['class']
                
                if model_last == model_now and count_judge == 0:
                    count_judge = 1
                    if flag_catch == 1:
                        count_catch += 1
                    if flag_first_detection == 0 and model_now not in ["circle","trapezium","triangle","rectangle"]:
###                        flag_first_detection = 1
                        flag_box_init = 1
                        model_site = model_box.index(model_now)-1
                    elif model_now in ["circle","trapezium","triangle","rectangle"]:
                        flag_box_init = 0
                    model_site += 1
                    if model_site >= 8:
                        model_site = 0
                    model_judge[0] = model_judge[1]
                    model_judge[1] = model_now
                    ###uart.Serial_Send(model_site,0x01)
                
                if model_last != model_now:
                    count_judge = 0
                model_last = model_now
                



            label = f"{obj['class']} {obj['conf']:.2f}"
            cv2.putText(frame1, label, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        for i in range(7):
            cv2.line(frame1,(i*100,0),(i*100,450),(100,100,100),2)
        for i in range(6):
           cv2.line(frame1,(0,i*90),(600,i*90),(100,100,100),2)
        cv2.rectangle(frame1,(model_x1,model_y1),(model_x2,model_y2),(0,0,0),2)
        for i in range(7):
            cv2.rectangle(frame1,(model_box_location[i][0],model_box_location[i][2]),(model_box_location[i][1],model_box_location[i][3]),(0,0,0),2)

    cv2.imshow("Camera1 Detection", frame1)
    if flag_box_init == 0:
        triangle_box = [obj['box'] for obj in detections1 if obj['class']==task_color+'triangle']
        trapezium_box = [obj['box'] for obj in detections1 if obj['class']==task_color+'trapezium']
        if len(triangle_box) == 1:
            x11,y11,x22,y22=map(int,triangle_box[0])
            for i in range(7):
                if model_box_location[i][0] < x11 and model_box_location[i][1] > x22 and model_box_location[i][2] < y11 and model_box_location[i][3] > y22:
                    triangle_site = i+1
                    break
            if triangle_site != 0:
                triangle_site = (model_box.index(task_color+'triangle') + 8 - triangle_site) % 8
                model_site = triangle_site
                triangle_site = 0
            triangle_box = []
            
        if len(trapezium_box) == 1:
            x11,y11,x22,y22=map(int,trapezium_box[0])
            for i in range(7):
                if model_box_location[i][0] < x11 and model_box_location[i][1] > x22 and model_box_location[i][2] < y11 and model_box_location[i][3] > y22:
                    trapezium_site = i+1
                    break
            if trapezium_site != 0:
                trapezium_site = (model_box.index(task_color+'trapezium') + 8 - trapezium_site) % 8
                model_site = trapezium_site
                trapezium_site = 0
            trapezium_box = []
        flag_box_init = 1

    if flag_box_init == 1:
        if model_judge[1] == model_task_box and model_task_box != '' and flag_priority != 1:
            if flag_priority == 2:
                if (model_judge[0] in ["circle","triangle","rectangle","trapezium"]) and (task_color not in model_box[(model_site+7)%8]):
                    flag_interrupt = 1
                    flag_catch = 0
                    flag_priority = 1
                else:
                    flag_priority_next = 1
            elif flag_priority == 0:
                flag_priority = 1
            ###uart.Serial_Send(0x02,0x01)

        if model_judge[1] in ["circle","triangle","rectangle","trapezium"] and ((model_judge[1] != model_catch and flag_priority_next == 0) or (model_judge[1] != model_catch_next and flag_priority_next == 2)) and (task_color not in model_box[model_site]):
            if flag_priority == 0:
                flag_priority = 2
                flag_catch = 1
                count_catch = 0
                model_catch = model_judge[1]
            elif flag_priority == 2:
                flag_priority_next = 2
                model_catch_next = model_judge[1]
            elif flag_priority == 1:
                flag_priority_next = 2
                model_catch_next = model_judge[1]
            ###uart.Serial_Send(0x02,0x02)

        if flag_turn == 0 and task_process == 0 and flag_priority == 2 and count_catch >= 1 and flag_interrupt == 0:
            flag_first_start = 1
            task_process = 1
            uart.Serial_Send(0x00,0x01)
            flag_csd_start = 1
            flag_turn = 1
        
        if flag_turn_back == 0 and flag_turn == 1:
            if uart.Serial_Receive() == b'\xFF\x06\x01\xFE':
                flag_turn_back = 1
                task_process = 0
                uart.Serial_Send(0x06,0x01)
                time.sleep(0.2)

        if flag_priority == 1 and flag_interrupt == 1:    ### zhuan hui qu
            ###uart.Serial_Send(0x00,0x02)
            flag_interrupt = 0
            flag_catch = 0
            count_catch = 0
            model_catch = ''

        if flag_priority == 1 and flag_arm_frstart == 0 and task_process == 0:
            task_process = 1
            flag_arm_frstart = 1
            uart.Serial_Send(0x03,0x00)
            time.sleep(0.2)


    if flag_first == 0:
        if uart.Serial_Receive() == b'\xFF\x01\x02\xFE':
            task_process = 0
            flag_first = 1


    # 按'q'退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap0.release()
cap1.release()
cv2.destroyAllWindows()
