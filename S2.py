import RPi.GPIO as GPIO
import threading
import serial
import time

# 모터 및 핀 설정
PWMA = 18
AIN1 = 22
AIN2 = 27
PWMB = 23
BIN1 = 24
BIN2 = 25

# GPIO 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# PWM 설정
L_Motor = GPIO.PWM(PWMA, 500)
R_Motor = GPIO.PWM(PWMB, 500)
L_Motor.start(0)  # 초기 정지
R_Motor.start(0)  # 초기 정지

# Bluetooth 설정
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
gData = ""  # Bluetooth 데이터를 저장할 변수

# 모터 제어 함수
def turn_left():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(50)
    print("전진")

def turn_right():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(50)
    print("후진")

def move_forward():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(50)
    print("좌회전")

def move_backward():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    L_Motor.ChangeDutyCycle(50) 
    R_Motor.ChangeDutyCycle(50)
    print("우회전")

def stop_motors():
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)
    print("정지")

# Bluetooth 수신 스레드
def serial_thread():
    global gData
    while True:
        data = bleSerial.readline()
        data = data.decode().strip()
        gData = data

# 메인 제어 함수
def main():
    global gData
    try:
        while True:
            if gData == "go":
                move_forward()
            elif gData == "back":
                move_backward()
            elif gData == "left":
                turn_left()
            elif gData == "right":
                turn_right()
            elif gData == "stop":
                stop_motors()
            
            # gData 초기화하여 명령이 반복되지 않도록 설정
            gData = ""
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

# 프로그램 시작
if __name__ == "__main__":
    task1 = threading.Thread(target=serial_thread)
    task1.start()
    main()
    # 종료 시 GPIO 정리
    bleSerial.close()
    L_Motor.stop()
    R_Motor.stop()
    GPIO.cleanup()
