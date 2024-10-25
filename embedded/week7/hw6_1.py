import RPi.GPIO as GPIO
import time

# 스위치 번호 설정
switch_pins = [5, 6, 13, 19]  # GPIO 번호
switch_values = [0, 0, 0, 0]  # 현재 스위치 값 저장
prev_switch_values = [0, 0, 0, 0]  # 이전 스위치 값 저장
click_counts = [0, 0, 0, 0]  # 스위치 클릭 횟수 저장

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 각 스위치 핀을 입력으로 설정하고 풀다운 저항 활성화
for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        for i, pin in enumerate(switch_pins):
            switch_values[i] = GPIO.input(pin)  # 현재 스위치 값 읽기

            # 스위치가 0 -> 1로 변할 때만 ("click" 출력 및 카운트 증가)
            if prev_switch_values[i] == 0 and switch_values[i] == 1:
                click_counts[i] += 1
                print(f"SW{i+1} click {click_counts[i]}")

            # 현재 스위치 값을 이전 값으로 저장
            prev_switch_values[i] = switch_values[i]

        time.sleep(0.1)  # 0.1초 대기

except KeyboardInterrupt:
    pass

GPIO.cleanup()