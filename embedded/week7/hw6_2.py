import RPi.GPIO as GPIO
import time

# 모터 및 스위치 핀 번호 설정
PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23  # 오른쪽 모터 제어용
BIN1 = 24
BIN2 = 25

switch_pins = [5, 6, 13, 19]  # SW1, SW2, SW3, SW4 스위치 핀 번호

# GPIO 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)

GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# 스위치 설정
for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# PWM 설정
L_Motor = GPIO.PWM(PWMA, 500)
R_Motor = GPIO.PWM(PWMB, 500)

L_Motor.start(0)  # 초기 정지
R_Motor.start(0)  # 초기 정지

previous_action = None  # 이전 동작 상태 초기화

def move_forward():
    """자동차 전진"""
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    L_Motor.ChangeDutyCycle(50)  # 50% 속도로 전진
    R_Motor.ChangeDutyCycle(50)
    return "전진"

def move_backward():
    """자동차 후진"""
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    L_Motor.ChangeDutyCycle(50)  # 50% 속도로 후진
    R_Motor.ChangeDutyCycle(50)
    return "후진"

def turn_left():
    """자동차 좌회전"""
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    L_Motor.ChangeDutyCycle(50)  # 왼쪽 모터 후진, 오른쪽 모터 전진
    R_Motor.ChangeDutyCycle(50)
    return "좌회전"

def turn_right():
    """자동차 우회전"""
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    L_Motor.ChangeDutyCycle(50)  # 왼쪽 모터 전진, 오른쪽 모터 후진
    R_Motor.ChangeDutyCycle(50)
    return "우회전"

def stop_motors():
    """모터 정지"""
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)
    return "정지"

try:
    while True:
        current_action = None  # 현재 동작 상태 초기화
        
        # 스위치 입력에 따른 동작 수행
        if GPIO.input(switch_pins[0]) == GPIO.HIGH:  # SW1 전진
            current_action = move_forward()
        elif GPIO.input(switch_pins[3]) == GPIO.HIGH:  # SW4 후진
            current_action = move_backward()
        elif GPIO.input(switch_pins[2]) == GPIO.HIGH:  # SW3 좌회전
            current_action = turn_left()
        elif GPIO.input(switch_pins[1]) == GPIO.HIGH:  # SW2 우회전
            current_action = turn_right()
        else:
            current_action = stop_motors()  # 스위치가 눌리지 않으면 정지

        # 상태가 변화했을 때만 출력
        if current_action != previous_action:
            print(current_action)  # 새로운 동작 상태 출력
            previous_action = current_action  # 이전 상태 업데이트

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

# PWM 및 GPIO 클린업
L_Motor.stop()
R_Motor.stop()
GPIO.cleanup()