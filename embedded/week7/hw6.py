import RPi.GPIO as GPIO
import time

# Buzzer 및 Switch GPIO 설정
BUZZER = 12
switch_pins = [5, 6, 13, 19]  # 스위치 GPIO 번호

# 음계 주파수 리스트 (도레미파솔라시도)
frequencies = [262, 294, 330, 349, 392, 440, 494, 523]  # 도~도 음계 주파수

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Buzzer 핀 출력 설정
GPIO.setup(BUZZER, GPIO.OUT)
p = GPIO.PWM(BUZZER, 262)  # 초기 주파수 설정 (262 Hz)

# 스위치 핀 입력 설정 및 풀다운 저항 활성화
for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def play_music():
    """간단한 음악 패턴 재생"""
    music_pattern = [262, 262, 392, 392, 440, 440, 392]  # 간단한 음악 음계
    for freq in music_pattern:
        p.ChangeFrequency(freq)
        p.start(20)  # 소리 크기 설정 (20% duty cycle)
        time.sleep(0.3)
    p.stop()

def play_scale():
    """도~도까지 음계 재생"""
    for freq in frequencies:  # 도~도까지 재생
        p.ChangeFrequency(freq)
        p.start(20)  # 소리 크기 설정 (20% duty cycle)
        time.sleep(0.5)
    p.stop()

try:
    while True:
        # 스위치 눌림 감지 및 각 스위치별 동작
        for i, pin in enumerate(switch_pins):
            if GPIO.input(pin) == GPIO.HIGH:  # 스위치가 눌렸을 때
                if i == 0:  # 5번 핀: 도~도까지 음계 재생
                    print("도~도 음계 재생")
                    play_scale()
                    time.sleep(0.5)
                elif i == 1:  # 6번 핀: 미 음 재생
                    print("미 음계 재생")
                    p.ChangeFrequency(frequencies[2])  # '미' 음
                    p.start(20)
                    time.sleep(0.5)
                    p.stop()
                elif i == 2:  # 13번 핀: 솔 음 재생
                    print("솔 음계 재생")
                    p.ChangeFrequency(frequencies[4])  # '솔' 음
                    p.start(20)
                    time.sleep(0.5)
                    p.stop()
                elif i == 3:  # 19번 핀: 간단한 음악 재생
                    print("간단한 음악 재생")
                    play_music()
                    time.sleep(0.5)  # 음악이 끝날 때까지 대기

        time.sleep(0.1)  # 반복 주기 대기

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()