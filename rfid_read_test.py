import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

# RFID 리더 객체 생성
# 이 라이브러리는 내부적으로 SPI 설정을 처리해줘
reader = SimpleMFRC522()

print("RFID 리더가 준비되었습니다. 태그를 스캔해주세요...")
print("프로그램을 종료하려면 Ctrl+C를 누르세요.")

try:
    while True:
        # 태그 읽기를 시도 (태그가 인식될 때까지 여기서 멈춤)
        id, text = reader.read()

        # 태그가 인식되면 ID를 출력
        print("-" * 20)
        print(f"태그가 인식되었습니다!")
        print(f"  - ID: {id}")
        # 참고: SimpleMFRC522 라이브러리는 태그에 텍스트를 쓸 수도 있어
        # 지금은 ID만 사용할 거야
        # print(f"  - Text: {text}")
        print("-" * 20)

        # 너무 빠르게 연속으로 읽히는 것을 방지하기 위해 잠시 대기
        time.sleep(1)

except KeyboardInterrupt:
    # Ctrl+C를 누르면 GPIO를 정리하고 프로그램 종료
    print("\n프로그램을 종료합니다.")
    GPIO.cleanup()
