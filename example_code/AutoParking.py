from re import X
from turtle import distance
import cv2
from time import sleep
import RPi.GPIO as GPIO
import threading
import sys
import Motor
import numpy as np
import time, math


MOTOR_RIGHT_PIN1 = 19
MOTOR_RIGHT_PIN2 = 13
MOTOR_RIGHT_PIN3 = 16
MOTOR_RIGHT_PIN4 = 20

MOTOR_LEFT_PIN1 = 7
MOTOR_LEFT_PIN2 = 5
MOTOR_LEFT_PIN3 = 6
MOTOR_LEFT_PIN4 = 12

ECHO_PIN = 4
TRIG_PIN = 17

PI = 3.1415927
WHEEL_R = 12.25
ROBOT_R = 41
SPEED = 0.005

Trig = 27                           
Echo = 18  
GPIO.setmode(GPIO.BCM)              
GPIO.setup(Trig, GPIO.OUT)          
GPIO.setup(Echo, GPIO.IN)

class AutoParking:
   

    def __init__(self):
        self.count_left = 0
        self.count_right = 0
        print('Init')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ECHO_PIN, GPIO.IN)
        GPIO.setup(TRIG_PIN, GPIO.OUT, initial=GPIO.LOW)
        
        self._motor_left = Motor.Motor(MOTOR_LEFT_PIN1, MOTOR_LEFT_PIN2, MOTOR_LEFT_PIN3, MOTOR_LEFT_PIN4)
        self._motor_right = Motor.Motor(MOTOR_RIGHT_PIN1, MOTOR_RIGHT_PIN2, MOTOR_RIGHT_PIN3, MOTOR_RIGHT_PIN4)
        print('Init done')

        self.thread_l = threading.Thread()
        self.thread_r = threading.Thread()

        self._moving_flag = False

    def _distance_trans_steps(self, distance):
        steps = int((180 * distance * 4096) / (PI * WHEEL_R * 360))
        print(steps)
        return steps

    def _angle_trans_steps(self, theta):
        L = (theta * PI * ROBOT_R) / 180
        steps = int((180 * L * 4096) / (PI * WHEEL_R * 360))
        print(steps)
        return steps

    def move_forward(self, distance):
        result = self._distance_trans_steps(distance)
        self.thread_l = threading.Thread(target=self._motor_left.Step_CCW, args=(result, SPEED))
        self.thread_l.setDaemon(False)
        self.thread_r = threading.Thread(target=self._motor_right.Step_CW, args=(result, SPEED))
        self.thread_r.setDaemon(False)
        self.thread_l.start()
        self.thread_r.start()

    def move_backward(self, distance):
        result = self._distance_trans_steps(distance)
        thread_l = threading.Thread(target=self._motor_left.Step_CW, args=(result, SPEED))
        thread_l.setDaemon(False)
        thread_r = threading.Thread(target=self._motor_right.Step_CCW, args=(result, SPEED))
        thread_r.setDaemon(False)
        thread_r.start()
        thread_l.start()

    def turn_left(self, theta):
        result = self._angle_trans_steps(theta)
        thread_l = threading.Thread(target=self._motor_left.Step_CW, args=(result, SPEED))
        thread_l.setDaemon(False)
        thread_r = threading.Thread(target=self._motor_right.Step_CW, args=(result, SPEED))
        thread_r.setDaemon(False)
        thread_l.start()
        thread_r.start()
    
    def turn_right(self, theta):
        result = self._angle_trans_steps(theta)
        thread_l = threading.Thread(target=self._motor_left.Step_CCW, args=(result, SPEED))
        thread_l.setDaemon(False)
        thread_r = threading.Thread(target=self._motor_right.Step_CCW, args=(result, SPEED))
        thread_r.setDaemon(False)
        thread_l.start()
        thread_r.start()

    def can_move(self):
        if self.thread_l.is_alive() == False and self.thread_r.is_alive() == False:
            return True
        else:
            return False
        
    def stop(self):
        result = 0
        self.thread_l = threading.Thread(target=self._motor_left.Step_CCW, args=(result, SPEED))
        self.thread_l.setDaemon(False)
        self.thread_r = threading.Thread(target=self._motor_right.Step_CW, args=(result, SPEED))
        self.thread_r.setDaemon(False)
        self.thread_l.start()
        self.thread_r.start()


    # 駐車マークを検出
    def mark_detection(self, image):
        """
        input: image

        ouput: circle x direction from input image
        """
    
    # Check if image is loaded fine
      
        hsvimage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([150, 10, 10], dtype="uint8")
        upper = np.array([180, 255, 255], dtype="uint8")
        mask = cv2.inRange(hsvimage, lower, upper)
        img1 = image.copy()
        img1[mask==0] = [0, 0, 0]
        hsv2rgb = cv2.cvtColor(img1, cv2.COLOR_HSV2RGB)
        gray = cv2.cvtColor(hsv2rgb, cv2.COLOR_RGB2GRAY)

        gray = cv2.medianBlur(gray, 5)
        rows = mask.shape[0]
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows,
                                   param1= 100, param2=19,
                                   minRadius=60, maxRadius=0)
        

        if circles is not None:
            circles = np.uint16(np.around(circles))

        
            return circles[0][0][0]
        else:
            pass
       


    # 駐車マークに真っ直ぐ向いていく
    def face_to_mark(self, coordinate_x):
        d = 1
        
        if 310 < coordinate_x < 330:
            print("stop")
            self.stop()
            turned_theta = abs(self.count_left*d - self.count_right*d)
            return True, turned_theta
        elif coordinate_x < 310:
            print("turn_left")
            self.turn_left(d)
            self.count_left += 1
        elif coordinate_x > 330:
            print("turn_right")
            self.turn_right(d)
            self.count_right +=1
     

    # 駐車マークまでの距離を取る
    def get_distance(self):
        GPIO.output(TRIG_PIN, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
        time.sleep(0.00001)                     #10μ秒間待つ
        GPIO.output(TRIG_PIN, GPIO.LOW)             #GPIO27の出力をLow(0V)にする

        while GPIO.input(ECHO_PIN) == GPIO.LOW:     #GPIO18がLowの時間
            sig_off = time.time()
        while GPIO.input(ECHO_PIN) == GPIO.HIGH:    #GPIO18がHighの時間
            sig_on = time.time()

        duration = sig_off - sig_on 
                #GPIO18がHighしている時間を算術
        distance_to_mark = abs(duration * 34000 / 2)
            
        if distance_to_mark > 2 and distance_to_mark < 400:   #距離を求める(cm)
            return distance_to_mark

    # 経路の長さを計算する
    def calculate_path(self, distance_to_mark, turned_theta):
        path_x = distance_to_mark * np.cos(math.radians(turned_theta))
        path_y = distance_to_mark * np.sin(math.radians(turned_theta))
        return path_x, path_y


    # 駐車マークまで移動
    def move_to_mark(self, path_x, path_y, turned_theta):
        count=1
        while(count!=0):
            if(count==1):
                self.turn_right(turned_theta)    
                if(self.can_move()==True):
                    count+=1

            elif(count==2):
                self.move_forward(int(path_x))
                if(self.can_move()==True):
                    count+=1
            elif(count==3):
                self.turnleft(90)
                if(self.can_move()==True):
                    count+=1            
            elif(count==4):
                self.move_forward(int(path_y))
                count==0
        return True

    def end_process(self):
        GPIO.cleanup()


def main():
    moving_flag = False
    turning_flag = False
    auto_parking = AutoParking()
    # カメラをセット
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    out = cv2.VideoWriter('robot.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (640, 480))
    # メインループ
    try:
        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                continue

            x = auto_parking.mark_detection(img)
            
            turned_theta = auto_parking.face_to_mark(x)
            print("-----Test-----")
            print(turned_theta)
            # print("flag: ", movin)
            print('-----Done------') 
            if turned_theta == None:
                pass
            else:
                print("-------break----------")
                print("distance = ", auto_parking.get_distance())
                distance = auto_parking.get_distance()
                path_x, path_y = auto_parking.calculate_path(distance, turned_theta[1])
                if auto_parking.can_move() and moving_flag == False:
                    moving_flag = True
                    auto_parking.move_to_mark(int(path_x), int(path_y), turned_theta)
                else:
                    pass
                break
                

            

            # if auto_parking.can_move() and moving_flag == False:
            #     moving_flag = True
                # moving_flag, turned_theta = auto_parking.face_to_mark(x)

                # print("-----Test-----")
                # print(turned_theta)
                # print('-----Done------')
                
                
                # distance_to_mark = get_distance()

                # path_x, path_y = calculate_path(distance_to_mark, turned_theta)

                # move_to_mark(path_x, path_y)
                # auto_parking.move_forward(50)
            # else:
            #     pass
            out.write(img)

    except KeyboardInterrupt:
        print('\nCtl+C')
    except Exception as e:
        print(str(e))
    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        auto_parking.end_process()
        print('End')


if __name__ == '__main__':
    main()
