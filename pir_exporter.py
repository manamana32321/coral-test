import time
from periphery import GPIO

# --- 설정 ---
# 네가 선택한 GPIO 라인 번호 6 사용
PIR_GPIO_LINE = 6
GPIO_CHIP = "/dev/gpiochip0"

# --- 메인 프로그램 ---
pir_pin = None
try:
    # GPIO 핀을 입력(in)으로 열기
    pir_pin = GPIO(GPIO_CHIP, PIR_GPIO_LINE, "in")

    print(f"PIR 센서(GPIO Line: {PIR_GPIO_LINE}) 초기화 중...")
    # 센서는 전원 인가 후 안정화 시간이 필요함 (최소 30초 이상 권장)
    time.sleep(10)
    print("=" * 30)
    print("센서 준비 완료. 움직임 감지를 시작합니다.")
    print("프로그램을 종료하려면 Ctrl+C를 누르세요.")
    print("=" * 30)

    last_state = False

    while True:
        current_state = pir_pin.read()

        # 상태가 이전과 다를 때만 메시지 출력 (터미널 도배 방지)
        if current_state != last_state:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            if current_state:
                # 움직임 감지!
                print(f"✅ [{timestamp}] 동아리방에 움직임이 감지되었습니다.")
            else:
                # 움직임 없음.
                print(f"⚪️ [{timestamp}] 상태: 정상 (움직임 없음)")

            last_state = current_state

        # 0.1초마다 상태를 확인하여 CPU 사용률을 낮춤
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
except Exception as e:
    print(f"\n에러 발생: {e}")
finally:
    # 프로그램 종료 시 GPIO 리소스 정리
    if pir_pin:
        pir_pin.close()
    print("GPIO 리소스가 정리되었습니다.")
