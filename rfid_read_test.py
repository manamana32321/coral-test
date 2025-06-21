import time
from periphery import GPIO

from mfrc522 import MFRC522  # RPi.GPIO 대신 periphery의 GPIO를 사용

# RST 핀 번호 설정 (BCM 핀 번호 기준, 코랄보드 22번핀 = GPIO 25)
# 코랄보드 GPIO 번호는 `gpioinfo` 명령어로 확인 가능
RST_PIN_BCM = 25

try:
    # GPIO 객체 생성 및 리셋 핀 초기화
    # /dev/gpiochip0의 25번 라인을 출력으로 설정
    reset_pin = GPIO("/dev/gpiochip0", RST_PIN_BCM, "out")
    print("GPIO 초기화 완료. RST 핀 제어 준비됨.")

    # MFRC522 객체 생성 (SPI 버스 0, 장치 0)
    MIFAREReader = MFRC522(bus=0, device=0, rst_pin_mode=MFRC522.RST_PIN_NONE)
    # rst_pin_mode를 NONE으로 설정하고 우리가 직접 제어

    print("RFID 리더가 준비되었습니다. 태그를 스캔해주세요...")
    print("프로그램을 종료하려면 Ctrl+C를 누르세요.")

    while True:
        # 1. 태그가 범위 안에 있는지 탐지
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # 2. 태그가 탐지되면
        if status == MIFAREReader.MI_OK:
            print("-" * 20)
            print("태그가 인식되었습니다!")

            # 3. 태그의 UID(고유 ID) 읽기
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                print(f"  - UID: {uid[0]}:{uid[1]}:{uid[2]}:{uid[3]}")

        # 너무 빠르게 반복하지 않도록 잠시 대기
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
except Exception as e:
    print(f"\n에러 발생: {e}")
finally:
    # GPIO 리소스 정리
    if "reset_pin" in locals():
        reset_pin.close()
