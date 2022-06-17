import cv2
from time import sleep
import RPi.GPIO as GPIO
import threading
import sys
import Motor

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

class AutoParking:
    def __init__(self):
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

    # 駐車マークを検出
    def mark_detection(self, image):
        pass

    # 駐車マークに真っ直ぐ向いていく
    def face_to_mark(self, coordinate_x):
        pass

    # 駐車マークまでの距離を取る
    def get_distance(self):
        pass

    # 経路の長さを計算する
    def calculate_path(self, distance_to_mark, turned_theta):
        pass

    # 駐車マークまで移動
    def move_to_mark(self, path_x, path_y, turned_theta):
        pass

    def end_process(self):
        GPIO.cleanup()


def main():
    moving_flag = False
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
            if auto_parking.can_move() and moving_flag == False:
                moving_flag = True
                auto_parking.move_forward(50)
            else:
                pass
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